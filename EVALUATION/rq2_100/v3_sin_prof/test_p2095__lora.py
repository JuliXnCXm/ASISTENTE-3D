import blender_arch as A
A.limpiar_escena()

# Crear la base de la habitación
habitacion = A.crear_habitacion(
    nombre="Sala_Estar",
    ancho=6.0,
    fondo=4.5,
    alto=2.8,
    material_muro="Estuco",
    material_suelo="Porcelanato"
)

# Colocar un sofá grande contra la pared del fondo
sofa = A.crear_sofa(
    nombre="Sofa_Principal",
    ancho=3.0,
    origen=(1.5, 0.2, 0),
    material="Tela_Gris"
)

# Colocar una alfombra en el suelo
alfombra = A.crear_alfombra(
    nombre="Alfombra_Sala",
    ancho=2.5,
    fondo=1.8,
    origen=(1.75, 1.5, 0),
    material="Textil_Blanco"
)

# Crear una estantería de diseño irregular
estanteria = A.crear_estanteria(
    nombre="Estanteria_Diseño",
    ancho=2.0,
    alto=2.2,
    fondo=0.3,
    num_estantes=5,
    origen=(-1.0, 2.0, 0),
    material="Madera_Roble"
)

# Aplicar modificadores para darle forma irregular
for i in range(5):
    estanteria.modifiers.new(name=f"Displace_{i}", type='DISPLACE')
    estanteria.modifiers["Displace_" + str(i)].texture = A.crear_textura_ruido(
        nombre=f"Ruido_{i}",
        tamaño=0.1,
        valor_maximo=0.05,
        origen=(i * 0.2, 0, 0)
    )
    estanteria.modifiers["Displace_" + str(i)].stiffness = 0.05

# Añadir iluminación y cámara
A.agregar_luz(nombre="Luz_Principal", tipo="AREA", ubicacion=(3, 2.25, 2.7), energia=250)
A.crear_camara(nombre="Camara_Sala", ubicacion=(3, -3, 2.5), rotacion=(75, 0, 0))