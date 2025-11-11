import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
diametro_esfera = 0.4
altura_esfera = 2.5
largo_cable = 0.8

# --- Creación de la esfera (pantalla) ---
radio_esfera = diametro_esfera / 2
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=radio_esfera,
    location=(0, 0, altura_esfera),
    segments=32,
    ring_count=16
)
bpy.context.object.name = 'Pantalla_Lampara'

# --- Creación del cable ---
altura_cable = altura_esfera + radio_esfera + largo_cable / 2
bpy.ops.mesh.primitive_cylinder_add(
    radius=0.01,
    depth=largo_cable,
    location=(0, 0, altura_cable)
)
bpy.context.object.name = 'Cable_Lampara'

# --- Creación de la fuente de luz ---
bpy.ops.object.light_add(
    type='POINT',
    radius=0.2,
    location=(0, 0, altura_esfera)
)
bpy.context.object.data.energy = 50 # Watts
bpy.context.object.name = 'Luz_Puntual'