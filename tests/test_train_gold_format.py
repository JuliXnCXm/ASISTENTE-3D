import json
import sys
import types
from pathlib import Path
import numpy as np
from PIL import Image

TRAINING_DIR = Path(__file__).resolve().parents[1] / "TRAINING"
sys.path.insert(0, str(TRAINING_DIR))

try:
    import torch
except ImportError:
    # Lightweight numpy-backed tensor shim for local CPU environments without PyTorch installed
    class _FakeTensor:
        def __init__(self, arr):
            self.arr = np.asarray(arr)

        @property
        def shape(self):
            return self.arr.shape

        def squeeze(self, axis=0):
            return _FakeTensor(np.squeeze(self.arr, axis=axis))

        def tolist(self):
            return self.arr.tolist()

        def __getitem__(self, idx):
            return _FakeTensor(self.arr[idx])

        def __setitem__(self, idx, val):
            self.arr[idx] = val.arr if isinstance(val, _FakeTensor) else val

        def __ne__(self, other):
            return _FakeTensor(self.arr != other)

        def sum(self):
            return _FakeTensor(self.arr.sum())

        def any(self):
            return _FakeTensor(np.any(self.arr))

        def reshape(self, *shape):
            return _FakeTensor(self.arr.reshape(*shape))

        def float(self):
            return _FakeTensor(self.arr.astype(np.float32))

        def __add__(self, other):
            o = other.arr if isinstance(other, _FakeTensor) else other
            return _FakeTensor(self.arr + o)

        def __mul__(self, other):
            o = other.arr if isinstance(other, _FakeTensor) else other
            return _FakeTensor(self.arr * o)

        def __truediv__(self, other):
            o = other.arr if isinstance(other, _FakeTensor) else other
            return _FakeTensor(self.arr / o)

        def item(self):
            return self.arr.item()

    torch_mod = types.ModuleType("torch")
    torch_mod.long = np.int64
    torch_mod.bfloat16 = "bfloat16"
    torch_mod.tensor = lambda data, dtype=None: _FakeTensor(np.array(data, dtype=dtype or np.int64))
    torch_mod.randn = lambda *size: _FakeTensor(np.random.randn(*size).astype(np.float32))
    torch_mod.ones_like = lambda t: _FakeTensor(np.ones_like(t.arr))
    torch_mod.full_like = lambda t, fill: _FakeTensor(np.full_like(t.arr, fill))
    torch_mod.stack = lambda seq, dim=0: _FakeTensor(np.stack([x.arr for x in seq], axis=dim))
    torch_mod.cat = lambda seq, dim=0: _FakeTensor(np.concatenate([x.arr for x in seq], axis=dim))

    nn_mod = types.ModuleType("torch.nn")
    nn_mod.Identity = lambda: (lambda x: x)
    func_mod = types.ModuleType("torch.nn.functional")
    func_mod.pad = lambda t, pad_tuple, value=0: _FakeTensor(
        np.pad(t.arr, ((pad_tuple[0], pad_tuple[1]),), mode="constant", constant_values=value)
    )
    func_mod.cross_entropy = lambda logits, targets, ignore_index=-100, reduction="sum": _FakeTensor(
        np.array(float((targets.arr != ignore_index).sum()) * 1.25, dtype=np.float32)
    )
    nn_mod.functional = func_mod
    torch_mod.nn = nn_mod

    utils_mod = types.ModuleType("torch.utils")
    data_mod = types.ModuleType("torch.utils.data")
    data_mod.Dataset = object
    utils_mod.data = data_mod
    torch_mod.utils = utils_mod

    sys.modules["torch"] = torch_mod
    sys.modules["torch.nn"] = nn_mod
    sys.modules["torch.nn.functional"] = func_mod
    sys.modules["torch.utils"] = utils_mod
    sys.modules["torch.utils.data"] = data_mod
    import torch

for mod_name, attrs in [
    ("cv2", {"IMREAD_ANYCOLOR": 4, "IMREAD_ANYDEPTH": 2, "imread": lambda *a, **k: None}),
    (
        "transformers",
        {
            "Qwen2_5_VLForConditionalGeneration": object,
            "AutoProcessor": object,
            "BitsAndBytesConfig": object,
            "TrainingArguments": object,
            "Trainer": object,
            "EarlyStoppingCallback": object,
        },
    ),
    (
        "peft",
        {
            "LoraConfig": object,
            "get_peft_model": lambda *a, **k: None,
            "prepare_model_for_kbit_training": lambda *a, **k: None,
        },
    ),
]:
    if mod_name not in sys.modules:
        m = types.ModuleType(mod_name)
        for k, v in attrs.items():
            setattr(m, k, v)
        sys.modules[mod_name] = m

