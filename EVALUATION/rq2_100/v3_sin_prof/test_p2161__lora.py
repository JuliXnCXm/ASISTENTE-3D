import blender_arch as A
import bpy

A.limpiar_escena()

# --- Parámetros ---
ancho_piscina = 12.0
fondo_piscina = 6.0
profundidad_piscina = 1.5
ancho_deck = 2.0
grosor_losa = 0.2
ancho_escalones = 0.5
num_escalones = 5

# --- Deck ---
deck = A.crear_losa_rectangular(
    nombre="Deck",
    ancho=ancho_piscina + ancho_deck,
    fondo=ancho_deck,
    espesor=grosor_losa,
    origen=(0, 0, grosor_losa),
    material="Madera"
)

# --- Piscina infinita (con hueco) ---
piscina = A.extruir_con_huecos(
    nombre="PiscinaInfinita",
    contorno=[(-ancho_piscina/2, -fondo_piscina/2), (ancho_piscina/2, -fondo_piscina/2), (ancho_piscina/2, fondo_piscina/2), (-ancho_piscina/2, fondo_piscina/2)],
    agujeros=[[(-ancho_piscina/2, -fondo_piscina/2), (ancho_piscina/2, -fondo_piscina/2), (ancho_piscina/2, fondo_piscina/2), (-ancho_piscina/2, fondo_piscina/2)]],
    altura=profundidad_piscina,
    material="Agua"
)

# --- Escalones de obra ---
altura_escalon = profundidad_piscina / num_escalones
for i in range(num_escalones):
    pos_x = -ancho_piscina/2 + ancho_escalones/2
    pos_y = -fondo_piscina/2 + ancho_escalones/2
    pos_z = i * altura_escalon
    
    escalon = A.crear_losa_rectangular(
        nombre=f"Escalon_{i+1}",
        ancho=ancho_escalones,
        fondo=ancho_escalones,
        espesor=0.1,
        origen=(pos_x, pos_y, pos_z),
        material="Hormigon"
    )
    A.asignar_material(escalon, nombre="Hormigon", base_color=(0.5, 0.5, 0.5, 1))