import bpy
import bmesh
import math

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la escalera ---
altura_total = 3.0
diametro_total = 1.8
num_escalones = 16
radio_poste = 0.075
grosor_escalon = 0.05
vuelta_completa_grados = 360

# --- Cálculos derivados ---
altura_escalon = altura_total / num_escalones
angulo_por_escalon = math.radians(vuelta_completa_grados / num_escalones)
radio_exterior = diametro_total / 2

# --- Crear poste central ---
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_poste,
    depth=altura_total,
    location=(0, 0, altura_total / 2),
    vertices=32
)
poste = bpy.context.active_object
poste.name = "PosteCentral"

# --- Crear un escalón y duplicarlo ---
for i in range(num_escalones):
    # Crear la forma base del escalón con bmesh
    bm = bmesh.new()

    # Vértices del escalón (forma de cuña)
    v1 = bm.verts.new((radio_poste, 0, 0))
    v2 = bm.verts.new((radio_exterior, 0, 0))
    
    # Rotar para el siguiente borde de la cuña
    angulo_siguiente = math.radians(vuelta_completa_grados / num_escalones * 0.9) # 0.9 para dejar un pequeño espacio
    v3_x = radio_exterior * math.cos(angulo_siguiente)
    v3_y = radio_exterior * math.sin(angulo_siguiente)
    v3 = bm.verts.new((v3_x, v3_y, 0))

    v4_x = radio_poste * math.cos(angulo_siguiente)
    v4_y = radio_poste * math.sin(angulo_siguiente)
    v4 = bm.verts.new((v4_x, v4_y, 0))

    # Crear la cara inferior
    bm.faces.new((v1, v2, v3, v4))
    
    # Extruir hacia arriba para dar grosor
    geom = bmesh.ops.extrude_face_region(bm, geom=bm.faces)
    verts_extruidos = [v for v in geom['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, grosor_escalon), verts=verts_extruidos)

    # Crear el objeto mesh
    mesh = bpy.data.meshes.new(f"MeshEscalon_{i+1}")
    bm.to_mesh(mesh)
    bm.free()
    
    escalon_obj = bpy.data.objects.new(f"Escalon_{i+1}", mesh)
    scene.collection.objects.link(escalon_obj)

    # Posicionar y rotar el escalón
    escalon_obj.location.z = i * altura_escalon
    escalon_obj.rotation_euler.z = i * angulo_por_escalon