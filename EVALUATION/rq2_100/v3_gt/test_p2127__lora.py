import blender_arch as A
import bpy

A.limpiar_escena()

# --- ESTRUCTURA Y SUELO ---
A.crear_terreno_plano('Plaza', ancho=20, fondo=20, espesor=0.2, material='Concreto_Piso')
A.crear_columna('Base_Fuente', seccion='circ', diametro=2.5, alto=0.8, origen=(0,0,-0.2), material='Hormigon')
A.crear_columna('Cuerpo_Fuente', seccion='circ', diametro=2.0, alto=1.5, origen=(0,0,0.8), material='Hormigon')
A.crear_columna('Copa_Fuente', seccion='circ', diametro=1.5, alto=2.0, origen=(0,0,2.3), material='Marmol')

# --- ARBOLADO ---
A.crear_arbol_simple('Arbol_1', radio_copa=2.0, altura_copa=3.5, altura_tronco=1.8, origen=(-6, 6, 0))
A.crear_arbol_simple('Arbol_2', radio_copa=1.8, altura_copa=3.0, altura_tronco=1.5, origen=(6, -5, 0))
A.crear_arbol_simple('Arbol_3', radio_copa=1.5, altura_copa=2.5, altura_tronco=1.2, origen=(-5, -6, 0))

# --- BANCOS DE DISEÑO ---
def crear_banco(nombre, origen):
    # Base
    A.extruir_perfil(nombre=f'{nombre}_Base', puntos_2d=[(0,0), (2.2,0), (2.2,0.4), (0,0.4), (-2.2,0.4), (-2.2,0), (-2.2,-0.4), (0,-0.4)], altura=0.4, material='Madera_Roble')
    # Asiento
    A.extruir_perfil(nombre=f'{nombre}_Asiento', puntos_2d=[(0,0), (2.0,0), (2.0,0.3), (0,0.3), (-2.0,0.3), (-2.0,0), (-2.0,-0.3), (0,-0.3)], altura=0.4, material='Madera_Roble')
    # Respaldo
    A.extruir_perfil(nombre=f'{nombre}_Respaldo', puntos_2d=[(0,0), (2.0,0), (2.0,0.3), (0,0.3), (-2.0,0.3), (-2.0,0), (-2.0,-0.3), (0,-0.3)], altura=0.9, material='Madera_Roble')
    # Unir partes
    bpy.context.view_layer.objects.active = bpy.data.objects[f'{nombre}_Base']
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifier[0].operation = 'DIFFERENCE'
    bpy.context.object.modifier[0].object = bpy.data.objects[f'{nombre}_Asiento']
    bpy.ops.object.modifier_apply(modifier=bpy.context.object.modifier.name)
    bpy.context.object.name = nombre
    bpy.data.objects.remove(bpy.data.objects[nombre + '_Asiento'])
    bpy.data.objects.remove(bpy.data.objects[nombre + '_Respaldo'])

crear_banco('Banco_Plaza_1', origen=(-4, 4, 0))
crear_banco('Banco_Plaza_2', origen=(4, -3, 0))
crear_banco('Banco_Plaza_3', origen=(-3, -4, 0))