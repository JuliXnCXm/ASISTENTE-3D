import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el colchón de textil blanco
bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0, 0, -0.5))
colchon = bpy.context.object
colchon.scale = (0.8, 0.8, 1)  # Ajustar el tamaño a 1.6m x 2.0m x 0.1m
colchon.name = "Colchon"
bpy.ops.object.shade_smooth()
colchon.active_material = bpy.data.materials.new(name="Blanco")
colchon.active_material.diffuse_color = (1, 1, 1, 1)

# Crear la estructura de madera de nogal
madera = bpy.data.materials.new(name="Nogal")
madera.diffuse_color = (0.5, 0.3, 0.2, 1)

# Pies de cama
bpy.ops.mesh.primitive_cube_add(size=0.1, location=(-0.8, -1, -0.6))
pies_cama = bpy.context.object
pies_cama.scale = (0.4, 0.4, 1)
pies_cama.name = "PieIzquierdo"
pies_cama.active_material = madera

bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0.8, -1, -0.6))
pies_cama = bpy.context.object
pies_cama.scale = (0.4, 0.4, 1)
pies_cama.name = "PieDerecho"
pies_cama.active_material = madera

bpy.ops.mesh.primitive_cube_add(size=0.1, location=(-0.8, 1, -0.6))
pies_cama = bpy.context.object
pies_cama.scale = (0.4, 0.4, 1)
pies_cama.name = "PieIzquierdo2"
pies_cama.active_material = madera

bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0.8, 1, -0.6))
pies_cama = bpy.context.object
pies_cama.scale = (0.4, 0.4, 1)
pies_cama.name = "PieDerecho2"
pies_cama.active_material = madera

# Lado izquierdo de la cama
bpy.ops.mesh.primitive_cube_add(size=0.1, location=(-0.8, -0.5, -0.6))
lado_izq = bpy.context.object
lado_izq.scale = (0.4, 1.5, 1)
lado_izq.name = "LadoIzquierdo"
lado_izq.active_material = madera

# Lado derecho de la cama
bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0.8, -0.5, -0.6))
lado_der = bpy.context.object
lado_der.scale = (0.4, 1.5, 1)
lado_der.name = "LadoDerecho"
lado_der.active_material = madera

# Pared frontal de la cama
bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0, -0.9, -0.6))
pared_frontal = bpy.context.object
pared_frontal.scale = (1.6, 0.2, 1)
pared_frontal.name = "ParedFrontal"
pared_frontal.active_material = madera

# Pared trasera de la cama
bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0, -0.95, -0.6))
pared_trasera = bpy.context.object
pared_trasera.scale = (1.6, 0.2, 1)
pared_trasera.name = "ParedTrasera"
pared_trasera.active_material = madera

# Guardar el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)