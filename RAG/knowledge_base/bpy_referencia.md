# Referencia bpy — Operaciones esenciales para modelado AEC

Subconjunto curado de la API de Blender Python (bpy) relevante para el dominio
AEC (Architecture, Engineering and Construction). Complementa el DSL blender_arch.
Unidades: metros. Versión Blender: 4.x

---

## Crear y vincular un objeto a la escena

```python
import bpy

# 1. Crear datos de malla vacía
mesh = bpy.data.meshes.new("nombre_mesh")

# 2. Crear objeto y asignar la malla
obj = bpy.data.objects.new("nombre_objeto", mesh)

# 3. Vincularlo a la colección activa (aparece en la escena)
bpy.context.collection.objects.link(obj)

# 4. Seleccionarlo y hacerlo activo
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
```

> Alternativa rápida con primitivas:
> ```python
> bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
> obj = bpy.context.active_object
> obj.name = "MiCubo"
> obj.scale = (ancho, fondo, alto)
> bpy.ops.object.transform_apply(scale=True)
> ```

---

## Construir geometría con bmesh

bmesh es la API de bajo nivel para crear y editar mallas directamente en memoria,
sin depender de operadores de Blender (`bpy.ops`). Es más rápido y predecible
para geometría paramétrica.

```python
import bpy, bmesh

# Crear malla con bmesh
mesh = bpy.data.meshes.new("Malla")
bm   = bmesh.new()

# Añadir vértices
v0 = bm.verts.new((0, 0, 0))
v1 = bm.verts.new((1, 0, 0))
v2 = bm.verts.new((1, 1, 0))
v3 = bm.verts.new((0, 1, 0))

# IMPORTANTE: actualizar tabla de índices antes de acceder por índice
bm.verts.ensure_lookup_table()

# Crear cara (orden antihorario visto desde arriba = normal hacia +Z)
bm.faces.new([v0, v1, v2, v3])
bm.faces.ensure_lookup_table()  # necesario tras faces.new()

# Extruir cara hacia +Z (altura)
ret = bmesh.ops.extrude_face_region(bm, geom=[bm.faces[0]])
verts_nuevos = [v for v in ret['geom'] if isinstance(v, bmesh.types.BMVert)]
bmesh.ops.translate(bm, vec=(0, 0, 3.0), verts=verts_nuevos)

# Escribir bmesh en la malla y liberar
bm.to_mesh(mesh)
bm.free()
mesh.update()

# Crear objeto con la malla
obj = bpy.data.objects.new("Objeto", mesh)
bpy.context.collection.objects.link(obj)
```

> **Errores comunes:**
> - `IndexError: BMElemSeq[index]: outdated internal index table` →
>   agregar `bm.verts.ensure_lookup_table()` o `bm.faces.ensure_lookup_table()`
>   después de cualquier operación que añada o elimine elementos.
> - Nunca mezclar `bmesh.ops.*` con accesos por índice sin actualizar la tabla.

---

## Transformaciones de objetos

```python
from mathutils import Vector, Euler
from math import radians

obj = bpy.context.active_object

# Posición
obj.location = Vector((x, y, z))
obj.location.x += 1.0          # desplazar en X

# Rotación (en radianes internamente, pero se puede convertir)
obj.rotation_euler = Euler((radians(90), 0, radians(45)), 'XYZ')

# Escala
obj.scale = (1.0, 1.0, 2.0)   # doble de alto

# Aplicar transformaciones (hace las transformaciones permanentes en la malla)
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
```

> En modelado paramétrico es preferible ajustar `obj.location` y `obj.rotation_euler`
> en lugar de usar `bpy.ops.transform.translate()`, que depende del contexto de UI.

---

## Materiales — asignación básica

```python
import bpy

def asignar_color(obj, nombre, color_rgba=(0.8, 0.8, 0.8, 1.0)):
    """Crea o reutiliza un material y lo asigna al objeto."""
    if nombre in bpy.data.materials:
        mat = bpy.data.materials[nombre]
    else:
        mat = bpy.data.materials.new(name=nombre)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = color_rgba
            bsdf.inputs["Roughness"].default_value = 0.7

    # Asignar al slot 0 del objeto
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    return mat

# Uso:
asignar_color(obj, "Hormigon", (0.62, 0.62, 0.62, 1.0))
```

> Para vidrio (transparencia):
> ```python
> mat.blend_method = 'BLEND'
> bsdf.inputs["Transmission Weight"].default_value = 1.0
> bsdf.inputs["Roughness"].default_value = 0.0
> ```

---

## Operación booleana (Boolean Modifier)

Usada para abrir vanos (puertas, ventanas) en muros.
El objeto A es el muro; el objeto B es el volumen del hueco.

