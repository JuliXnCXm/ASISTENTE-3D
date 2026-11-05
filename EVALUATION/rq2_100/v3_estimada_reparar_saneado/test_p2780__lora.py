import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros del panel ---
ancho_total = 6.0
alto_total = 9.0
grosor_perfil = 0.1
espesor_vidrio = 0.02
ancho_panel = 1.5
alto_panel = 3.0
num_h = int(ancho_total / ancho_panel)
num_v = int(alto_total / alto_panel)

# --- Creación de un panel completo ---
def crear_panel():
    # Perfil horizontal
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, grosor_perfil/2, alto_panel/2))
    perfil_h = bpy.context.active_object
    perfil_h.name = "PerfilH"
    perfil_h.dimensions = (ancho_panel, grosor_perfil, alto_panel)
    
    # Perfil vertical
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-ancho_panel/2 + grosor_perfil/2, 0, alto_panel/2))
    perfil_v = bpy.context.active_object
    perfil_v.name = "PerfilV"
    perfil_v.dimensions = (grosor_perfil, ancho_panel, alto_panel)
    
    # Vidrio
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, grosor_perfil/2, alto_panel/2))
    vidrio = bpy.context.active_object
    vidrio.name = "Vidrio"
    vidrio.dimensions = (ancho_panel - 2 * grosor_perfil, espesor_vidrio, alto_panel)
    
    # Unir todos en un solo objeto
    bpy.ops.object.select_all(action='DESELECT')
    perfil_h.select_set(True)
    perfil_v.select_set(True)
    vidrio.select_set(True)
    bpy.context.view_layer.objects.active = perfil_h
    bpy.ops.object.join()
    return bpy.context.active_object

# --- Creación de los paneles ---
for i in range(num_h):
    for j in range(num_v):
        x_pos = -ancho_total/2 + (i * ancho_panel) + ancho_panel/2
        z_pos = j * alto_panel
        
        bpy.ops.object.delete()
        crear_panel().location = (x_pos, 0, z_pos)