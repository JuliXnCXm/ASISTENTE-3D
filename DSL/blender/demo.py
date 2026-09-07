# demo.py
# ---------------------------------------------------------
# Demo completa de la DSL blender_arch
# Uso: blender --background --python demo.py -- --out /tmp/demo.blend
# ---------------------------------------------------------
import os, sys, bpy

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import blender_arch as A

# --- Escena limpia ---
A.limpiar_escena()

# ---------------------------------------------------------
# ESCENA EXTERIOR — fachada + terreno + vegetación
# ---------------------------------------------------------

# Terreno
A.crear_terreno_plano("Terreno", ancho=24, fondo=18, espesor=0.3,
                      origen=(-2, -2, -0.3))

# Muros perimetrales de una vivienda simple
A.crear_muro("Fachada_Sur",  largo=8.0, alto=3.0, grosor=0.2,
             origen=(0, 0, 0))
A.crear_muro("Muro_Norte",   largo=8.0, alto=3.0, grosor=0.2,
             origen=(0, 6.0, 0))
A.crear_muro("Muro_Oeste",   largo=6.0, alto=3.0, grosor=0.2,
             origen=(0, 0.2, 0), rotacion_z=90)
A.crear_muro("Muro_Este",    largo=6.0, alto=3.0, grosor=0.2,
             origen=(7.8, 0.2, 0), rotacion_z=90)

# Tejado a dos aguas
A.crear_tejado_dos_aguas("Tejado_Casa", ancho=8.0, fondo=6.0,
                          altura_cumbrera=2.0, espesor=0.15,
                          voladizo_x=0.4, voladizo_y=0.3,
                          origen=(0, 0, 3.0))

# Ventana en fachada sur
v1 = A.crear_ventana("Ventana_Fachada_1", ancho=1.2, alto=1.0,
                     espesor_marco=0.05, prof_marco=0.2,
                     divisiones=(2, 1), origen=(1.0, 0, 1.0))
v2 = A.crear_ventana("Ventana_Fachada_2", ancho=1.2, alto=1.0,
                     espesor_marco=0.05, prof_marco=0.2,
                     divisiones=(2, 1), origen=(4.0, 0, 1.0))

# Puerta principal
A.crear_puerta("Puerta_Principal", ancho=1.0, alto=2.15,
               espesor_panel=0.045, ancho_marco=0.08, prof_marco=0.2,
               origen=(6.5, 0, 0))

# Columnas decorativas de la entrada
A.crear_columna("Col_Ent_Izq", seccion="circ", diametro=0.2, alto=3.2,
                origen=(6.2, -0.3, 0))
A.crear_columna("Col_Ent_Der", seccion="circ", diametro=0.2, alto=3.2,
                origen=(7.6, -0.3, 0))

# Baranda frente a la entrada
A.crear_baranda_lineal("Baranda_Entrada", largo=7.8, altura=0.9,
                        poste_cada=1.0, num_travesanos=2,
                        origen=(0, -0.6, 0))

# Árboles en el jardín
A.crear_arbol_simple("Arbol_1", radio_copa=1.8, altura_copa=3.0,
                     altura_tronco=1.5, origen=(-1.5, 1.0, 0))
A.crear_arbol_simple("Arbol_2", radio_copa=1.5, altura_copa=2.5,
                     altura_tronco=1.2, origen=(-1.5, 5.0, 0))
A.crear_arbol_simple("Arbol_3", radio_copa=2.0, altura_copa=3.5,
                     altura_tronco=2.0, origen=(9.5, 3.0, 0))

# ---------------------------------------------------------
# ESCENA INTERIOR — habitación + mobiliario
# ---------------------------------------------------------

# Habitación completa desplazada para no solapar
HAB_X = 12.0

A.crear_habitacion("Sala_Principal", ancho=5.0, fondo=4.5, alto=3.0,
                   grosor_muro=0.2, grosor_losa=0.2,
                   origen=(HAB_X, 0, 0))

# Mobiliario sala
mesa = A.crear_mesa("Mesa_Sala", ancho=1.8, fondo=0.9, alto=0.75,
                    origen=(HAB_X + 1.5, 1.5, 0))

for i, off in enumerate([(-0.6, 0, 0), (2.0, 0, 0),
                          (0.45, -0.7, 0), (0.45, 1.65, 0)]):
    A.crear_silla(f"Silla_{i+1}", origen=(
        HAB_X + 1.5 + off[0],
        1.5 + off[1],
        off[2],
    ))

