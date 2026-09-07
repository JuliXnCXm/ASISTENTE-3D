import blender_arch as A
import bpy
import math

# --- Inicio del script ---
A.limpiar_escena()

# 1. Definir niveles
altura_desnivel = 2.4
mat_hormigon = "Hormigon"
mat_piso = "Concreto_Piso"

losa_inferior = A.crear_losa_rectangular("LosaBaja", 20, 10, 0.3, origen=(0, -5, -0.15), material=mat_piso)
losa_superior = A.crear_losa_rectangular("LosaAlta", 20, 10, 0.3, origen=(0, 10, altura_desnivel-0.15), material=mat_piso)

# 2. Escalinata central con bpy
ancho_escalera = 6.0
num_peldanos = 14
huella = (10.0 + 5.0) / num_peldanos
contrahuella = altura_desnivel / num_peldanos

bpy.ops.mesh.primitive_cube_add(size=1, location=(-ancho_escalera/2 + ancho_escalera/2, 0, contrahuella/2))
escalon = bpy.context.active_object
escalon.name = "EscalonBase"
escalon.scale = (ancho_escalera, huella, contrahuella)
bpy.ops.object.transform_apply(scale=True)
A.asignar_material(escalon, nombre=mat_piso)

mod = escalon.modifiers.new(name='Array', type='ARRAY')
mod.count = num_peldanos
mod.relative_offset_displace[0] = 0
mod.relative_offset_displace[1] = 1
mod.relative_offset_displace[2] = 1

# 3. Rampas de accesibilidad
ancho_rampa = 2.0
pendiente = 0.08
largo_rampa_plano = altura_desnivel / pendiente
angulo_rampa = math.atan(pendiente)

def crear_rampa(nombre, origen, rotacion_z):
    # Tramo inclinado
    bpy.ops.mesh.primitive_plane_add(size=1, location=(origen[0], origen[1], origen[2]))
    rampa = bpy.context.active_object
    rampa.name = nombre
    rampa.rotation_euler = (angulo_rampa, 0, math.radians(rotacion_z))
    rampa.dimensions = (largo_rampa_plano, ancho_rampa, 0)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    rampa.location.z = origen[2] + largo_rampa_plano * math.sin(angulo_rampa) / 2
    mod_solid = rampa.modifiers.new(name='Solidify', type='SOLIDIFY')
    mod_solid.thickness = 0.2
    A.asignar_material(rampa, nombre=mat_piso)
    return rampa

# Rampas y descansillos (simplificado a un tramo)
crear_rampa("RampaIzquierda", (-ancho_escalera/2 - ancho_rampa/2 - 1, 2.5, 0), 0).location.y = -2.5
crear_rampa("RampaDerecha", (ancho_escalera/2 + ancho_rampa/2 + 1, 2.5, 0), 0).location.y = -2.5


# 4. Jardineras laterales
jardinera_alto = 1.0
jardinera_grosor = 0.4
jardinera_largo = 15.0
jardinera_ancho = 2.5
pos_x_jardinera = ancho_escalera/2 + ancho_rampa + 1.5 + jardinera_ancho/2

contorno = [(-jardinera_largo/2, -jardinera_ancho/2), (jardinera_largo/2, -jardinera_ancho/2), (jardinera_largo/2, jardinera_ancho/2), (-jardinera_largo/2, jardinera_ancho/2)]
agujero = [(-jardinera_largo/2+jardinera_grosor, -jardinera_ancho/2+jardinera_grosor), (jardinera_largo/2-jardinera_grosor, -jardinera_ancho/2+jardinera_grosor), (jardinera_largo/2-jardinera_grosor, jardinera_ancho/2-jardinera_grosor), (-jardinera_largo/2+jardinera_grosor, jardinera_ancho/2-jardinera_grosor)]

jardinera_izq = A.extruir_con_huecos("JardineraIzq", contorno, [agujero], altura=jardinera_alto, material=mat_hormigon)
jardinera_izq.location = (-pos_x_jardinera, 2.5, 0)
jardinera_der = A.extruir_con_huecos("JardineraDer", contorno, [agujero], altura=jardinera_alto, material=mat_hormigon)
jardinera_der.location = (pos_x_jardinera, 2.5, 0)

# 5. Vegetación en jardineras
for i in range(5):
    offset_x = -jardinera_largo/2 + 1.5 + i * 3
    A.crear_arbol_simple(f"ArbolJardineraIzq_{i}", radio_copa=0.8, altura_copa=1, altura_tronco=0.5, origen=(-pos_x_jardinera + offset_x, 2.5, jardinera_alto))
    A.crear_arbol_simple(f"ArbolJardineraDer_{i}", radio_copa=0.8, altura_copa=1, altura_tronco=0.5, origen=(pos_x_jardinera + offset_x, 2.5, jardinera_alto))

# 6. Iluminación de piso
for i in range(8):
    y = -4 + i * 2
    A.agregar_luz(f"LuzPiso_{i}", tipo="POINT", ubicacion=(-ancho_escalera/2-0.5, y, 0.1), energia=50, color=(1, 0.8, 0.5))
    A.agregar_luz(f"LuzPiso_{i+8}", tipo="POINT", ubicacion=(ancho_escalera/2+0.5, y, 0.1), energia=50, color=(1, 0.8, 0.5))

# 7. Contexto y cámara
A.crear_muro("FachadaFondo", 20, 5, 0.3, origen=(-10, 15, altura_desnivel), material="Muro_Pintura_Gris")
A.agregar_luz("LuzRelleno", tipo="SUN", ubicacion=(10, -20, 15), energia=2)
A.crear_camara("CamaraAcceso", ubicacion=(0, -18, 5), rotacion=(80, 0, 0), activa=True, focal_length=28)