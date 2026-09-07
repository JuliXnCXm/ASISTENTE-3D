import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = ROOT / "DATASET" / "dataset_creation_v1.json"
BENCHMARK_PROMPTS = ROOT / "BENCHMARK" / "prompts.json"

def main():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    items = data.get("items", {})
    
    # Filtrar solo los de test
    test_items = {k: v for k, v in items.items() if v.get("split") == "test"}
    
    # Separar por dominio
    interiores = [v for v in test_items.values() if v["domain"] == "interior"]
    exteriores = [v for v in test_items.values() if v["domain"] == "exterior"]
    
    # Muestrear aleatoriamente 50 de cada uno (fijando semilla para reproducibilidad)
    random.seed(42)
    sample_int = random.sample(interiores, min(50, len(interiores)))
    sample_ext = random.sample(exteriores, min(50, len(exteriores)))
    
    benchmark_set = sample_int + sample_ext
    
    # Formatear para el benchmark
    prompts_out = []
    for item in benchmark_set:
        prompts_out.append({
            "id": item["id"],
            "title": f"{item['domain']} - {item['category']} ({item['complexity']})",
            "prompt": item["prompt"],
            "python_code": item["python_code"] # Se guarda como Ground Truth para el evaluador
        })
        
    with open(BENCHMARK_PROMPTS, "w", encoding="utf-8") as f:
        json.dump(prompts_out, f, ensure_ascii=False, indent=2)
        
    print(f"Generado BENCHMARK/prompts.json con {len(prompts_out)} casos del Test Set.")

if __name__ == "__main__":
    main()
