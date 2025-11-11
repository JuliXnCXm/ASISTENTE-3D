import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la estantería ---
alto_total = 2.0
ancho_total = 1.2
fondo_total = 0.3
espesor_madera = 0.03
numero_baldas = 5

# --- Función para crear un panel ---
def crear_panel(nombre, escala, localizacion):
    bpy.ops.mesh.primitive_cube_add(size=1, location=localizacion)
    panel = bpy.context.active_object
    panel.name = nombre
    panel.scale = escala
    return panel

# --- Creación de los componentes ---
# Lateral izquierdo
escala_lateral = (espesor_madera, fondo_total, alto_total)
loc_izquierdo = (-ancho_total / 2 + espesor_madera / 2, 0, alto_total / 2)
crear_panel("LateralIzquierdo", escala_lateral, loc_izquierdo)

# Lateral derecho
loc_derecho = (ancho_total / 2 - espesor_madera / 2, 0, alto_total / 2)
crear_panel("LateralDerecho", escala_lateral, loc_derecho)

# Creación de las baldas
ancho_balda = ancho_total - (2 * espesor_madera)
escala_balda = (ancho_balda, fondo_total, espesor_madera)
espacio_entre_baldas = alto_total / (numero_baldas - 1)

for i in range(numero_baldas):
    z_pos = (i * espacio_entre_baldas) - (i/(numero_baldas-1) * espesor_madera) if numero_baldas > 1 else espesor_madera/2
    z_pos = min(z_pos, alto_total - espesor_madera/2)
    if i == 0: z_pos = espesor_madera/2
    loc_balda = (0, 0, z_pos)
    crear_panel(f"Balda_{i+1}", escala_balda, loc_balda)