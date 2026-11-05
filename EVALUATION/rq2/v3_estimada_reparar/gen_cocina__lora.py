import blender_arch as A

A.limpiar_escena()

# Crear la estructura de la cocina
A.crear_habitacion(
    nombre="Cocina",
    ancho=4.0,
    fondo=3.0,
    alto=2.8,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Porcelanato"
)

# Mesón en L
meson_largo = 3.0
meson_ancho = 1.5
meson_alto = 0.9
meson_x = (4.0 - meson_largo) / 2
meson_y = (3.0 - meson_ancho) / 2

A.crear_losa_rectangular(
    nombre="Meson_Largo",
    ancho=meson_largo,
    fondo=meson_ancho,
    espesor=0.04,
    origen=(meson_x, meson_y, meson_alto),
    material="MDF_Blanco"
)
A.crear_losa_rectangular(
    nombre="Meson_Corto",
    ancho=meson_ancho,
    fondo=meson_largo - meson_ancho,
    espesor=0.04,
    origen=(meson_x + meson_largo - meson_ancho, meson_y, meson_alto),
    material="MDF_Blanco"
)

# Mesa de centro
mesa_ancho = 1.2
mesa_fondo = 0.7
mesa_alto = 0.75
mesa_x = 1.0
mesa_y = 1.5
A.crear_mesa(
    nombre="Mesa_Centro",
    ancho=mesa_ancho,
    fondo=mesa_fondo,
    alto=mesa_alto,
    origen=(mesa_x, mesa_y, 0),
    material_tablero="Madera_Roble"
)

# Sillas
silla_origen_x = 0.6
silla_origen_y = 0.6
for i in range(4):
    silla_x = silla_origen_x + i * (mesa_ancho / 3)
    silla_y = silla_origen_y
    A.crear_silla(
        nombre=f"Silla_{i+1}",
        origen=(silla_x, silla_y, 0),
        material="Cuero"
    )

# Ventana
ventana_ancho = 1.5
ventana_alto = 1.2
ventana_origen_x = 1.0
ventana_origen_y = 0.5
A.crear_ventana(
    nombre="Ventana_Cocina",
    ancho=ventana_ancho,
    alto=ventana_alto,
    prof_marco=0.1,
    origen=(ventana_origen_x, ventana_origen_y, 1.0),
    material_marco="Marco_Negro",
    material_vidrio="Vidrio"
)