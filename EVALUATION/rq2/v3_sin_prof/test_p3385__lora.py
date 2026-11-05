import blender_arch as A
A.limpiar_escena()

# --- Parámetros ---
ancho_total = 5.5
fondo_total = 10.0
alto_piso = 2.8

# --- Materiales ---
mat_muro = "Muro_Pintura"
mat_suelo = "Parquet"
mat_madera = "Madera_Roble"
mat_marco = "Marco_Negro"

# --- Estructura y Pisos ---
A.crear_habitacion(
    nombre="Apartamento",
    ancho=ancho_total,
    fondo=fondo_total,
    alto=alto_piso,
    grosor_muro=0.2,
    material_muro=mat_muro,
    material_suelo=mat_suelo,
    origen=(0, 0, 0)
)

# --- Zona de Entrada y Sala-Comedor ---
A.crear_pared("Pared_Sala", largo=ancho_total, alto=alto_piso, origen=(0, 6.0, 0), material=mat_muro)
A.crear_pared("Pared_Fondo_Sala", largo=fondo_total, alto=alto_piso, origen=(0, 0, 0), material=mat_muro)
A.crear_pared("Pared_Derecha_Sala", largo=fondo_total, alto=alto_piso, origen=(ancho_total, 0, 0), material=mat_muro)
A.crear_pared("Pared_Izquierda_Sala", largo=fondo_total, alto=alto_piso, origen=(0, 0, 0), rotacion_z=-90, material=mat_muro)
A.crear_piso("Suelo_Sala", ancho=ancho_total, fondo=fondo_total, espesor=0.05, origen=(0, 0, 0))
A.crear_ventana("Ventana_Sala", ancho=2.0, alto=1.2, prof_marco=0.2, origen=(ancho_total/2, 0.2, 1.0), material_marco=mat_marco, material_vidrio="Vidrio")

# --- Zona Cocina ---
A.crear_pared("Pared_Cocina", largo=3.0, alto=alto_piso, origen=(ancho_total, 0, 0), material=mat_muro)
A.crear_pared("Pared_Cocina_Dos", largo=3.0, alto=alto_piso, origen=(ancho_total + 3.0, 0, 0), material=mat_muro)
A.crear_pared("Pared_Cocina_Tres", largo=3.0, alto=alto_piso, origen=(ancho_total + 3.0, 3.0, 0), rotacion_z=-90, material=mat_muro)
A.crear_piso("Suelo_Cocina", ancho=3.0, fondo=3.0, espesor=0.05, origen=(ancho_total, 0, 0))

# --- Barra de Cocina ---
A.crear_barra("Barra_Cocina", ancho=1.2, alto=0.9, origen=(ancho_total + 3.0, 1.5, 0), material_tablero=mat_madera, material_patas="Metal")

# --- Pasillo ---
A.crear_piso("Suelo_Pasillo", ancho=1.5, fondo=1.5, espesor=0.05, origen=(ancho_total, 7.5, 0))
A.crear_pared("Pared_Pasillo_1", largo=1.5, alto=alto_piso, origen=(ancho_total, 7.5, 0), material=mat_muro)
A.crear_pared("Pared_Pasillo_2", largo=1.5, alto=alto_piso, origen=(ancho_total, 7.5, 0), rotacion_z=-90, material=mat_muro)

# --- Zona Privada ---
A.crear_piso("Suelo_Bano", ancho=2.5, fondo=2.0, espesor=0.05, origen=(ancho_total + 1.5, 7.5, 0))
A.crear_piso("Suelo_Dormitorio", ancho=4.0, fondo=4.0, espesor=0.05, origen=(ancho_total + 1.5, 3.0, 0))
A.crear_pared("Pared_Bano", largo=2.5, alto=alto_piso, origen=(ancho_total + 1.5, 7.5, 0), material=mat_muro)
A.crear_pared("Pared_Bano_Dos", largo=2.5, alto=alto_piso, origen=(ancho_total + 1.5, 7.5, 0), rotacion_z=-90, material=mat_muro)
A.crear_pared("Pared_Dormitorio", largo=4.0, alto=alto_piso, origen=(ancho_total + 1.5, 3.0, 0), material=mat_muro)
A.crear_pared("Pared_Dormitorio_Dos", largo=4.0, alto=alto_piso, origen=(ancho_total + 1.5, 3.0, 0), rotacion_z=-90, material=mat_muro)

# --- Armario ---
A.crear_armario("Armario_Dormitorio", ancho=2.5, alto=2.4, fondo=0.6, origen=(ancho_total + 1.5, 3.0, 0), material_cuerpo=mat_madera)