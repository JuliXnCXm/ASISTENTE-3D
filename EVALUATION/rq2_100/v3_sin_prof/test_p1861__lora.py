import blender_arch as A
A.limpiar_escena()

# Crear la habitación base
hab = A.crear_habitacion(
    nombre="Salon",
    ancho=6.0,
    fondo=4.0,
    alto=2.8,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Muebles
sofa = A.crear_sofa(
    nombre="Sofa_Principal",
    ancho=2.5,
    origen=(1.75, 0.2, 0),
    material="Tela_Beige"
)

mueble_tv = A.crear_mesa(
    nombre="Mueble_TV",
    ancho=1.2,
    fondo=0.3,
    alto=0.4,
    origen=(2.4, 3.5, 0),
    material_tablero="Madera_Roble"
)

estanteria = A.crear_estanteria(
    nombre="Estanteria_Nichos",
    ancho=1.8,
    alto=2.2,
    fondo=0.3,
    num_estantes=5,
    origen=(0.1, 0.1, 0),
    material="Hormigon"
)

# Modificadores para nichos
for i in range(5):
    # Crear un objeto de corte
    corte = A.crear_prisma(
        nombre=f"Corte_Nicho_{i}",
        ancho=0.3,
        alto=2.2,
        fondo=0.3,
        origen=(0.1 + 0.3*i, 0.1, 0),
        material="Hormigon"
    )
    
    # Aplicar modificador booleano
    mod = estanteria.modifiers.new(name=f"Boolean_Nicho_{i}", type='BOOLEAN')
    mod.object = corte
    mod.operation = 'DIFFERENCE'
    bpy.context.view_layer.objects.active = estanteria
    bpy.ops.object.modifier_apply(modifier=mod.name)
    A.asignar_material(corte, "Hormigon", base_color=(0.2, 0.2, 0.2, 1))

# Iluminación y cámara
A.agregar_luz("Luz_Salon", tipo="AREA", ubicacion=(3, 2, 2.7), energia=500)
A.crear_camara("Camara_Salon", ubicacion=(-2, -3, 2), rotacion=(70, 0, 0))