```python
import bpy

def aplicar_booleano(obj_base, obj_cortador, operacion='DIFFERENCE'):
    """
    Aplica modificador booleano y elimina el objeto cortador.
    operacion: 'DIFFERENCE' | 'UNION' | 'INTERSECT'
    """
    mod = obj_base.modifiers.new(name="Bool", type='BOOLEAN')
    mod.operation = operacion
    mod.solver = 'EXACT'          # más preciso que FAST para arquitectura
    mod.object = obj_cortador

    # Aplicar (requiere que obj_base sea el objeto activo)
    bpy.context.view_layer.objects.active = obj_base
    bpy.ops.object.modifier_apply(modifier=mod.name)

    # Eliminar el cortador
    bpy.data.objects.remove(obj_cortador, do_unlink=True)

# Ejemplo: abrir una ventana en un muro
# 1. Crear cubo que representa el hueco
bpy.ops.mesh.primitive_cube_add(size=1)
hueco = bpy.context.active_object
hueco.scale = (ancho_ventana, profundidad_muro + 0.1, alto_ventana)
hueco.location = (cx, cy, cz)
bpy.ops.object.transform_apply(scale=True)

# 2. Aplicar booleano
aplicar_booleano(muro_obj, hueco)
```

> **Nota solver EXACT vs FAST:**
> - `EXACT`: más lento pero correcto para geometría coplanar y muros con esquinas.
> - `FAST`: más rápido pero falla con caras paralelas (común en muros).
> Usar siempre `EXACT` para arquitectura.

---

## Colecciones (organización de escena)

```python
import bpy

# Crear una colección
col = bpy.data.collections.new("Piso_1")
bpy.context.scene.collection.children.link(col)

# Mover objeto a una colección específica
def mover_a_coleccion(obj, coleccion):
    # Desvincularlo de todas las colecciones actuales
    for c in obj.users_collection:
        c.objects.unlink(obj)
    # Vincularlo a la nueva
    coleccion.objects.link(obj)

mover_a_coleccion(obj, col)

# Crear sub-colección anidada
sub_col = bpy.data.collections.new("Muros")
col.children.link(sub_col)
```

---

## Objetos Empty (root / nodo organizador)

Los Empty son objetos sin geometría usados como raíz (parent) de un grupo.
Permiten mover/rotar/escalar todo el grupo con una sola operación.

```python
import bpy

# Crear Empty
empty = bpy.data.objects.new("RootGrupo", None)
empty.empty_display_type = 'ARROWS'   # visualización en viewport
empty.empty_display_size = 0.5
bpy.context.collection.objects.link(empty)

# Parentear objeto al Empty
def parentear(hijo, padre):
    hijo.parent = padre
    hijo.matrix_parent_inverse = padre.matrix_world.inverted()

parentear(muro_obj, empty)

# Almacenar metadatos como propiedades custom
empty["arch_tipo"]     = "habitacion"
empty["arch_ancho"]    = 5.0
empty["arch_alto"]     = 3.0
# Recuperar:
tipo = empty.get("arch_tipo", "desconocido")
```

---

## Limpiar escena

```python
import bpy

def limpiar_escena():
    """Elimina todos los objetos y datos huérfanos."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Eliminar datos huérfanos (mallas, materiales, etc. sin usuarios)
    for bloque in (bpy.data.meshes, bpy.data.materials,
                   bpy.data.cameras, bpy.data.lights,
                   bpy.data.curves):
        for item in bloque:
            if item.users == 0:
                bloque.remove(item)
```

---

## Exportar escena

```python
import bpy, os

ruta = "/tmp/modelo.glb"

# GLTF / GLB (para web, Three.js)
bpy.ops.export_scene.gltf(
    filepath=ruta,
    export_format='GLB',
    export_apply=True,          # aplica modificadores
    export_materials='EXPORT',
)

# OBJ
bpy.ops.wm.obj_export(
    filepath="/tmp/modelo.obj",
    export_materials=True,
)

# FBX
bpy.ops.export_scene.fbx(
    filepath="/tmp/modelo.fbx",
    apply_unit_scale=True,
    global_scale=1.0,
)

# Guardar .blend nativo
bpy.ops.wm.save_as_mainfile(filepath="/tmp/modelo.blend")
```

---

## Iluminación y cámara básicas

```python
import bpy
from math import radians

# Luz solar
luz_data = bpy.data.lights.new("Sol", type='SUN')
luz_data.energy = 5.0
luz_obj = bpy.data.objects.new("Sol", luz_data)
luz_obj.rotation_euler = (radians(45), 0, radians(135))
bpy.context.collection.objects.link(luz_obj)

# Cámara perspectiva
cam_data = bpy.data.cameras.new("Camara")
cam_data.lens = 35.0             # focal en mm
cam_obj = bpy.data.objects.new("Camara", cam_data)
cam_obj.location = (10, -12, 8)
cam_obj.rotation_euler = (radians(60), 0, radians(45))
bpy.context.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj   # cámara activa de la escena
```

---

## Propiedades de render (sin renderizar)

```python
import bpy

scene = bpy.context.scene

# Motor
scene.render.engine = 'BLENDER_EEVEE'   # o 'CYCLES'

# Resolución
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100

# Ruta de salida
scene.render.filepath = "/tmp/render_output.png"
scene.render.image_settings.file_format = 'PNG'

# Muestras CYCLES
scene.cycles.samples = 128
```
