import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la habitación
ancho = 5
alto = 4
altura = 2.7
espesor_pared = 0.15

# Crea el suelo
bpy.ops.mesh.primitive_plane_add(size=ancho, enter_editmode=False, align='WORLD', location=(0, 0, altura))
suelo = bpy.context.active_object
suelo.name = 'Suelo'
suelo.scale = (ancho, alto, 1)

# Crea el techo
bpy.ops.mesh.primitive_plane_add(size=ancho, enter_editmode=False, align='WORLD', location=(0, 0, altura - espesor_pared))
techo = bpy.context.active_object
techo.name = 'Techo'
techo.scale = (ancho, alto, 1)

# Crea las paredes
bpy.ops.mesh.primitive_plane_add(size=alto, enter_editmode=False, align='WORLD', location=(0, -ancho/2 + espesor_pared, altura))
pared_norte = bpy.context.active_object
pared_norte.name = 'Pared Norte'
pared_norte.scale = (espesor_pared, alto, 1)
bpy.ops.transform.translate(value=(0, ancho, 0), orient_type='GLOBAL', orient_matrix=((0, 1, 0), (-1, 0, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')
pared_sur = bpy.context.active_object
pared_sur.name = 'Pared Sur'
pared_sur.scale = (espesor_pared, alto, 1)
bpy.ops.transform.translate(value=(ancho/2 - espesor_pared, ancho, 0), orient_type='GLOBAL', orient_matrix=((0, 1, 0), (-1, 0, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')
pared_este = bpy.context.active_object
pared_este.name = 'Pared Este'
pared_este.scale = (espesor_pared, alto, 1)
bpy.ops.transform.translate(value=(-ancho/2 + espesor_pared, ancho, 0), orient_type='GLOBAL', orient_matrix=((0, 1, 0), (-1, 0, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')
pared_oeste = bpy.context.active_object
pared_oeste.name = 'Pared Oeste'
pared_oeste.scale = (espesor_pared, alto, 1)

# Crea la cama simple
bpy.ops.mesh.primitive_cube_add(size=2.5, enter_editmode=False, align='WORLD', location=(0, -ancho/2 + espesor_pared + 0.75, altura - espesor_pared))
cama = bpy.context.active_object
cama.name = 'Cama'
cama.scale = (1, 2, 1)

# Crea la mesa de noche
bpy.ops.mesh.primitive_cube_add(size=1.5, enter_editmode=False, align='WORLD', location=(0, -ancho/2 + espesor_pared + 1.25, altura - espesor_pared))
mesa_noche = bpy.context.active_object
mesa_noche.name = 'Mesa Noche'
mesa_noche.scale = (1, 1, 1)

# Guardar .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])