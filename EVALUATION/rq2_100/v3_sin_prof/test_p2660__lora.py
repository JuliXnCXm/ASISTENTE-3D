import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la habitación ---
largo_hab = 5.0
ancho_hab = 4.0
alto_hab = 2.8
grosor_muro = 0.15
grosor_losa = 0.2

# --- Crear Losa de Piso ---
bpy.ops.mesh.primitive_cube_add(location=(0, 0, -grosor_losa / 2))
losa_piso = bpy.context.active_object
losa_piso.name = "Losa_Piso"
losa_piso.dimensions = (largo_hab, ancho_hab, grosor_losa)

# --- Crear Muros ---
pos_x = largo_hab / 2
pos_y = ancho_hab / 2

# Muro Norte (+Y)
bpy.ops.mesh.primitive_cube_add(location=(0, pos_y, alto_hab / 2))
muro_norte = bpy.context.active_object
muro_norte.name = "Muro_Norte"
muro_norte.dimensions = (largo_hab + grosor_muro * 2, grosor_muro, alto_hab)

# Muro Sur (-Y)
bpy.ops.mesh.primitive_cube_add(location=(0, -pos_y, alto_hab / 2))
muro_sur = bpy.context.active_object
muro_sur.name = "Muro_Sur"
muro_sur.dimensions = (largo_hab + grosor_muro * 2, grosor_muro, alto_hab)

# Muro Este (+X)
bpy.ops.mesh.primitive_cube_add(location=(pos_x, 0, alto_hab / 2))
muro_este = bpy.context.active_object
muro_este.name = "Muro_Este"
muro_este.dimensions = (grosor_muro, ancho_hab, alto_hab)

# Muro Oeste (-X)
bpy.ops.mesh.primitive_cube_add(location=(-pos_x, 0, alto_hab / 2))
muro_oeste = bpy.context.active_object
muro_oeste.name = "Muro_Oeste"
muro_oeste.dimensions = (grosor_muro, ancho_hab, alto_hab)

# --- Crear Mobiliario ---
# Sofá
sofa_largo = 2.2
sofa_ancho = 0.9
sofa_alto_asiento = 0.4
sofa_alto_total = 0.75

bpy.ops.mesh.primitive_cube_add(location=(-1.2, 0.6, sofa_alto_asiento / 2))
sofa_base = bpy.context.active_object
sofa_base.name = "Sofa_Base"
sofa_base.dimensions = (sofa_largo, sofa_ancho, sofa_alto_asiento)

bpy.ops.mesh.primitive_cube_add(location=(-1.2, 0.6, sofa_alto_total / 2))
sofa_respaldo = bpy.context.active_object
sofa_respaldo.name = "Sofa_Respaldo"
sofa_respaldo.dimensions = (sofa_largo, 0.2, sofa_alto_total - sofa_alto_asiento)

# Mesa de Centro
mesa_largo = 1.2
mesa_ancho = 0.6
mesa_alto = 0.45

bpy.ops.mesh.primitive_cube_add(location=(0, 0, mesa_alto / 2))
mesa = bpy.context.active_object
mesa.name = "Mesa_Centro"
mesa.dimensions = (mesa_largo, mesa_ancho, mesa_alto)