import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

muro_contencion = A.crear_muro(nombre="MuroContencion", largo=10, alto=1.2, grosor=0.3, origen=(-5, 0, 0), material="Ladrillo_Rojo")
A.crear_baranda_lineal(nombre="BarandaMuro", largo=10, altura=1.0, poste_cada=1.5, origen=(-5, 0, 1.2), material="Acero_Inox")