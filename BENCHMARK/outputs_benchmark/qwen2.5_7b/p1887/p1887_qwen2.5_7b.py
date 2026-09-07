import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el escritorio en forma de L
bpy.ops.mesh.primitive_cube_add(size=1, location=(2, 0, 0))
escritorio = bpy.context.object
escritorio.scale = (3, 1.5, 0.1)
bpy.ops.transform.translate(value=(-1.5, -0.75, 0))

# Crear la silla de oficina
silla_base = bpy.ops.mesh.primitive_cube_add(size=1, location=(2, -2, 0))
silla_base = bpy.context.object
silla_base.scale = (0.8, 0.8, 1)
bpy.ops.transform.translate(value=(-0.4, -1.6, 0))

silla_asiento = bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.5, location=(2, -2, 0))
silla_asiento = bpy.context.object
bpy.ops.transform.translate(value=(-0.4, -1.7, 0))

# Crear la estantería de pared
estanteria = bpy.ops.mesh.primitive_cube_add(size=1, location=(5, 0, 0))
estanteria = bpy.context.object
estanteria.scale = (2, 1, 0.3)
bpy.ops.transform.translate(value=(-1, -0.15, 0))

# Aplicar modificadores paramétricos para la estantería
estanteria.modifiers.new(name="Array", type='ARRAY')
estanteria.modifiers["Array"].count = 4

estanteria.modifiers.new(name="Bevel", type='BEVEL')
estanteria.modifiers["Bevel"].width = 0.1

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if "BLEND_OUT" in dir(bpy.app):
    bpy.ops.wm.save_as_mainfile(filepath=bpy.app.blend_out)