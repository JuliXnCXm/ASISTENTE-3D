import blender_arch as A
import bpy
bpy.ops.wm.read_homefile(use_empty=True)
num_peldanos = 15
huella = 0.28
contrahuella = 0.18
ancho_escalera = 1.1
A.crear_escalera_recta(
    nombre="EscaleraPrincipal",
    huella=huella,
    contrahuella=contrahuella,
    ancho=ancho_escalera,
    num_peldanos=num_peldanos,
    con_contrahuellas=True,
    material="Hormigon"
)
pos_x_baranda = -(ancho_escalera / 2) - 0.05
pos_y_baranda = num_peldanos * huella
pos_z_baranda = num_peldanos * contrahuella
A.crear_baranda_lineal(
    nombre="BarandaDescanso",
    largo=1.5,
    altura=1.0,
    origen=(pos_x_baranda, pos_y_baranda, pos_z_baranda),
    material="Acero_Inox"
)