import blender_arch as A
import bpy
A.limpiar_escena()
ancho_plaza = 10.0
profundidad_plaza = 10.0
alto_base = 1.5
radio_base = 3.0
altura_esfera = 1.2
radio_esfera = 0.2
num_esferas = 3
potencia_luz = 10.0
A.crear_losa_rectangular(nombre='Base_Fuente', ancho=ancho_plaza, fondo=profundidad_plaza, espesor=alto_base, origen=(0, 0, 0), material='Concreto_Piso')
bpy.ops.mesh.primitive_cylinder_add(radius=radio_base, depth=alto_base, location=(0, 0, alto_base / 2))
base_escultura = bpy.context.active_object
A.asignar_material(base_escultura, 'Acero_Inox')
for i in range(num_esferas):
    angulo_x = i * (2 * 3.14159 / num_esferas)
    angulo_y = i * (2 * 3.14159 / num_esferas)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radio_esfera, location=(radio_base * 0.8 * np.cos(angulo_x) * np.sin(angulo_y), radio_base * 0.8 * np.sin(angulo_x) * np.sin(angulo_y), altura_esfera + radio_esfera))
    esfera = bpy.context.active_object
    A.asignar_material(esfera, 'Acero_Inox')
for i in range(4):
    angulo_z = i * (np.pi / 2)
    loc_x = radio_base * 0.8 * np.cos(angulo_z)
    loc_y = radio_base * 0.8 * np.sin(angulo_z)
    loc_z = altura_esfera - 0.5
    bpy.ops.light.add_type('POINT', radius=1.0)
    luz = bpy.context.active_object
    luz.location = (loc_x, loc_y, loc_z)
    luz.data.energy = potencia_luz
    A.asignar_material(luz, 'Luz_Blanca')