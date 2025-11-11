import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
ancho_hab = 4.0
largo_hab = 3.0
alto_zocalo = 0.08
espesor_zocalo = 0.015

def crear_zocalo(nombre, escala, posicion):
    bpy.ops.mesh.primitive_cube_add(size=1, scale=escala, location=posicion)
    zocalo = bpy.context.active_object
    zocalo.name = nombre

# Zócalo Norte
escala_norte = (ancho_hab, espesor_zocalo, alto_zocalo)
pos_norte = (0, largo_hab / 2 - espesor_zocalo / 2, alto_zocalo / 2)
crear_zocalo('ZocaloNorte', escala_norte, pos_norte)

# Zócalo Sur
escala_sur = (ancho_hab, espesor_zocalo, alto_zocalo)
pos_sur = (0, -largo_hab / 2 + espesor_zocalo / 2, alto_zocalo / 2)
crear_zocalo('ZocaloSur', escala_sur, pos_sur)

# Zócalo Este
ancho_util = ancho_hab - 2 * espesor_zocalo
escala_este = (espesor_zocalo, largo_hab, alto_zocalo)
pos_este = (ancho_hab / 2 - espesor_zocalo / 2, 0, alto_zocalo / 2)
crear_zocalo('ZocaloEste', escala_este, pos_este)

# Zócalo Oeste
escala_oeste = (espesor_zocalo, largo_hab, alto_zocalo)
pos_oeste = (-ancho_hab / 2 + espesor_zocalo / 2, 0, alto_zocalo / 2)
crear_zocalo('ZocaloOeste', escala_oeste, pos_oeste)