import train_qlora_multimodal as tqm


class DummyTokenizer:
    pad_token_id = 0
    assistant_seq = [101, 102]
    im_end_id = 103

    def encode(self, text, add_special_tokens=False):
        if "assistant" in text:
            return list(self.assistant_seq)
        return [10, 11]

    def convert_tokens_to_ids(self, tok):
        if tok == "<|im_end|>":
            return self.im_end_id
        return 0


class DummyProcessor:
    def __init__(self):
        self.tokenizer = DummyTokenizer()

    def apply_chat_template(self, messages, tokenize=False, add_generation_prompt=False):
        parts = []
        for m in messages:
            role = m["role"]
            txt = " ".join(c.get("text", "<IMG>") for c in m["content"])
            parts.append(f"<|im_start|>{role}\n{txt}<|im_end|>")
        return "\n".join(parts)

    def __call__(self, text, images=None, padding=False, return_tensors="pt"):
        prompt = text[0]
        n_assistant = prompt.count("<|im_start|>assistant\n")
        ids = [1, 2, 3, 4]
        for _ in range(n_assistant):
            ids.extend([101, 102, 50, 51, 52, 103, 5, 6])
        input_ids = torch.tensor([ids], dtype=torch.long)
        attention_mask = torch.ones_like(input_ids)
        out = {"input_ids": input_ids, "attention_mask": attention_mask}
        if images:
            out["pixel_values"] = torch.randn(len(images) * 4, 16)
            out["image_grid_thw"] = torch.tensor([[1, 2, 2]] * len(images), dtype=torch.long)
        return out


def test_qwen_vl_dataset_and_collator_support_gold_matrix_modality_dropout(tmp_path: Path):
    img_path = tmp_path / "ext_0001.jpg"
    Image.new("RGB", (256, 256), color=(120, 150, 180)).save(img_path)

    jsonl_path = tmp_path / "train_gold_sample.jsonl"
    records = [
        # 1. Creation with top-level image (no depth EXR present)
        {
            "id": "ext_0001__image_plus_prompt",
            "scene_id": "ext_0001",
            "matrix_category": "exterior_creation",
            "image": str(img_path),
            "messages": [
                {"role": "system", "content": "System"},
                {"role": "user", "content": "<image>\n[NIVEL_DISENO: LOD_500_ULTRA_DETALLE] Crea escena"},
                {"role": "assistant", "content": "<plan_arquitectonico>{}</plan_arquitectonico>\n```python\nimport bpy\n```"},
            ],
        },
        # 2. Text-only creation (Modality Dropout: image is None)
        {
            "id": "ext_0001__text_only",
            "scene_id": "ext_0001",
            "matrix_category": "exterior_creation",
            "image": None,
            "messages": [
                {"role": "system", "content": "System"},
                {"role": "user", "content": "[NIVEL_DISENO: LOD_500_ULTRA_DETALLE] Crea escena solo por texto"},
                {"role": "assistant", "content": "<plan_arquitectonico>{}</plan_arquitectonico>\n```python\nimport bpy\n```"},
            ],
        },
        # 3. Multi-turn Surgical Edit (2 user turns + 2 assistant turns)
        {
            "id": "ext_0001__exterior_edit",
            "scene_id": "ext_0001",
            "matrix_category": "exterior_edit",
            "image": str(img_path),
            "messages": [
                {"role": "system", "content": "System"},
                {"role": "user", "content": "<image>\nCrea escena"},
                {"role": "assistant", "content": "<plan_arquitectonico>{}</plan_arquitectonico>\n```python\nimport bpy\n```"},
                {"role": "user", "content": "Completa la escalera y puerta de 2m"},
                {"role": "assistant", "content": "<plan_edicion>{}</plan_edicion>\n```python\nimport bpy\n```"},
            ],
        },
    ]
    with jsonl_path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    proc = DummyProcessor()
    ds = tqm.QwenVLDataset(
        str(jsonl_path),
        proc,
        max_length=8192,
        assets_dir=str(tmp_path),
        usar_profundidad=True,
        usar_camara=True,
    )
    assert len(ds) == 3
    assert ds.n_con_imagen == 2

    item_img = ds[0]
    item_txt = ds[1]
    item_edit = ds[2]

    assert "pixel_values" in item_img
    assert "pixel_values" not in item_txt
    assert int((item_edit["labels"] != -100).sum().item()) == 8

    collator = tqm.QwenVLCollator(pad_token_id=0)
    batch = collator([item_img, item_txt, item_edit])
    assert batch["input_ids"].shape[0] == 3
    assert "pixel_values" in batch
    assert batch["pixel_values"].shape[0] == 8


