import blender_arch as A
import bpy

A.limpiar_escena()

# --- Materiales ---
mat_muro = "Estuco"
mat_losa = "Hormigon"
mat_vidrio = "Vidrio_Templado"
mat_madera = "Madera_Roble"

# --- Parámetros ---
ancho_edificio = 10.0
alto_piso = 3.2
num_pisos = 2
grosor_muro = 0.3
retranqueo = 0.5
ancho_losa = ancho_edificio - (2 * grosor_muro)

# --- Crear losas ---
losa_p1 = A.crear_losa_rectangular("Losa_P1", ancho=ancho_losa, fondo=10, espesor=0.2, origen=(0, 0, 0), material=mat_losa)
losa_p2 = A.crear_losa_rectangular("Losa_P2", ancho=ancho_losa, fondo=10, espesor=0.2, origen=(0, 0, alto_piso), material=mat_losa)

# --- Crear muros ---
muro_fachada = A.crear_muro("Muro_Fachada", largo=ancho_edificio, alto=alto_piso*2, grosor=grosor_muro, origen=(0, -grosor_muro/2, 0), material=mat_muro)

# --- Entrada principal acristalada (Planta Baja) ---
ventana_pb = A.crear_ventana("Ventana_PB", ancho=2.5, alto=2.8, prof_marco=grosor_muro, divisiones=(1,1), origen=(-2.5, -grosor_muro/2, 0), material_marco=mat_muro, material_vidrio=mat_vidrio)
A.abrir_vanos_batch_rectangulares(muro_fachada, centros_world=[(-2.5, -grosor_muro/2, 1.4)], ancho=2.5, alto=2.8)

# --- Celosía de lamas (Planta Alta) ---
ancho_lama = 0.05
alto_lama = 2.8
num_lamas = int(ancho_edificio / ancho_lama)
separacion = 0.02

for i in range(num_pisos):
    z_pos = alto_piso + (i * alto_piso)
    
    # Lamas
    for j in range(num_lamas):
        x_pos = j * (ancho_lama + separacion)
        bpy.ops.mesh.primitive_cube_add(location=(x_pos, 0, z_pos))
        lama = bpy.context.active_object
        lama.name = f"Lama_{j}_{i}"
        lama.dimensions = (ancho_lama, 0.05, alto_lama)
        A.asignar_material(lama, nombre=mat_madera)
        
        # Aplicar modificador Array para repetir
        array_mod = lama.modifiers.new(name=f"Array_Lama_{j}", type='ARRAY')
        array_mod.count = num_pisos
        array_mod.relative_offset_displace[0] = 0
        array_mod.use_relative_offset = False
        array_mod.use_constant_offset = True
        array_mod.constant_offset_displace[0] = 0
        
    # Ventana trasera (Planta Alta)
    ventana_pa = A.crear_ventana(f"Ventana_PA_{i}", ancho=ancho_edificio - 2*grosor_muro, alto=2.8, prof_marco=grosor_muro, divisiones=(int((ancho_edificio-2*grosor_muro)/ancho_lama), 1), origen=(grosor_muro, -grosor_muro/2, z_pos), material_marco=mat_muro, material_vidrio=mat_vidrio)
    A.abrir_vanos_batch_rectangulares(muro_fachada, centros_world=[(grosor_muro, -grosor_muro/2, z_pos + 1.4)], ancho=ancho_edificio - 2*grosor_muro, alto=2.8)