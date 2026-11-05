import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Terreno
A.crear_terreno_plano(
    nombre="JardinCasa", 
    ancho=30.0, 
    fondo=25.0, 
    origen=(-10, -12.5, -0.1), 
    material="Cesped"
)

# Casa
A.crear_casa_n_pisos(
    nombre="CasaCampo", 
    pisos=2, 
    ancho=10.0, 
    fondo=8.0, 
    alto_piso=2.8, 
    con_tejado=True, 
    material_muro="Estuco", 
    material_tejado="Teja"
)

# Camino de acceso
A.crear_losa_rectangular(
    nombre="Camino", 
    ancho=3.0, 
    fondo=8.0, 
    espesor=0.1, 
    origen=(3.5, -8.0, 0.0), 
    material="Concreto_Piso"
)