import blender_arch as A

A.limpiar_escena()

# Parámetros de la fachada
num_plantas = 5
ancho_modulo = 4.0
alto_modulo = 2.8
grosor_muro = 0.3
ancho_losa = 0.3
espesor_baranda = 0.1
ancho_puerta = 2.0
alto_puerta = 2.1

# Crear muros y cubierta
muro_fachada = A.crear_muro(
    nombre="Muro_Fachada",
    largo=num_plantas * ancho_modulo,
    alto=num_plantas * alto_modulo + grosor_muro,
    grosor=grosor_muro,
    origen=(0, 0, 0),
    material="Estuco"
)

losa_cubierta = A.crear_losa_rectangular(
    nombre="Losa_Cubierta",
    ancho=num_plantas * ancho_modulo,
    fondo=ancho_losa,
    espesor=0.2,
    origen=(0, -ancho_losa/2, num_plantas * alto_modulo),
    material="Hormigon"
)

# Crear balcón y barandilla para cada módulo
for i in range(num_plantas):
    for j in range(4):
        # Coordenadas del módulo
        x = j * ancho_modulo
        z = i * alto_modulo
        
        # Crear balcón
        balcón = A.crear_losa_rectangular(
            nombre=f"Balcon_{i}_{j}",
            ancho=ancho_modulo,
            fondo=ancho_losa,
            espesor=0.2,
            origen=(x, -ancho_losa/2, z + grosor_muro),
            material="Madera_Roble"
        )
        
        # Crear barandilla
        baranda = A.crear_baranda_lineal(
            nombre=f"Baranda_{i}_{j}",
            largo=ancho_modulo,
            altura=espesor_baranda,
            poste_cada=1.0,
            origen=(x, -ancho_losa/2, z + grosor_muro + 0.2),
            material="Vidrio"
        )

# Crear puertas correderas
for i in range(num_plantas):
    for j in range(4):
        # Coordenadas del módulo
        x = j * ancho_modulo
        z = i * alto_modulo
        
        # Crear puerta
        puerta = A.crear_puerta(
            nombre=f"Puerta_{i}_{j}",
            ancho=ancho_puerta,
            alto=alto_puerta,
            prof_marco=grosor_muro,
            origen=(x + ancho_modulo/2 - ancho_puerta/2, 0, z + grosor_muro),
            material_panel="Vidrio_Templado",
            material_marco="Marco_Negro"
        )