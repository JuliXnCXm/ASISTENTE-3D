```python
import bpy

# Crear el edificio
bpy.ops.mesh.primitive_cube_add(size=10, enter_editmode=False, align='WORLD', location=(0, 0, 0))

# Establecer la altura del edificio
bpy.context.object.data.size = 20

# Crear el muro de estuco blanco para la planta baja
bpy.ops.mesh.primitive_cube_add(size=10, enter_editmode=False, align='WORLD', location=(0, 0, 0))
bpy.context.object.name = "MuroBajo"
bpy.context.object.data.materials.append(bpy.data.materials.new(name="EstucoBlanco"))
bpy.context.object.data.materials[0].diffuse_color = (1, 1, 1)
bpy.context.object.data.materials[0].diffuse_shader = 'LAMINAR'
bpy.context.object.data.materials[0].laminar_type = 'PLANE'
bpy.context.object.data.materials[0].laminar_angle = 90
bpy.context.object.data.materials[0].laminar_size = 0.01
bpy.context.object.data.materials[0].laminar_distance = 0.01
bpy.context.object.data.materials[0].laminar_rotation = 0
bpy.context.object.data.materials[0].laminar_depth = 0.01
bpy.context.object.data.materials[0].laminar_strength = 1
bpy.context.object.data.materials[0].laminar_texture = 'BLANK'

# Crear la entrada principal acristalada
bpy.ops.mesh.primitive_cube_add(size=3, enter_editmode=False, align='WORLD', location=(0, 0, 0))
bpy.context.object.name = "EntradaPrincipal"
bpy.context.object.data.materials.append(bpy.data.materials.new(name="Acristalado"))
bpy.context.object.data.materials[0].diffuse_color = (0, 0, 0)
bpy.context.object.data.materials[0].diffuse_shader = 'ACRISTALADO'
bpy.context.object.data.materials[0].acristalado_transparency = 0.8
bpy.context.object.data.materials[0].acristalado_reflection = 0.2
bpy.context.object.data.materials[0].acristalado_refraction = 0.2
bpy.context.object.data.materials[0].acristalado_fresnel = 0.1
bpy.context.object.data.materials[0].acristalado_fresnel_power = 10
bpy.context.object.data.materials[0].acristalado_fresnel_offset = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_power = 10
bpy.context.object.data.materials[0].acristalado_fresnel_slope_offset = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_power = 10
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_offset = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_power = 10
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_offset = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_power = 10
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_offset = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_power = 10
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_offset = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_power = 10
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_offset = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_power = 10
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_offset = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_power = 10
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_offset = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_power = 10
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_offset = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_power = 10
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_offset = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_power = 10
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_offset = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_power = 10
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_offset = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_power = 10
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_offset = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_power = 10
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_offset = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_power = 10
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_offset = 0.5
bpy.context.object.data.materials[0].acristalado_fresnel_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope_slope = 0