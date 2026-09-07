import blender_arch as A
import bpy

A.limpiar_escena()

# --- ESTRUCTURA ---
habitacion = A.crear_habitacion(
    'Dormitorio', ancho=4.5, fondo=6.0, alto=2.7,
    material_muro='Muro_Pintura', material_suelo='Madera'
)

# --- CAMA Y MESITAS (usando blender_arch y bpy) ---
cama = A.crear_cama(
    'CamaPrincipal', ancho=1.8, largo=2.0, alto_cabecero=0.0, # Cabecero se hará con bpy
    origen=(0, -1.9, 0), 
    material_colchon='Textil_Blanco', material_base='Madera_Nogal'
)

# Cabecero tapizado personalizado con bpy
bpy.ops.mesh.primitive_cube_add(location=(0, -2.95, 0.6))
cabecero = bpy.context.active_object
cabecero.name = 'Cabecero'
cabecero.scale = (1.4, 0.05, 0.6)
bpy.ops.object.transform_apply(scale=True)
A.asignar_material(cabecero, nombre='Tela_Acolchada', base_color=(0.2, 0.25, 0.3, 1))

# Añadir detalle de botones (tufting)
for y in [-0.5, 0.5]:
    for z in [0.4, 0.8]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.02, location=(0, -2.99, z), rotation=(0, 1.57, 0))
        btn = bpy.context.active_object
        btn.scale.x = 0.2
        A.asignar_material(btn, nombre='Tela_Acolchada')
        btn.location[0] = y

# Mesitas de noche
A.crear_mesa('Mesita_Izq', ancho=0.5, fondo=0.4, alto=0.5, origen=(-1.25, -2.75, 0), material_tablero='Madera_Nogal')
A.crear_mesa('Mesita_Der', ancho=0.5, fondo=0.4, alto=0.5, origen=(1.25, -2.75, 0), material_tablero='Madera_Nogal')

# --- MURO SEPARADOR VESTIDOR (usando blender_arch) ---
muro_separador = A.crear_muro(
    'MuroSeparador', largo=4.5, alto=1.5, grosor=0.15,
    origen=(-2.25, 0.5, 0), material='Muro_Pintura'
)

# --- ARMARIOS VESTIDOR (usando blender_arch) ---
A.crear_armario(
    'Armario_1', ancho=2.0, alto=2.7, fondo=0.6, num_puertas=3,
    origen=(-2.15, 2.7, 0), material_cuerpo='MDF_Blanco'
)
A.crear_armario(
    'Armario_2', ancho=2.0, alto=2.7, fondo=0.6, num_puertas=3,
    origen=(0.15, 2.7, 0), material_cuerpo='MDF_Blanco'
)

# --- ILUMINACIÓN Y CÁMARA ---
A.agregar_luz('Luz_Dormitorio', tipo='AREA', ubicacion=(0, 0, 2.5), energia=200)
A.agregar_luz('Luz_Vestidor', tipo='POINT', ubicacion=(0, 2.0, 2.0), energia=100)
A.crear_camara('CamaraDormitorio', ubicacion=(-4, -4, 2), rotacion=(75, 0, -45))