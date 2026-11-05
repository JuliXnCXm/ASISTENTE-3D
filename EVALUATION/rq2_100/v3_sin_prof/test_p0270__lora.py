import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
ancho_total = 6.0
alto_total = 3.0
grosor_perfil = 0.1
divisiones_h = 4
divisiones_v = 2
espesor_vidrio = 0.005

# --- Creación de Paneles de Vidrio ---
def crear_panel_vidrio(nombre, ubicacion):
    # Crear el objeto vacío para el panel
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=ubicacion)
    panel = bpy.context.active_object
    panel.name = nombre
    
    # Crear el material del vidrio
    mat_vidrio = bpy.data.materials.new(name="Vidrio")
    mat_vidrio.use_nodes = True
    bsdf = mat_vidrio.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1)
        bsdf.inputs['Roughness'].default_value = 0.8
    panel.data.materials.append(mat_vidrio)

    # Crear el objeto vacío para el vidrio
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    vidrio = bpy.context.active_object
    vidrio.name = nombre + "_Vidrio"
    vidrio.dimensions = (ancho_total / divisiones_v, grosor_perfil * 1.2, alto_total / divisiones_h)
    vidrio.parent = panel
    return panel

# --- Creación de Montantes y Travesaños ---
def crear_perfil(nombre, ubicacion, dimensiones):
    bpy.ops.mesh.primitive_cube_add(location=ubicacion)
    perfil = bpy.context.active_object
    perfil.name = nombre
    perfil.dimensions = dimensiones
    return perfil

# Montantes (verticales)
espaciado_v = ancho_total / (divisiones_v - 1)
for i in range(divisiones_v):
    x = -ancho_total/2 + i * espaciado_v
    crear_perfil(f"Montante_{i}", (x, 0, alto_total/2), (grosor_perfil, alto_total, grosor_perfil))

# Travesaños (horizontales)
espaciado_h = alto_total / (divisiones_h - 1)
for i in range(divisiones_h):
    z = -alto_total/2 + i * espaciado_h
    crear_perfil(f"Travesano_{i}", (0, 0, z), (ancho_total, grosor_perfil, grosor_perfil))

# --- Creación de Paneles de Vidrio ---
num_paneles = divisiones_v * divisiones_h
for i in range(num_paneles):
    x = -ancho_total/2 + i % divisiones_v * espaciado_v
    z = -alto_total/2 + i // divisiones_v * espaciado_h
    crear_panel_vidrio(f"Panel_Vidrio_{i}", (x, 0, z))