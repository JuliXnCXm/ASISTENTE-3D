import blender_arch as A
A.limpiar_escena()

# Crear la habitación base
hab = A.crear_habitacion(
    nombre="Salon",
    ancho=4.5, fondo=4.0, alto=2.8,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Mobiliario
sofa = A.crear_sofa(
    nombre="Sofa_Principal",
    ancho=2.5, fondo=0.9, origen=(1.5, 0.2, 0),
    material="Tela_Beige"
)
mueble_tv = A.crear_mesa(
    nombre="Mueble_TV",
    ancho=1.2, fondo=0.3, alto=0.4,
    origen=(1.5, 3.5, 0),
    material_tablero="Madera_Roble"
)
estanteria = A.crear_estanteria(
    nombre="Estanteria_Nichos",
    ancho=1.8, alto=2.2, fondo=0.3,
    num_estantes=5, origen=(0.2, 0.2, 0),
    material="Hormigon"
)

# Modificadores para nichos
for i in range(3):
    # Nicho izquierdo
    mod = estanteria.modifiers.new(name=f"BooleanNicho_{i}", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = A.crear_caja(f"Nicho_Izq_{i}", ancho=0.1, fondo=0.3, alto=0.4, origen=(-0.05 + i*0.6, 0.2, 0), material="MDF_Blanco")
    mod.object.location.z = 0.2
    
    # Nicho derecho
    mod = estanteria.modifiers.new(name=f"BooleanNicho_{i}_D", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = A.crear_caja(f"Nicho_Der_{i}", ancho=0.1, fondo=0.3, alto=0.4, origen=(0.05 + i*0.6, 0.2, 0), material="MDF_Blanco")
    mod.object.location.z = 0.2

A.agregar_luz("Luz_Salon", tipo="AREA", ubicacion=(2.25, 2.0, 2.7), energia=250)