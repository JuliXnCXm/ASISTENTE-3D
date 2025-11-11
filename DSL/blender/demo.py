# demo_atomic.py
import os, sys, bpy
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
import blender_arch as A

bpy.ops.wm.read_factory_settings(use_empty=True)

# A.crear_muro(nombre="MuroA", largo=1, alto=3, grosor=0.25)
A.crear_ventana(nombre="VentanaA", ancho=1.5, alto=1.2, espesor_marco=0.06, prof_marco=0.29, divisiones=(7,2), espesor_divisor=0.03)
A.crear_puerta(nombre="PuertaA", ancho=1.0, alto=2.2, espesor_panel=0.045, ancho_marco=0.08, prof_marco=0.12)
A.crear_techo_plano(nombre="TechoA", ancho=8, fondo=6, espesor=0.2, caida_x=0.05, caida_y=0.0, origen=(0,5,3.0))
A.crear_silla(nombre="SillaA")
A.crear_sofa(nombre="SofaA", ancho=2.1, fondo=0.9)
A.crear_cama(nombre="CamaA", ancho=1.6, largo=2.0)
A.crear_tuberia(nombre="TuberiaA", puntos_3d=((0,0,0),(0,2,0),(1,2,0.5)), radio=0.05)
A.crear_columna("ColRect", seccion="rect", ancho=0.3, fondo=0.5, alto=3.2).location = (0,2,0)
A.crear_columna("ColCirc", seccion="circ", diametro=0.4, alto=3.2).location = (1,2,0)
A.crear_losa_rectangular("LosaA", ancho=6, fondo=4, espesor=0.2).location = (0,4,3.0)
A.crear_escalera_recta("EscaleraDemo", huella=0.30, contrahuella=0.17, ancho=1.2, num_peldanos=12).location = (0,6,0)
A.crear_mesa("MesaDemo", ancho=1.8, fondo=0.9).location = (3,0,0)
A.crear_baranda_lineal("BarandaDemo", largo=8, altura=1.05).location = (0,8,0)

# Guardar si pasas --out
if "--" in sys.argv:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/tmp/atomic_demo.blend")
    args, _ = ap.parse_known_args(sys.argv[sys.argv.index("--")+1:])
    bpy.ops.wm.save_as_mainfile(filepath=args.out)
    print("Guardado en", args.out)