A.crear_sofa("Sofa_Sala", ancho=2.2, fondo=0.9,
             origen=(HAB_X + 0.3, 3.3, 0))

A.crear_estanteria("Librero_Sala", ancho=1.0, alto=2.1, fondo=0.35,
                   num_estantes=4, origen=(HAB_X + 4.0, 0.3, 0))

# Habitación dormitorio
A.crear_habitacion("Dormitorio_1", ancho=4.0, fondo=3.5, alto=3.0,
                   grosor_muro=0.2, origen=(HAB_X + 6.5, 0, 0))

A.crear_cama("Cama_Matrimonial", ancho=1.6, largo=2.0,
             origen=(HAB_X + 7.0, 0.5, 0))

A.crear_armario("Closet_Dorm1", ancho=2.0, alto=2.4, fondo=0.6,
                num_puertas=2, origen=(HAB_X + 6.7, 2.8, 0))

# Escalera que conecta niveles
A.crear_escalera_recta("Escalera_Interior",
                        huella=0.28, contrahuella=0.175,
                        ancho=1.1, num_peldanos=14,
                        con_contrahuellas=True, con_zancas=True,
                        origen=(HAB_X + 5.5, 0, 0))

# Instalaciones (tubería de agua)
A.crear_tuberia("Tuberia_Agua",
                puntos_3d=((0, 0, 0.5), (0, 3, 0.5), (4, 3, 0.5)),
                radio=0.025, material="Cobre",
                origen=(HAB_X + 0.1, 0.1, 0))

# Ventana interior
A.crear_ventana("Ventana_Dorm", ancho=1.0, alto=1.2,
                divisiones=(1, 1), prof_marco=0.2,
                origen=(HAB_X + 9.0, 1.0, 1.0))

# Geometría genérica — demo extruir_perfil y extruir_con_huecos
A.extruir_perfil("Dintel_Arco",
                 puntos_2d=[(0, 0), (0.5, 0), (0.5, 0.6),
                            (0.25, 0.85), (0, 0.6)],
                 altura=0.1,
                 material="Hormigon").location = (HAB_X + 3, 4.5, 2.5)

A.extruir_con_huecos("MarcoDecorativos",
                      contorno=[(0, 0), (0.6, 0), (0.6, 0.6), (0, 0.6)],
                      agujeros=[[(0.1, 0.1), (0.5, 0.1),
                                 (0.5, 0.5), (0.1, 0.5)]],
                      altura=0.05,
                      material="Metal").location = (HAB_X + 2, 4.6, 1.0)

# ---------------------------------------------------------
# ILUMINACIÓN Y CÁMARA
# ---------------------------------------------------------

# Luz solar exterior
A.agregar_luz("Luz_Sol", tipo="SUN", ubicacion=(5, -5, 10),
              energia=5.0, color=(1.0, 0.97, 0.88))

# Luces de techo interiores
A.agregar_luz("Luz_Sala",      tipo="AREA", ubicacion=(HAB_X + 2.5, 2.25, 2.8),
              energia=400, color=(1.0, 0.95, 0.85))
A.agregar_luz("Luz_Dormitorio",tipo="AREA", ubicacion=(HAB_X + 8.5, 1.75, 2.8),
              energia=300, color=(1.0, 0.93, 0.80))

# Cámara principal (isométrica)
A.crear_camara("Camara_Principal",
               ubicacion=(10, -12, 8),
               rotacion=(60, 0, 45),
               focal_length=35, activa=True)

# ---------------------------------------------------------
# GUARDAR / EXPORTAR
# ---------------------------------------------------------

if "--" in sys.argv:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/tmp/dsl_demo_completo.blend")
    ap.add_argument("--formato", default="BLEND",
                    choices=["BLEND", "OBJ", "FBX", "GLTF", "STL"])
    ap.add_argument("--render", action="store_true",
                    help="Renderiza vistas estándar a /tmp/renders/")
    args, _ = ap.parse_known_args(sys.argv[sys.argv.index("--") + 1:])

    A.exportar_escena(args.out, formato=args.formato)
    print(f"[Demo] Guardado en {args.out}")

    if args.render:
        print("[Demo] El renderizado automático requiere el script images.py. Ejecuta: python images.py")
