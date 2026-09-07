import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones habitación
dim_x, dim_y, dim_z = 4.0, 3.5, 2.5
grosor_muro = 0.15

# Suelo
bpy.ops.mesh.primitive_cube_add(location=(0, 0, -grosor_muro / 2))
suelo = bpy.context.active_object
suelo.name = 'Suelo'
suelo.dimensions = (dim_x, dim_y, grosor_muro)

# Paredes
locs_dims = [
    ((0, dim_y/2 - grosor_muro/2, dim_z/2), (dim_x, grosor_muro, dim_z)), # Fondo
    ((0, -dim_y/2 + grosor_muro/2, dim_z/2), (dim_x, grosor_muro, dim_z)),# Frontal
    ((dim_x/2 - grosor_muro/2, 0, dim_z/2), (grosor_muro, dim_y - 2*grosor_muro, dim_z)), # Derecha
    ((-dim_x/2 + grosor_muro/2, 0, dim_z/2), (grosor_muro, dim_y - 2*grosor_muro, dim_z)) # Izquierda
]
for i, (loc, dim) in enumerate(locs_dims):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    muro = bpy.context.active_object
    muro.name = f'Muro_{i+1}'
    muro.dimensions = dim

# Cama
cama_largo, cama_ancho, cama_alto_base = 2.0, 1.0, 0.3
colchon_alto = 0.2
cama_x, cama_y, cama_z = 0, dim_y/2 - grosor_muro - cama_ancho/2, cama_alto_base/2
bpy.ops.mesh.primitive_cube_add(location=(cama_x, cama_y, cama_z))
base_cama = bpy.context.active_object
base_cama.name = 'Base_Cama'
base_cama.dimensions = (cama_largo, cama_ancho, cama_alto_base)

bpy.ops.mesh.primitive_cube_add(location=(cama_x, cama_y, cama_alto_base + colchon_alto/2))
colchon = bpy.context.active_object
colchon.name = 'Colchon'
colchon.dimensions = (cama_largo, cama_ancho, colchon_alto)

# Mesita de noche
mesita_dim = (0.4, 0.4, 0.5)
gap = 0.1
mesita_x = cama_largo/2 + gap + mesita_dim[0]/2
mesita_y = dim_y/2 - grosor_muro - mesita_dim[1]/2
mesita_z = mesita_dim[2]/2
bpy.ops.mesh.primitive_cube_add(location=(mesita_x, mesita_y, mesita_z))
mesita = bpy.context.active_object
mesita.name = 'Mesita_Noche'
mesita.dimensions = mesita_dim