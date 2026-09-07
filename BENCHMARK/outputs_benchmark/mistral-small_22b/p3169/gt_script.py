import blender_arch as A

A.limpiar_escena()

# --- ESPACIO GENERAL Y MATERIALES ---
ancho_oficina = 8.0
_oficina = 6.0
alto_oficina = 2.8
oficina = A.crear_habitacion("OficinaOpenPlan", ancho=ancho_oficina, fondo=_oficina, alto=alto_oficina, 
                              material_muro="Muro_Pintura_Gris", material_suelo="Parquet")

# --- SALA DE REUNIONES (con tabique de vidrio) ---
ancho_sala = 4.0
fondo_sala = 3.0
x_sala = ancho_oficina/2 - ancho_sala/2
y_sala = _oficina/2 - fondo_sala/2

# Tabiques de vidrio
tabique_1 = A.crear_muro("TabiqueVidrio1", largo=ancho_sala, alto=alto_oficina, grosor=0.05, 
                         origen=(x_sala-ancho_sala/2, y_sala, 0), material="Vidrio_Templado")
tabique_2 = A.crear_muro("TabiqueVidrio2", largo=fondo_sala-0.9, alto=alto_oficina, grosor=0.05, 
                         origen=(x_sala, y_sala-fondo_sala/2, 0), material="Vidrio_Templado")

# Mobiliario sala de reuniones
mesa_reunion = A.crear_mesa("MesaReunion", ancho=2.4, fondo=1.1, alto=0.75, 
                            origen=(x_sala, y_sala, 0), material_tablero="Madera_Roble")

for i in range(3):
    offset_x = (i - 1) * 0.8
    A.crear_silla(f"SillaReunion.A.{i}", origen=(x_sala + offset_x, y_sala - 1.1/2 - 0.4, 0), material="Cuero")
    silla_b = A.crear_silla(f"SillaReunion.B.{i}", origen=(x_sala + offset_x, y_sala + 1.1/2 + 0.4, 0), material="Cuero")
    silla_b.rotation_euler[2] = 3.14159 # Rotar 180 grados

# --- ZONA DE TRABAJO ABIERTA ---
x_puestos = [-2.0, -2.0, 2.0, 2.0]
y_puestos = [-1.5, 1.5, -1.5, 1.5]

for i in range(4):
    x, y = x_puestos[i], y_puestos[i]
    # Escritorio
    A.crear_mesa(f"Escritorio.{i}", ancho=1.4, fondo=0.7, alto=0.74, 
                 origen=(x, y, 0), material_tablero="MDF_Blanco")
    # Silla
    A.crear_silla(f"SillaTrabajo.{i}", origen=(x, y - 0.5, 0), material="Tela_Gris")
    # Cajonera
    A.crear_armario(f"Cajonera.{i}", ancho=0.4, alto=0.6, fondo=0.5, num_puertas=1, 
                    origen=(x - 1.4/2 + 0.2, y + 0.7/2 - 0.25, 0), material_cuerpo="MDF_Blanco")

# --- ILUMINACIÓN Y CÁMARA ---
A.agregar_luz("LuzOficina", tipo="AREA", ubicacion=(0, 0, 2.7), energia=800, color=(0.8, 0.9, 1.0))
A.crear_camara("CamaraOficina", ubicacion=(-6, -8, 5), rotacion=(65, 0, -45))