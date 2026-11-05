import blender_arch as A

A.limpiar_escena()

# Crear la base de la habitación
habitacion = A.crear_habitacion(
    nombre="Sala_Estar",
    ancho=6.0,
    fondo=4.5,
    alto=2.8,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Colocar un sofá grande contra la pared izquierda
sofa = A.crear_sofa(
    nombre="Sofa_Principal",
    ancho=3.0,
    origen=(1.5, 0.2, 0),
    material="Tela_Beige"
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

# Aplicar modificadores para darle forma
mod_bevel = estanteria.modifiers.new(name='Bevel', type='BEVEL')
mod_bevel.width = 0.01
mod_bevel.segments = 3

mod_array_x = estanteria.modifiers.new(name='Array_X', type='ARRAY')
mod_array_x.count = 2
mod_array_x.relative_offset_displace[0] = 1.0

mod_array_z = estanteria.modifiers.new(name='Array_Z', type='ARRAY')
mod_array_z.count = 2
mod_array_z.relative_offset_displace[2] = 1.0