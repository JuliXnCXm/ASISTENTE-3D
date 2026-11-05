import blender_arch as A
A.limpiar_escena()
A.crear_escalera_recta(nombre='Escalera_Caracol', huella=0.28, contrahuella=0.175, ancho=1.1, num_peldanos=16, grosor_peldano=0.03, con_contrahuellas=True, con_zancas=True, espesor_zanca=0.15, origen=(0, 0, 0), material='Madera')
A.crear_columna(nombre='Poste_Central', seccion='circ', diametro=0.2, alto=3.0, origen=(0, 0, 0), material='Hormigon')