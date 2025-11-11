import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
altura_poste = 4.0
diametro_poste = 0.15
largo_brazo = 1.0
diametro_brazo = 0.1
tamano_luminaria = 0.3

# --- Creación del poste vertical ---
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_poste / 2,
    depth=altura_poste,
    location=(0, 0, altura_poste / 2)
)
poste = bpy.context.active_object
poste.name = "Farola.Poste"

# --- Creación del brazo horizontal ---
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_brazo / 2,
    depth=largo_brazo,
    location=(0, largo_brazo / 2, altura_poste - diametro_brazo),
    rotation=(1.5708, 0, 0) # 90 grados en X
)
brazo = bpy.context.active_object
brazo.name = "Farola.Brazo"

# --- Creación de la luminaria ---
bpy.ops.mesh.primitive_cube_add(
    size=tamano_luminaria,
    location=(0, largo_brazo, altura_poste - diametro_brazo - tamano_luminaria / 2)
)
luminaria = bpy.context.active_object
luminaria.name = "Farola.Luminaria"