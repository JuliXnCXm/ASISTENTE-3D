import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
altura_poste = 6.0
radio_poste = 0.15
largo_brazo = 1.5
radio_luminaria = 0.25

# Crear el poste vertical
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_poste,
    depth=altura_poste,
    location=(0, 0, altura_poste / 2)
)
poste = bpy.context.active_object
poste.name = "Farola_Poste"

# Crear el brazo horizontal
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_poste * 0.6,
    depth=largo_brazo,
    location=(0, largo_brazo / 2, altura_poste),
    rotation=(math.radians(90), 0, 0)
)
brazo = bpy.context.active_object
brazo.name = "Farola_Brazo"

# Crear la luminaria (media esfera)
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=radio_luminaria,
    location=(0, largo_brazo, altura_poste)
)
luminaria = bpy.context.active_object
luminaria.name = "Farola_Luminaria"

# Cortar la esfera para hacerla semiesférica (aproximación por creación)
# Se crea un cubo grande que se podría usar para una operación booleana
# Pero como no se permite edición, se deja la esfera completa como representación
# Para cumplir estrictamente 'solo creación', se modelaría con vértices, lo cual excede la premisa.
# La esfera representa la luminaria.