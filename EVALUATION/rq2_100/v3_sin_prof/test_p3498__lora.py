import blender_arch as A
A.limpiar_escena()

# Edificio de oficinas con fachada de vidrio
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioApartamentos",
    pisos=5,
    ancho=16.0,
    fondo=12.0,
    alto_piso=3.0,
    grosor_muro=0.3,
    con_techo_plano=True,
    con_columnas=False,
    material_fachada="Estuco",
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio",
    origen=(0, 0, 0)
)

# Crear balcones y puertas en los huecos
for p in range(5):
    for i in range(4):
        # Coordenadas del hueco
        x = i * 4.0 + 0.15
        y = p * 3.0 + 0.15
        z = 2.8
        
        # Crear balcón
        A.crear_losa_rectangular(f"Balcon_{p}_{i}", ancho=4.0, fondo=1.0, espesor=0.2, origen=(x, y, z), material="Hormigon")
        
        # Crear barandilla de vidrio
        A.crear_losa_rectangular(f"VidrioBarandilla_{p}_{i}", ancho=4.0, fondo=0.1, espesor=0.02, origen=(x, y + 0.95, z + 0.2), material="Vidrio_Templado")
        
        # Crear puerta corredera
        A.crear_losa_rectangular(f"PuertaCorredera_{p}_{i}", ancho=1.0, fondo=2.2, espesor=0.02, origen=(x + 0.2, y, z), material="Vidrio_Templado")