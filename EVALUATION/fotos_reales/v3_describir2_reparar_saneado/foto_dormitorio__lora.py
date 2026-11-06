import blender_arch as A

A.limpiar_escena()

# --- ESTRUCTURA Y MUEBLES ---
habitacion = A.crear_habitacion(
    nombre="HabitacionHotel",
    ancho=4.0,
    fondo=5.0,
    alto=2.8,
    material_muro="Muro_Pintura",
    material_suelo="Parquet"
)

# --- CAMAS INDIVIDUALES ---
cama1 = A.crear_cama(
    nombre="CamaPrincipal",
    ancho=1.6,
    largo=2.0,
    origen=(1.2, 1.0, 0),
    material_colchon="Textil_Blanco",
    material_base="Madera_Roble"
)
cama2 = A.crear_cama(
    nombre="CamaSecundaria",
    ancho=1.4,
    largo=2.0,
    origen=(0.3, 1.0, 0),
    material_colchon="Textil_Blanco",
    material_base="Madera_Roble"
)

# --- MUEBLES DE NOCHE ---
mesa_noche1 = A.crear_mesa(
    nombre="MesaNochePrincipal",
    ancho=0.5,
    fondo=0.5,
    alto=0.6,
    origen=(1.2 + 0.5/2 - 0.05, 0.3, 0),
    material_tablero="Madera_Roble"
)
mesa_noche2 = A.crear_mesa(
    nombre="MesaNocheSecundaria",
    ancho=0.5,
    fondo=0.5,
    alto=0.6,
    origen=(0.3 + 0.5/2 - 0.05, 0.3, 0),
    material_tablero="Madera_Roble"
)

# --- ILUMINACION ---
for i in range(2):
    A.agregar_luz(
        nombre=f"Luz{i+1}",
        tipo="POINT",
        ubicacion=(1.2 + 0.5/2, 0.3 + 0.5/2, 2.5),
        energia=150 if i==0 else 100,
        color=(1, 0.9, 0.8)
    )
    A.agregar_luz(
        nombre=f"Luz{i+1}_Techo",
        tipo="POINT",
        ubicacion=(1.2 + 0.5/2, 0.3 + 0.5/2, 2.7),
        energia=150 if i==0 else 100,
        color=(1, 0.9, 0.8)
    )

# --- VENTANAS ---
ventana1 = A.crear_ventana(
    nombre="VentanaPrincipal",
    ancho=2.0,
    alto=1.2,
    prof_marco=0.2,
    origen=(1.0, 0.1, 1.1),
    material_marco="Marco_Aluminio",
    material_vidrio="Vidrio"
)
ventana2 = A.crear_ventana(
    nombre="VentanaSecundaria",
    ancho=1.5,
    alto=1.2,
    prof_marco=0.2,
    origen=(0.5, 0.1, 1.1),
    material_marco="Marco_Aluminio",
    material_vidrio="Vidrio"
)

# --- PAREDES ---
pared1 = A.crear_muro("ParedIzquierda", largo=4.0, alto=2.8, origen=(0, 0, 0), rotacion_z=0)
pared2 = A.crear_muro("ParedDerecha", largo=4.0, alto=2.8, origen=(4.0, 0, 0), rotacion_z=0)
pared3 = A.crear_muro("ParedFondo", largo=5.0, alto=2.8, origen=(0, 5.0, 0), rotacion_z=-90)
pared4 = A.crear_muro("ParedFrontal", largo=5.0, alto=2.8, origen=(0, 0, 0), rotacion_z=90)