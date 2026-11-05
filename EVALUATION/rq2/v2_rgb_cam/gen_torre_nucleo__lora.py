import blender_arch as A

A.limpiar_escena()

# --- ESTRUCTURA ---
A.crear_torre_n_pisos(
    nombre="TorreOficina",
    pisos=20,
    ancho=30.0,
    fondo=30.0,
    alto_piso=3.5,
    grosor_muro=0.3,
    con_columnas=True,
    dim_columna=0.4,
    modulo_columna_x=5.0,
    modulo_columna_y=5.0,
    origen=(0, 0, 0),
    material_muro="Hormigon",
    material_losa="Hormigon",
    material_columna="Hormigon"
)

# --- MATERIALES ---
mat_vidrio = "Vidrio_Templado"
mat_marco = "Marco_Aluminio"

# --- VENTANAS ---
for i in range(1, 20):
    for j in range(1, 19):
        x = -15 + (j * 5) + 0.2
        y = -15 + (i * 5) + 0.2
        A.crear_ventana(
            nombre=f"Ventana_{i}_{j}",
            ancho=2.8,
            alto=2.2,
            prof_marco=0.2,
            origen=(x, y, 2.5),
            material_marco=mat_marco,
            material_vidrio=mat_vidrio
        )

# --- ILUMINACION Y CAMARA ---
A.agregar_luz(nombre="LuzSol", tipo="SUN", ubicacion=(-10, -10, 25), energia=3)
A.crear_camara(nombre="CamaraFrontal", ubicacion=(0, -20, 10), rotacion=(80, 0, 0))