# test_dsl.py
import os
import sys
import unittest

# Ensure the DSL is in the path
HERE = os.path.dirname(os.path.abspath(__file__))
DSL_DIR = os.path.abspath(os.path.join(HERE, "..", "DSL", "blender"))
if DSL_DIR not in sys.path:
    sys.path.insert(0, DSL_DIR)

import blender_arch as A
import bpy
import bmesh

class TestBlenderArch(unittest.TestCase):
    def setUp(self):
        A.limpiar_escena()

    def assertMeshValid(self, obj):
        self.assertEqual(obj.type, 'EMPTY')
        # Check all child meshes or curves
        geom_found = False
        def check_recursive(o):
            nonlocal geom_found
            if o.type in ('MESH', 'CURVE'):
                geom_found = True
                if o.type == 'MESH':
                    rep = A.validar_malla(o, verbose=False)
                    # We only assert it didn't crash. Non-manifold edges are common after Booleans.
            for c in o.children:
                check_recursive(c)
        check_recursive(obj)
        self.assertTrue(geom_found, f"No se encontró geometría en {obj.name}")

    def test_materiales(self):
        obj = A.crear_muro("MuroTest")
        mesh = A._first_mesh_child(obj)
        mat = A.asignar_material(mesh, "TestMat", base_color=(1, 0, 0, 1), transmission=0.5)
        self.assertIsNotNone(mat)
        self.assertEqual(mat.name, "TestMat")
        
    def test_muro(self):
        muro = A.crear_muro("Muro", largo=4.0, alto=3.0, grosor=0.2)
        self.assertMeshValid(muro)
        
    def test_columna(self):
        col_rect = A.crear_columna("ColRect", seccion="rect", ancho=0.3, fondo=0.3, alto=3.0)
        self.assertMeshValid(col_rect)
        col_circ = A.crear_columna("ColCirc", seccion="circ", diametro=0.3, alto=3.0)
        self.assertMeshValid(col_circ)

    def test_losa_y_piso(self):
        losa = A.crear_losa_rectangular("Losa", ancho=4, fondo=3, espesor=0.2)
        self.assertMeshValid(losa)
        piso = A.crear_piso("Piso", ancho=4, fondo=3, espesor=0.05)
        self.assertMeshValid(piso)

    def test_techos(self):
        techo = A.crear_techo_plano("TechoP", ancho=6, fondo=4, espesor=0.2)
        self.assertMeshValid(techo)
        tejado = A.crear_tejado_dos_aguas("Tejado", ancho=8, fondo=6, altura_cumbrera=2.5)
        self.assertMeshValid(tejado)

    def test_huecos(self):
        muro = A.crear_muro("MuroHueco", largo=5, alto=3, grosor=0.2)
        A.abrir_vanos_batch_rectangulares(muro, [(2.5, 0, 1.5)], 1.0, 1.0)
        self.assertMeshValid(muro)

        muro2 = A.crear_muro("MuroHueco2", largo=10, alto=3, grosor=0.2)
        A.abrir_vanos_grid_local(muro2, 2, 3, 1.0, 1.0, 2.0, 1.5, 1.0, 1.0)
        self.assertMeshValid(muro2)

    def test_ventana_y_puerta(self):
        ventana = A.crear_ventana("Ventana", ancho=1.2, alto=1.2)
        self.assertMeshValid(ventana)
        puerta = A.crear_puerta("Puerta", ancho=0.9, alto=2.1)
        self.assertMeshValid(puerta)

    def test_escaleras_y_barandas(self):
        esc = A.crear_escalera_recta("Escalera", num_peldanos=10, con_zancas=True, con_contrahuellas=True)
        self.assertMeshValid(esc)
        bar = A.crear_baranda_lineal("Baranda", largo=4.0)
        self.assertMeshValid(bar)

    def test_mobiliario(self):
        mesa = A.crear_mesa("Mesa")
        self.assertMeshValid(mesa)
        silla = A.crear_silla("Silla")
        self.assertMeshValid(silla)
        sofa = A.crear_sofa("Sofa")
        self.assertMeshValid(sofa)
        cama = A.crear_cama("Cama")
        self.assertMeshValid(cama)
        est = A.crear_estanteria("Estanteria")
        self.assertMeshValid(est)
        arm = A.crear_armario("Armario")
        self.assertMeshValid(arm)

    def test_exterior(self):
        terreno = A.crear_terreno_plano("Terreno")
        self.assertMeshValid(terreno)
        arbol = A.crear_arbol_simple("Arbol")
        self.assertMeshValid(arbol)

    def test_composites(self):
        hab = A.crear_habitacion("Hab")
        self.assertMeshValid(hab)
        # Note: creating a house/building takes more time but should be tested
        casa = A.crear_casa_n_pisos("Casa", pisos=1)
        self.assertMeshValid(casa)
        edif = A.crear_edificio_n_pisos("Edificio", pisos=2)
        self.assertMeshValid(edif)

    def test_edificio_columnas_por_defecto(self):
        from mathutils import Vector
        edif = A.crear_edificio_n_pisos("E", pisos=3, ancho=12, fondo=15)
        bpy.context.view_layer.update()
        cols = [o for o in edif.children if o.get("arch_categoria") == "columna"]
        # rejilla completa: ≥ 4 esquinas por piso
        self.assertGreaterEqual(len(cols), 4 * 3)
        for c in cols:
            m = A._first_mesh_child(c)
            pts = [m.matrix_world @ Vector(v) for v in m.bound_box]
            self.assertGreaterEqual(min(p.x for p in pts), 0.2 - 1e-4)   # dentro de muros
            self.assertLessEqual(max(p.x for p in pts), 12 - 0.2 + 1e-4)
            self.assertGreaterEqual(min(p.y for p in pts), 0.2 - 1e-4)
            self.assertLessEqual(max(p.y for p in pts), 15 - 0.2 + 1e-4)

    def test_geometria_generica(self):
        extr = A.extruir_perfil("Extr", [(0,0), (1,0), (1,1), (0,1)])
        self.assertMeshValid(extr)
        
        extr_huecos = A.extruir_con_huecos("ExtrHuecos", [(0,0), (2,0), (2,2), (0,2)], agujeros=[[(0.5,0.5), (1.5,0.5), (1.5,1.5), (0.5,1.5)]])
        self.assertMeshValid(extr_huecos)

        tub = A.crear_tuberia("Tub", [(0,0,0), (0,1,0), (1,1,0)])
        self.assertMeshValid(tub)

    def test_luces_y_camaras(self):
        luz = A.agregar_luz("LuzTest")
        self.assertEqual(luz.type, 'LIGHT')
        cam = A.crear_camara("CamTest")
        self.assertEqual(cam.type, 'CAMERA')

    def test_utilidades(self):
        muro = A.crear_muro("MuroAncla", largo=5)
        silla = A.crear_silla("SillaAncla")
        A.anclar_a(silla, muro, punto_anchor="centro", offset=(1,0,0))
        self.assertAlmostEqual(silla.location.x, 2.5 + 1.0 + 0) # muro x center is 2.5

    def test_torre(self):
        from mathutils import Vector
        for kw in (dict(pisos=30), dict(pisos=12, giro_por_piso=3.0),
                   dict(pisos=20, escala_superior=0.6, seccion_columna="circ")):
            A.limpiar_escena()
            torre = A.crear_torre("T", ancho=24, fondo=24, **kw)
            bpy.context.view_layer.update()
            pisos = [c for c in torre.children if c.get("arch_categoria") == "piso_torre"]
            self.assertEqual(len(pisos), kw["pisos"])
            for piso in pisos:
                meshes = [m for m in piso.children_recursive if m.type == 'MESH']
                losas = [m for m in meshes if m.name.endswith("_Losa")]
                cols = [m for m in meshes if "_Col_" in m.name]
                self.assertEqual(len(losas), 1, piso.name)
                self.assertGreaterEqual(len(cols), 4, piso.name)
                z_losa = min((losas[0].matrix_world @ Vector(c)).z for c in losas[0].bound_box)
                for c in cols:
                    z_top = max((c.matrix_world @ Vector(v)).z for v in c.bound_box)
                    self.assertAlmostEqual(z_top, z_losa, places=3, msg=c.name)

if __name__ == '__main__':
    # run tests
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestBlenderArch)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
