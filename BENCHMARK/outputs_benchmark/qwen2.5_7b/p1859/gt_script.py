import blender_arch as A
import bpy

A.limpiar_escena()

# --- Estructura y mobiliario base ---
hab = A.crear_habitacion('Oficina', ancho=3.5, fondo=3, alto=2.8, material_muro='Muro_Pintura', material_suelo='Parquet')
estanteria = A.crear_estanteria('EstanteriaLibros', ancho=1.5, alto=2.4, fondo=0.3, num_estantes=5, origen=(0.15, 1.2, 0), material='Madera')
silla = A.crear_silla('SillaOficina', origen=(2.0, 1.0, 0), material='Marco_Negro')
silla.rotation_euler[2] = -0.8 # Girar la silla

# --- Escritorio en L personalizado (bpy) ---
# Definir el perfil 2D de la L
perfil_L = [
    (0, 0),
    (2.0, 0),
    (2.0, 0.6),
    (0.6, 0.6),
    (0.6, 1.5),
    (0, 1.5)
]

# Crear la malla y el objeto
mesh_data = bpy.data.meshes.new('perfil_escritorio_mesh')
obj_perfil = bpy.data.objects.new('PerfilEscritorio', mesh_data)

# Vincular a la escena
scene = bpy.context.scene
scene.collection.objects.link(obj_perfil)

# Generar la malla a partir de los puntos
verts = [(p[0], p[1], 0) for p in perfil_L]
edges = []
faces = [tuple(range(len(verts)))]
mesh_data.from_pydata(verts, edges, faces)
mesh_data.update()

# Mover el objeto a su posición y extruir
obj_perfil.location = (1.3, 1.3, 0.75)

solidify_mod = obj_perfil.modifiers.new(name='GrosorTablero', type='SOLIDIFY')
solidify_mod.thickness = -0.04 # Extruir hacia abajo
solidify_mod.offset = 1
A.asignar_material(obj_perfil, 'MDF_Blanco')

# --- Patas del escritorio (bpy) ---
posiciones_patas = [(1.35, 1.35), (3.25, 1.35), (3.25, 1.85), (1.35, 2.75)]
for i, pos in enumerate(posiciones_patas):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.75, location=(pos[0], pos[1], 0.375))
    pata = bpy.context.active_object
    pata.name = f'Pata_{i+1}'
    A.asignar_material(pata, 'Acero_Inox')

# --- Iluminación ---
A.agregar_luz('LuzOficina', tipo='AREA', ubicacion=(1.75, 1.5, 2.6), energia=250, color=(0.95, 0.95, 1))
A.crear_camara('CamaraOficina', ubicacion=(-1, 1.5, 1.8), rotacion=(80, 0, -70))