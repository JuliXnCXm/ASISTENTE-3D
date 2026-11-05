import bpy
import blender_arch as A

A.limpiar_escena()

# 1. Base de la azotea
ancho, fondo = 12, 8
techo = A.crear_techo_plano("BaseAzotea", ancho=ancho, fondo=fondo, espesor=0.3, origen=(0,0,0), material="Hormigon")
parapeto1 = A.crear_muro("Parapeto1", largo=ancho, alto=1.0, grosor=0.2, origen=(-ancho/2, -fondo/2, 0.3), material="Estuco")
parapeto2 = A.crear_muro("Parapeto2", largo=fondo, alto=1.0, grosor=0.2, origen=(-ancho/2, -fondo/2, 0.3), material="Estuco")

# 2. Deck de madera
bpy.ops.mesh.primitive_cube_add(location=(-ancho/2 + 0.1, -fondo/2 + 3, 0.31))
liston = bpy.context.active_object
liston.name = "ListonDeck"
liston.scale = (0.1, 3, 0.02)
A.asignar_material(liston, "Madera")
mod_array_x = liston.modifiers.new(name="ArrayX", type='ARRAY')
mod_array_x.count = int((ancho-0.2)/0.11)
mod_array_x.relative_offset_displace[0] = 1.1

# 3. Jardineras perimetrales
jardinera1 = A.extruir_con_huecos("Jardinera1", contorno=[(0,0), (ancho,0), (ancho,1), (0,1)], agujeros=[[(0.1,0.1), (ancho-0.1,0.1), (ancho-0.1,0.9), (0.1,0.9)]], altura=0.6, material="Hormigon")
jardinera1.location = (-ancho/2, fondo/2 - 1, 0.3)

jardinera2 = A.extruir_con_huecos("Jardinera2", contorno=[(0,0), (1,0), (1,fondo), (0,fondo)], agujeros=[[(0.1,0.1), (0.9,0.1), (0.9,fondo-0.1), (0.1,fondo-0.1)]], altura=0.6, material="Hormigon")
jardinera2.location = (ancho/2 - 1, -fondo/2, 0.3)

# 4. Vegetación en jardineras
for i in range(10):
    x = -ancho/2 + 0.5 + i * 1.1
    y = fondo/2 - 0.5
    z = 0.3 + 0.6
    shrub = A.crear_arbol_simple(f"Arbusto1_{i}", radio_copa=0.4, altura_copa=0.5, altura_tronco=0.2, origen=(x,y,z))

for i in range(7):
    x = ancho/2 - 0.5
    y = -fondo/2 + 0.5 + i * 1.1
    z = 0.3 + 0.6
    shrub = A.crear_arbol_simple(f"Arbusto2_{i}", radio_copa=0.4, altura_copa=0.5, altura_tronco=0.2, origen=(x,y,z))


# 5. Pérgola de acero
for i in [0, 1]:
    for j in [0, 1]:
        x = -4 + i * 8
        y = -2 + j * 4
        poste = A.crear_columna(f"PostePergola_{i}{j}", seccion="rect", ancho=0.15, fondo=0.15, alto=2.5, origen=(x, y, 0.3), material="Marco_Negro")

viga1 = A.crear_losa_rectangular("Viga1", ancho=8.15, fondo=0.15, espesor=0.2, origen=(-4, -2, 0.3+2.5), material="Marco_Negro")
viga2 = A.crear_losa_rectangular("Viga2", ancho=8.15, fondo=0.15, espesor=0.2, origen=(-4, 2, 0.3+2.5), material="Marco_Negro")

for i in range(17):
    x = -4 + i * 0.5
    liston_pergola = A.crear_losa_rectangular(f"ListonPergola_{i}", ancho=0.08, fondo=4.3, espesor=0.15, origen=(x, -2.15, 0.3+2.5+0.2), material="Marco_Negro")

# 6. Mobiliario
sofa = A.crear_sofa("SofaExterior", origen=(0, 0, 0.3), material="Tela_Gris")
sofa.rotation_euler[2] = 1.5708 # 90 grados
mesa = A.crear_mesa("MesaExterior", ancho=1, fondo=0.6, alto=0.4, origen=(0, -1.5, 0.3), material_tablero="Madera_Nogal")

# 7. Iluminación y cámara
A.agregar_luz("LuzTerraza", tipo="SUN", ubicacion=(8, -10, 15), energia=6)
A.crear_camara("CamaraTerraza", ubicacion=(-12, -10, 8), rotacion=(65, 0, -50))