import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

largo = 5.0 # Dimensión en Y
ancho = 4.0 # Dimensión en X
alto = 2.8
espesor = 0.2

def crear_muro(nombre, loc, sca):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, scale=sca)
    muro = bpy.context.active_object
    muro.name = nombre

# Muro Norte (al fondo en Y+)
crear_muro('MuroNorte', (ancho/2, largo - espesor/2, alto/2), (ancho, espesor, alto))

# Muro Sur (al frente en Y-)
crear_muro('MuroSur', (ancho/2, espesor/2, alto/2), (ancho, espesor, alto))

# Muro Este (a la derecha en X+)
crear_muro('MuroEste', (ancho - espesor/2, largo/2, alto/2), (espesor, largo - 2*espesor, alto))

# Muro Oeste (a la izquierda en X-)
crear_muro('MuroOeste', (espesor/2, largo/2, alto/2), (espesor, largo - 2*espesor, alto))