def test_qwen_vl_dataset_preserves_legacy_multimodal_depth_guard(tmp_path: Path):
    import pytest

    img_path = tmp_path / "p0001_rgb.png"
    Image.new("RGB", (128, 128), color=(100, 120, 140)).save(img_path)

    legacy_jsonl = tmp_path / "legacy_missing_depth.jsonl"
    legacy_rec = {
        "id": "p0001",
        "multimodal": {
            "image": str(img_path),
            "metric_depth": "nonexistent_depth.exr",
        },
        "messages": [
            {"role": "system", "content": "System"},
            {"role": "user", "content": "<image>\nCrea escena"},
            {"role": "assistant", "content": "import bpy"},
        ],
    }
    legacy_jsonl.write_text(json.dumps(legacy_rec) + "\n", encoding="utf-8")

    with pytest.raises(SystemExit):
        tqm.QwenVLDataset(
            str(legacy_jsonl),
            DummyProcessor(),
            assets_dir=str(tmp_path),
            usar_profundidad=True,
        )


def test_descargar_assets_syncs_hf_gold_splits(tmp_path: Path, monkeypatch):
    import huggingface_hub

    def fake_snapshot_download(repo_id, repo_type, local_dir, allow_patterns, max_workers=16):
        assert "images/*" in allow_patterns
        assert "data/*.jsonl" in allow_patterns
        dl_data = Path(local_dir) / "data"
        dl_data.mkdir(parents=True, exist_ok=True)
        for sp in ("train", "validation", "test"):
            (dl_data / f"{sp}.jsonl").write_text(f'{{"split": "{sp}"}}\n', encoding="utf-8")

    monkeypatch.setattr(huggingface_hub, "snapshot_download", fake_snapshot_download)
    monkeypatch.setattr(huggingface_hub, "hf_hub_download", lambda **kwargs: None)
    monkeypatch.setattr(tqm, "SCRIPT_DIR", str(tmp_path / "TRAINING"))

    tqm.descargar_assets(str(tmp_path / "DATASET"), con_profundidad=False)
    for sp in ("train", "validation", "test"):
        synced = tmp_path / "TRAINING" / "data" / f"{sp}_multimodal.jsonl"
        assert synced.is_file()
        assert synced.read_text(encoding="utf-8").strip() == f'{{"split": "{sp}"}}'


def test_chunked_cross_entropy_trainer_computes_exact_loss_without_full_upcast():
    trainer = tqm.ChunkedCrossEntropyTrainer.__new__(tqm.ChunkedCrossEntropyTrainer)

    class FakeLinear:
        in_features = 16
        out_features = 32

        def __call__(self, h):
            assert h.shape[-1] == 16
            b, t, _ = h.shape
            return torch.randn(b, t, 32)

    class InnerModel:
        def __init__(self):
            self.lm_head = FakeLinear()
            self._modules = {"lm_head": self.lm_head}

    class OuterPeftWrapper:
        def __init__(self):
            self.inner = InnerModel()

        @property
        def lm_head(self):
            return self.inner.lm_head

        def modules(self):
            return [self, self.inner]

        def __call__(self, **kwargs):
            assert "labels" not in kwargs
            b, seq_len = kwargs["input_ids"].shape
            hidden = torch.randn(b, seq_len, 16)
            return {"logits": self.inner.lm_head(hidden)}

    peft_model = OuterPeftWrapper()
    orig_head = peft_model.inner.lm_head
    input_ids = torch.tensor([[1, 2, 3, 4, 5, 6]], dtype=torch.long)
    labels = torch.tensor([[-100, -100, 3, 4, 5, -100]], dtype=torch.long)
    loss = trainer.compute_loss(peft_model, {"input_ids": input_ids, "labels": labels})
    assert loss is not None
    assert peft_model.inner.lm_head is orig_head




