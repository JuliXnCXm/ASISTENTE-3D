import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

muro_fachada = A.crear_muro(
    nombre="Fachada_Principal",
    largo=10.0,
    alto=6.0,
    grosor=0.25,
    material="Ladrillo_Rojo"
)

A.abrir_vanos_grid_local(
    muro=muro_fachada,
    filas=2,
    cols=4,
    x0=1.0,
    z0=1.0,
    dx=2.4,
    dz=2.5,
    ancho=1.2,
    alto=1.1
)

# El DSL no tiene una función para rellenar vanos, se asume que se crean por separado.
# Aquí se genera una ventana para mostrar cómo se haría en una posición.
A.crear_ventana(
    nombre="Ventana_Ejemplo", 
    ancho=1.2, 
    alto=1.1, 
    prof_marco=0.25, 
    origen=(1.0, 0, 1.0), 
    material_marco="Marco_Aluminio", 
    material_vidrio="Vidrio"
)