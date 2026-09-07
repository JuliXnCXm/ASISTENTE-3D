import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

largo_tramo = 10.0
ancho_acera = 2.0
ancho_calzada = 4.0

A.crear_losa_rectangular(
    nombre="Acera",
    ancho=largo_tramo,
    fondo=ancho_acera,
    espesor=0.15,
    origen=(-largo_tramo/2, -ancho_acera/2, 0),
    material="Concreto_Piso"
)

A.crear_losa_rectangular(
    nombre="Calzada",
    ancho=largo_tramo,
    fondo=ancho_calzada,
    espesor=0.15,
    origen=(-largo_tramo/2, ancho_acera/2, -0.05),
    material="Asfalto"
)

A.crear_baranda_lineal(
    nombre="Baranda_Proteccion",
    largo=largo_tramo,
    altura=1.0,
    poste_cada=1.5,
    origen=(-largo_tramo/2, -ancho_acera/2, 0.15),
    material="Acero_Inox"
)