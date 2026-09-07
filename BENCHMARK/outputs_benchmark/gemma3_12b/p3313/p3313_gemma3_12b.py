import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones generales
longitud_total = 20  # metros
ancho_total = 10  # metros
altura_desnivel = 3  # metros
ancho_escalera = 8  # metros
ancho_rampas = 3  # metros
altura_jardineras = 1.5  # metros
longitud_jardineras = 4  # metros
ancho_jardineras = 2  # metros

# --- Funciones de creación ---

def crear_escalera(longitud, ancho, altura_por_escalon, num_escalones):
    """Crea una escalera."""
    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    escalera = bpy.context.object
    escalera.name = "Escalera"
    escalera.scale = (1, ancho / 2, 1)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    escalera.data.name = "Escalera_Data"
    escalera.data.vertices.clear()
    escalera.data.edges.clear()
    escalera.data.faces.clear()

    for i in range(num_escalones):
        altura = i * altura_por_escalon
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, altura))
        escalon = bpy.context.object
        escalon.name = f"Escalon_{i}"
        escalon.scale = (1, ancho / 2, 1)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        escalon.data.name = f"Escalera_Data_{i}"
        escalon.data.vertices.clear()
        escalon.data.edges.clear()
        escalon.data.faces.clear()
        escalon.parent = escalera
        escalera.select_set(True)
        bpy.context.view_layer.objects.active = escalera
        bpy.ops.object.parent_set(type='OBJECT')
        escalera.select_set(False)

def crear_rampa(longitud, ancho, altura_total, num_segmentos):
    """Crea una rampa."""
    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    rampa = bpy.context.object
    rampa.name = "Rampa"
    rampa.scale = (1, ancho / 2, 1)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    rampa.data.name = "Rampa_Data"
    rampa.data.vertices.clear()
    rampa.data.edges.clear()
    rampa.data.faces.clear()

    altura_por_segmento = altura_total / num_segmentos
    for i in range(num_segmentos):
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, i * altura_por_segmento))
        segmento = bpy.context.object
        segmento.name = f"Segmento_Rampa_{i}"
        segmento.scale = (1, ancho / 2, 1)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        segmento.data.name = f"Rampa_Data_{i}"
        segmento.data.vertices.clear()
        segmento.data.edges.clear()
        segmento.data.faces.clear()
        segmento.parent = rampa
        rampa.select_set(True)
        bpy.context.view_layer.objects.active = rampa
        bpy.ops.object.parent_set(type='OBJECT')
        rampa.select_set(False)

def crear_jardinera(longitud, ancho, altura):
    """Crea una jardinera de hormigón."""
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    jardinera = bpy.context.object
    jardinera.name = "Jardinera"
    jardinera.scale = (longitud / 2, ancho / 2, altura / 2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    jardinera.data.name = "Jardinera_Data"
    return jardinera

def crear_iluminacion_piso(ubicacion):
    """Crea una luz de piso."""
    bpy.ops.object.light_add(type='POINT', radius=0.1, align='WORLD', location=ubicacion, scale=(1, 1, 1))
    luz = bpy.context.object
    luz.name = "Luz_Piso"
    luz.data.energy = 50  # Ajustar intensidad
    luz.data.use_color = True
    luz.data.color = (1, 0.8, 0.6)  # Color cálido
    return luz

# --- Creación de la escena ---

# Escalera
num_escalones = int(altura_desnivel / 0.2)
altura_por_escalon = altura_desnivel / num_escalones
crear_escalera(longitud_total, ancho_escalera, altura_por_escalon, num_escalones)
escalera = bpy.context.object

# Rampas
crear_rampa(longitud_total, ancho_rampas, altura_desnivel, int(altura_desnivel / 0.5))
rampa_izquierda = bpy.context.object
rampa_derecha = bpy.context.object

# Posicionar la escalera y las rampas
escalera.location = (longitud_total / 2, 0, altura_desnivel / 2)
rampa_izquierda.location = (-longitud_total / 2, ancho_total / 2 + ancho_rampas / 2, altura_desnivel / 2)
rampa_derecha.location = (-longitud_total / 2, -ancho_total / 2 - ancho_rampas / 2, altura_desnivel / 2)

# Jardineras
jardinera_izquierda = crear_jardinera(longitud_jardineras, ancho_jardineras, altura_jardineras)
jardinera_derecha = crear_jardinera(longitud_jardineras, ancho_jardineras, altura_jardineras)

jardinera_izquierda.location = (-longitud_total / 2 - longitud_jardineras / 2, ancho_total / 2 + ancho_jardineras / 2, altura_jardineras / 2)
jardinera_derecha.location = (-longitud_total / 2 - longitud_jardineras / 2, -ancho_total / 2 - ancho_jardineras / 2, altura_jardineras / 2)

# Iluminación de piso
iluminacion_escalera = crear_iluminacion_piso((0, 0, 0.1))
iluminacion_rampa_izquierda = crear_iluminacion_piso((-longitud_total / 2 - 0.5, ancho_total / 2 + ancho_rampas / 2 + 0.1, altura_desnivel / 2))
iluminacion_rampa_derecha = crear_iluminacion_piso((-longitud_total / 2 - 0.5, -ancho_total / 2 - ancho_rampas / 2, altura_desnivel / 2))

# --- Guardar la escena ---
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])