import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el escritorio en forma de L
bpy.ops.mesh.primitive_cube_add(size=1, location=(2, 0, 0))
escritorio = bpy.context.object
escritorio.scale = (3, 1.5, 0.5)
bpy.ops.transform.translate(value=(0, -1.5, 0))

# Crear la silla de oficina
silla_base = bpy.ops.mesh.primitive_cube_add(size=1, location=(-2, 0, 0))
silla_base = bpy.context.object
silla_base.scale = (1, 1, 0.8)
bpy.ops.transform.translate(value=(0, -1, 0))

silla_asiento = bpy.ops.mesh.primitive_cube_add(size=1, location=(-2, 0, -0.5))
silla_asiento = bpy.context.object
silla_asiento.scale = (1.2, 1.2, 0.3)
bpy.ops.transform.translate(value=(0, -1, 0))

# Crear la estantería de pared
estanteria = bpy.ops.mesh.primitive_cube_add(size=1, location=(-4, 1, 0))
estanteria = bpy.context.object
estanteria.scale = (0.5, 2, 1)
bpy.ops.transform.translate(value=(-3, 0, 0))

# Aplicar modificadores para el diseño paramétrico
estanteria.modifiers.new(name="Array", type='ARRAY')
estanteria.modifiers["Array"].count = 4

estanteria.modifiers.new(name="Bevel", type='BEVEL')
estanteria.modifiers["Bevel"].width = 0.1

# Guardar el archivo .blend si existe la variable de entorno BLEND_OUT
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)