import blender_arch as A
import bpy

A.limpiar_escena()

# --- Terreno y deck ---
A.crear_terreno_plano("TerrenoCesped", ancho=20, fondo=20, espesor=0.2, origen=(-10,-10,-0.2), material="Cesped")
deck = A.crear_piso("DeckMadera", ancho=12, fondo=10, espesor=0.1, origen=(-6, -8, 0), material="Parquet")

# --- Crear estructura de la piscina con bpy ---
ancho_piscina, fondo_piscina, prof_piscina = 8, 4, 1.5

# Bloque principal de hormigón
bpy.ops.mesh.primitive_cube_add(location=(0, -2, -0.75), scale=(ancho_piscina/2+0.5, fondo_piscina/2+0.5, prof_piscina/2+0.1))
estructura = bpy.context.active_object
estructura.name = "EstructuraPiscina"
A.asignar_material(estructura, "Hormigon")

# Objeto para el vaciado (booleana)
bpy.ops.mesh.primitive_cube_add(location=(0, -2, -0.6), scale=(ancho_piscina/2, fondo_piscina/2, prof_piscina/2))
vaciado = bpy.context.active_object
vaciado.name = "VaciadoPiscina"
vaciado.display_type = 'WIRE'

bool_mod = estructura.modifiers.new(name="BooleanVaciado", type='BOOLEAN')
bool_mod.object = vaciado
bool_mod.operation = 'DIFFERENCE'

# --- Modelado del borde infinito y canal con bpy ---
borde_infinito_y = -2 + fondo_piscina/2 # Lado Y positivo

bpy.ops.mesh.primitive_cube_add(location=(0, borde_infinito_y + 0.15, -1.5), scale=(ancho_piscina/2, 0.05, 0.1))
recorte_borde = bpy.context.active_object
recorte_borde.name = "RecorteBordeInfinito"

bool_mod_borde = estructura.modifiers.new(name="BooleanBorde", type='BOOLEAN')
bool_mod_borde.object = recorte_borde
bool_mod_borde.operation = 'DIFFERENCE'

bpy.ops.mesh.primitive_cube_add(location=(0, borde_infinito_y + 0.4, -1.7), scale=(ancho_piscina/2, 0.1, 0.2))
canal = bpy.context.active_object
canal.name = "CanalRebalse"
A.asignar_material(canal, "Hormigon")

# Aplicar modificadores (opcional para visualización)
# bpy.context.view_layer.objects.active = estructura
# bpy.ops.object.modifier_apply(modifier=bool_mod.name)
# bpy.ops.object.modifier_apply(modifier=bool_mod_borde.name)
# bpy.data.objects.remove(vaciado)
# bpy.data.objects.remove(recorte_borde)

# --- Agua ---
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -2, -0.1))
agua = bpy.context.active_object
agua.name = "AguaPiscina"
agua.scale.x = ancho_piscina
agua.scale.y = fondo_piscina
A.asignar_material(agua, "Agua")

# --- Escalones de obra ---
num_escalones = 4
for i in range(num_escalones):
    escalon_ancho = 1.5
    escalon_huella = 0.3
    escalon_alto = 0.25
    x_pos = -ancho_piscina/2 + escalon_ancho/2
    y_pos = -2 - fondo_piscina/2 + escalon_huella/2 + i * escalon_huella
    z_pos = -prof_piscina + escalon_alto/2 + i * escalon_alto
    bpy.ops.mesh.primitive_cube_add(location=(x_pos, y_pos, z_pos), scale=(escalon_ancho/2, escalon_huella/2, escalon_alto/2))
    escalon = bpy.context.active_object
    escalon.name = f"Escalon.{i}"
    A.asignar_material(escalon, "Hormigon")