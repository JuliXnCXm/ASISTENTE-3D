import blender_arch as A
import bpy

# Limpiar la escena
A.limpiar_escena()

# --- DEFINIR DIMENSIONES ---
ANCHO_OFICINA = 8.0
FONDO_OFICINA = 6.0
ALTO_OFICINA = 3.0

# --- CREAR ESPACIO PRINCIPAL ---
room = A.crear_habitacion("OficinaOpenPlan", ancho=ANCHO_OFICINA, fondo=FONDO_OFICINA, alto=ALTO_OFICINA, grosor_muro=0.1,
                          material_muro="Muro_Pintura_Gris", material_suelo="Concreto_Piso")

# --- SALA DE REUNIONES DE VIDRIO (3x3m en una esquina) ---
DIM_SALA = 3.0
# Tabique frontal
tabique1 = A.crear_losa_rectangular("TabiqueVidrio1", ancho=DIM_SALA, fondo=0.05, espesor=ALTO_OFICINA, 
                                    origen=(0, DIM_SALA, 0))
A.asignar_material(tabique1, "Vidrio")
# Tabique lateral
tabique2 = A.crear_losa_rectangular("TabiqueVidrio2", ancho=0.05, fondo=DIM_SALA-1.0, espesor=ALTO_OFICINA, 
                                    origen=(DIM_SALA, 0, 0))
A.asignar_material(tabique2, "Vidrio")

# Puerta de vidrio
puerta_vidrio = A.crear_puerta("PuertaSala", ancho=0.9, alto=2.4, prof_marco=0.05, origen=(DIM_SALA, DIM_SALA-0.95, 0), 
                               material_panel="Vidrio_Templado", material_marco="Marco_Aluminio")

# Mobiliario sala de reuniones
mesa_reunion = A.crear_mesa("MesaReunion", ancho=1.2, fondo=1.2, alto=0.75, origen=(DIM_SALA/2, DIM_SALA/2, 0),
                             material_tablero="Vidrio_Esmerilado", material_patas="Acero_Inox")
silla_r1 = A.crear_silla("SillaR1", origen=(DIM_SALA/2, DIM_SALA/2 - 0.8, 0), material="Cuero")
silla_r2 = A.crear_silla("SillaR2", origen=(DIM_SALA/2, DIM_SALA/2 + 0.8, 0), material="Cuero")
silla_r2.rotation_euler[2] = 3.14159
silla_r3 = A.crear_silla("SillaR3", origen=(DIM_SALA/2 - 0.8, DIM_SALA/2, 0), material="Cuero")
silla_r3.rotation_euler[2] = 1.5708
silla_r4 = A.crear_silla("SillaR4", origen=(DIM_SALA/2 + 0.8, DIM_SALA/2, 0), material="Cuero")
silla_r4.rotation_euler[2] = -1.5708

# --- PUESTOS DE TRABAJO (4 puestos) ---
POSICIONES_PUESTOS = [(5.0, 1.5), (7.0, 1.5), (5.0, 4.0), (7.0, 4.0)]

for i, pos in enumerate(POSICIONES_PUESTOS):
    nombre_base = f"Puesto_{i+1}"
    mesa = A.crear_mesa(f"{nombre_base}_Mesa", ancho=1.4, fondo=0.7, alto=0.75, origen=(pos[0], pos[1], 0),
                        material_tablero="Madera_Roble", material_patas="Marco_Negro")
    silla = A.crear_silla(f"{nombre_base}_Silla", ancho=0.5, fondo=0.5, alto_asiento=0.48, alto_respaldo=1.1,
                          origen=(pos[0], pos[1]-0.6, 0), material="Tela_Gris")

# --- ELEMENTOS ADICIONALES ---
armario_archivo = A.crear_armario("ArmarioArchivo", ancho=2.5, alto=2.0, fondo=0.45, num_puertas=3,
                                  origen=(ANCHO_OFICINA - 2.6, FONDO_OFICINA - 0.55, 0), 
                                  material_cuerpo="MDF_Blanco", material_puerta="MDF_Blanco")

# --- ILUMINACIÓN Y CÁMARA ---
A.agregar_luz("LuzOficina1", tipo="AREA", ubicacion=(ANCHO_OFICINA/2, FONDO_OFICINA*0.25, ALTO_OFICINA-0.1), energia=1000)
A.agregar_luz("LuzOficina2", tipo="AREA", ubicacion=(ANCHO_OFICINA/2, FONDO_OFICINA*0.75, ALTO_OFICINA-0.1), energia=1000)
A.crear_camara("CamaraOficina", ubicacion=(ANCHO_OFICINA/2, -5, ALTO_OFICINA/2 + 1), rotacion=(70, 0, 0), activa=True)