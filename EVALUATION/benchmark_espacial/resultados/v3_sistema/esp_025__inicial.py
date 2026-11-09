import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Oficinas",
    pisos=6,
    ancho=18.0,
    fondo=12.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_muro="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Balcon en la fachada oeste (Y+)
fachada_oeste = edificio.children[0].children[6] # Seleccionar el muro oeste del piso 4
A.extruir_con_huecos(fachada_oeste, 
    contorno=[(-18/2 + 0.25/2, -12/2 + 0.25/2), (-18/2 + 0.25/2, 12/2 - 0.25/2)], 
    agujeros=[[(-18/2, -12/2), (-18/2, 12/2)]], 
    altura=1.5
)

# Baranda simple en el nuevo hueco
baranda = A.crear_baranda_lineal("Baranda_Balcon", largo=18.0-0.5, altura=1.0, origen=(-9.25, -6.0, 3.0), material="Acero_Inox")
baranda.rotation_euler[2] = 1.5708 # 90 grados en Z

# Colocar balcón sobre la losa del piso 4
balcon = A.crear_losa_rectangular("Vigas_Balcon", ancho=18.0-0.5, fondo=3.0, espesor=0.2, origen=(-9.25, -6.0, 3.0))
balcon.rotation_euler[2] = 1.5708 # 90 grados en Z
balcon.parent = edificio
balcon.select_set(True)