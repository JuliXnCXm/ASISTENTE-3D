import bpy
import math
from mathutils import Vector

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Parámetros
radio_cupula = 4.0
frecuencia = 2
radio_vertice = 0.08 / 2
radio_arista = 0.04 / 2

# 1. Crear el icosaedro base
bpy.ops.mesh.primitive_ico_sphere_add(radius=radio_cupula, subdivisions=frecuencia, location=(0, 0, 0))
ico_obj = bpy.context.active_object
ico_mesh = ico_obj.data

# 2. Crear esferas en los vértices
vertices_coords = [v.co for v in ico_mesh.vertices]
for i, coord in enumerate(vertices_coords):
    if coord.z >= -0.001: # Solo hemisferio superior
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radio_vertice, location=coord)
        bpy.context.active_object.name = f"Vertice_{i}"

# 3. Crear cilindros en las aristas
edges = [e for e in ico_mesh.edges]
for i, edge in enumerate(edges):
    v1_idx = edge.vertices[0]
    v2_idx = edge.vertices[1]
    
    v1 = vertices_coords[v1_idx]
    v2 = vertices_coords[v2_idx]
    
    # Solo crear aristas en el hemisferio superior
    if v1.z >= -0.001 and v2.z >= -0.001:
        dist = (v1 - v2).length
        center = (v1 + v2) / 2
        
        # Calcular la rotación del cilindro
        direction = v2 - v1
        quat = direction.to_track_quat('Z', 'Y')
        
        bpy.ops.mesh.primitive_cylinder_add(
            radius=radio_arista, 
            depth=dist, 
            location=center, 
            rotation=quat.to_euler()
        )
        bpy.context.active_object.name = f"Arista_{i}"

# 4. Limpiar el icosaedro original
bpy.data.objects.remove(ico_obj, do_unlink=True)