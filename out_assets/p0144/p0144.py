import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
caja_l = 1.2
caja_w = 0.4
caja_h = 0.3
pata_s = 0.05 # lado de la pata
pata_h = 0.2

# Crear la caja de la jardinera
loc_caja_z = pata_h + caja_h / 2
bpy.ops.mesh.primitive_cube_add(
    location=(caja_l/2, caja_w/2, loc_caja_z),
    scale=(caja_l, caja_w, caja_h)
)
bpy.context.active_object.name = "CajaJardinera"

# Crear las 4 patas
posiciones = [
    (pata_s/2, pata_s/2),
    (caja_l - pata_s/2, pata_s/2),
    (pata_s/2, caja_w - pata_s/2),
    (caja_l - pata_s/2, caja_w - pata_s/2)
]

for i, pos in enumerate(posiciones):
    bpy.ops.mesh.primitive_cube_add(
        location=(pos[0], pos[1], pata_h/2),
        scale=(pata_s, pata_s, pata_h)
    )
    bpy.context.active_object.name = f"PataJardinera_{i+1}"