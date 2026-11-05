import bpy

def crear_panel(nombre, dimensiones, ubicacion):
    bpy.ops.mesh.primitive_cube_add(size=1, location=ubicacion)
    panel = bpy.context.active_object
    panel.name = nombre
    panel.dimensions = dimensiones
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return panel

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# --- Dimensiones ---
ancho_total = 1.2
alto_total = 2.0
profundidad_total = 0.3
grosor_madera = 0.03
num_baldas = 5

# --- Creación de componentes ---
componentes = []

# Paneles laterales
dimensiones_lateral = (grosor_madera, profundidad_total, alto_total)
panel_izq = crear_panel('Lateral_Izq', dimensiones_lateral, (-(ancho_total/2 - grosor_madera/2), 0, alto_total/2))
panel_der = crear_panel('Lateral_Der', dimensiones_lateral, ( (ancho_total/2 - grosor_madera/2), 0, alto_total/2))
componentes.extend([panel_izq, panel_der])

# Panel trasero
dimensiones_trasero = (ancho_total, grosor_madera, alto_total)
panel_trasero = crear_panel('Trasero', dimensiones_trasero, (0, -(profundidad_total/2 - grosor_madera/2), alto_total/2))
componentes.append(panel_trasero)

# Baldas
ancho_balda = ancho_total - 2 * grosor_madera
dimensiones_balda = (ancho_balda, profundidad_total - grosor_madera, grosor_madera)
espacio_entre_baldas = alto_total / (num_baldas - 1)

for i in range(num_baldas):
    z = (i * espacio_entre_baldas) - (espacio_entre_baldas/2) if i > 0 else 0 # Ajuste para balda inferior
    if i == num_baldas - 1:
        z = alto_total - grosor_madera/2 # Balda superior
    elif i == 0:
        z = grosor_madera/2 # Balda inferior
    else:
        z = (alto_total / (num_baldas-1)) * i

    z_pos = (alto_total / (num_baldas + 1)) * (i + 1)
    balda = crear_panel(f'Balda_{i+1}', dimensiones_balda, (0, grosor_madera/2, (alto_total / (num_baldas-1)) * i if i < num_baldas -1 else alto_total-grosor_madera/2))
    if i == 0: balda.location.z = grosor_madera/2
    componentes.append(balda)

# --- Agrupar objeto ---
for obj in bpy.data.objects:
    obj.select_set(False)

for comp in componentes:
    comp.select_set(True)

bpy.context.view_layer.objects.active = componentes[0]
bpy.ops.object.join()
estanteria = bpy.context.active_object
estanteria.name = 'Estanteria'