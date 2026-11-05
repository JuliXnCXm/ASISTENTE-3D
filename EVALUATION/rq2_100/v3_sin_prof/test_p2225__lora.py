import blender_arch as A
import bpy

A.limpiar_escena()

# --- Parámetros ---
ancho_plaza = 12.0
profundidad_plaza = 12.0
alto_fuente = 2.5
radio_base = 3.0
radio_esfera = 0.6
num_esferas = 3
distancia_z_esfera = 1.2
altura_luz_sumergida = -1.5

# --- Base de la fuente ---
A.crear_losa_rectangular(
    nombre="Base_Plaza",
    ancho=ancho_plaza,
    fondo=profundidad_plaza,
    espesor=0.2,
    origen=(0, 0, 0),
    material="Concreto_Piso"
)

# --- Escultura central con blender_arch ---
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_base,
    depth=alto_fuente,
    location=(0, 0, alto_fuente / 2)
)
base_escultura = bpy.context.active_object
A.asignar_material(base_escultura, "Acero_Inox")

# --- Esferas con bpy ---
for i in range(num_esferas):
    angulo_rad = i * (2 * 3.14159 / num_esferas)
    x = radio_esfera * np.cos(angulo_rad)
    y = radio_esfera * np.sin(angulo_rad)
    
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=radio_esfera,
        location=(x, y, distancia_z_esfera)
    )
    esfera = bpy.context.active_object
    A.asignar_material(esfera, "Acero_Inox")

# --- Luces sumergidas con bpy ---
for i in range(4):
    angulo_rad = i * (2 * 3.14159 / 4)
    x = radio_esfera * np.cos(angulo_rad) + 1.5
    y = radio_esfera * np.sin(angulo_rad) + 1.5
    
    bpy.ops.light.add_type('POINT', radius=1.0)
    luz = bpy.context.active_object
    luz.location = (x, y, altura_luz_sumergida)
    A.asignar_material(luz.data, "Luz_Amarilla")
    luz.data.energy = 150