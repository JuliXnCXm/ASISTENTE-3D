# Estándares AEC — Referencia para generación de modelos arquitectónicos

Dominio: Architecture, Engineering and Construction (AEC)
Unidades: metros (m) salvo indicación contraria
Uso: base de conocimiento para el asistente de modelado 3D con DSL blender_arch

---

## 1. Alturas de entrepiso y libre

| Espacio | Altura libre mínima (m) | Altura libre típica (m) |
|---|---|---|
| Vivienda (sala, dormitorio) | 2.40 | 2.60 – 2.80 |
| Vivienda (cocina, baño) | 2.20 | 2.40 |
| Oficinas | 2.60 | 2.80 – 3.20 |
| Comercio / locales | 3.00 | 3.50 – 4.50 |
| Garaje | 2.20 | 2.40 |
| Bodega / industrial | 4.00 | 5.00 – 8.00 |

> **En el DSL:** `alto` en `crear_muro`, `crear_habitacion`, `crear_losa_rectangular`.
> Altura de entrepiso = altura libre + espesor de losa (típico 0.20 m).

---

## 2. Espesores de muros y losas

| Elemento | Espesor mínimo (m) | Espesor típico (m) |
|---|---|---|
| Muro exterior de mampostería | 0.15 | 0.20 – 0.30 |
| Muro interior divisorio | 0.10 | 0.12 – 0.15 |
| Muro estructural de concreto | 0.15 | 0.20 – 0.25 |
| Losa maciza de entrepiso | 0.10 | 0.20 – 0.25 |
| Losa de cubierta plana | 0.10 | 0.20 |
| Cimentación corrida | 0.30 | 0.40 – 0.60 |

> **En el DSL:** `grosor` en `crear_muro`; `espesor` en `crear_losa_rectangular`, `crear_piso`, `crear_techo_plano`.

---

## 3. Puertas

| Tipo | Ancho (m) | Alto (m) | Observaciones |
|---|---|---|---|
| Puerta principal exterior | 0.90 – 1.20 | 2.10 – 2.40 | Puede ser doble hoja |
| Puerta interior habitaciones | 0.80 – 0.90 | 2.00 – 2.10 | Estándar residencial |
| Puerta de baño | 0.70 – 0.80 | 2.00 | Mínimo 0.70 m |
| Puerta de garaje (vehicular) | 2.40 – 3.00 | 2.00 – 2.20 | Seccional o corrediza |
| Puerta de emergencia | 0.90 | 2.10 | Doble hoja ≥ 1.80 m |
| Puerta accesible (PMR) | ≥ 0.90 | 2.10 | Libre paso ≥ 0.80 m |

> **En el DSL:** `ancho`, `alto` en `crear_puerta`.

---

## 4. Ventanas

| Tipo | Ancho típico (m) | Alto típico (m) | Alféizar desde suelo (m) |
|---|---|---|---|
| Ventana sala / comedor | 1.20 – 2.40 | 1.00 – 1.40 | 0.80 – 1.00 |
| Ventana dormitorio | 0.90 – 1.50 | 1.00 – 1.20 | 0.90 – 1.10 |
| Ventana baño (privacidad) | 0.40 – 0.60 | 0.40 – 0.60 | 1.60 – 1.80 |
| Ventana cocina | 0.80 – 1.20 | 0.60 – 0.90 | 1.00 – 1.20 |
| Muro cortina / fachada vidrio | Variable | Piso a techo | 0.00 |
| Tragaluz / claraboya (plana) | 0.60 – 1.20 | 0.60 – 1.20 | En cubierta |

> **En el DSL:** `ancho`, `alto`, `origen[2]` (alféizar en Z) en `crear_ventana`.
> `divisiones=(nx, ny)`: ventana de 1 paño = (1,1); con travesaño horizontal = (1,2).

---

## 5. Escaleras

| Parámetro | Mínimo | Recomendado | Máximo |
|---|---|---|---|
| Ancho libre escalera vivienda | 0.90 m | 1.00 – 1.20 m | — |
| Ancho libre escalera pública | 1.20 m | 1.50 – 1.80 m | — |
| Huella (profundidad del peldaño) | 0.25 m | 0.28 – 0.30 m | 0.35 m |
| Contrahuella (altura del escalón) | 0.14 m | 0.165 – 0.18 m | 0.20 m |
| Relación 2C + H | — | 0.60 – 0.65 m | — |
| Altura de baranda / pasamanos | 0.90 m | 1.00 – 1.10 m | — |
| Número de peldaños por tramo | — | 10 – 18 | 18 |

> Fórmula de Blondel: `2 × contrahuella + huella ≈ 0.63 m`
> **En el DSL:** `huella`, `contrahuella`, `ancho`, `num_peldanos` en `crear_escalera_recta`.
> Altura total = `num_peldanos × contrahuella`.

---

## 6. Columnas y vigas

| Elemento | Sección mínima | Sección típica | Observaciones |
|---|---|---|---|
| Columna rectangular (concreto) | 0.20 × 0.20 m | 0.30 × 0.30 m | Para luces hasta 5 m |
| Columna circular (concreto) | ø 0.25 m | ø 0.30 – 0.40 m | |
| Columna metálica (perfil H) | ø eq. 0.15 m | 0.20 – 0.30 m | |
| Viga de concreto | 0.20 × 0.30 m | 0.25 × 0.50 m | Alto ≈ L/12 |
| Viga metálica | — | H = L/20 | L = luz libre |

> **En el DSL:** `ancho`, `fondo` en `crear_columna(seccion='rect')`; `diametro` en `crear_columna(seccion='circ')`.

---

## 7. Mobiliario — dimensiones estándar

### Sala / Comedor
| Mueble | Ancho (m) | Fondo (m) | Alto (m) |
|---|---|---|---|
| Sofá de 2 puestos | 1.40 – 1.60 | 0.80 – 0.90 | 0.75 – 0.85 |
| Sofá de 3 puestos | 1.90 – 2.20 | 0.80 – 0.90 | 0.75 – 0.85 |
| Mesa de centro | 0.80 – 1.20 | 0.50 – 0.70 | 0.40 – 0.45 |
| Mesa comedor 4 personas | 1.20 – 1.40 | 0.80 – 0.90 | 0.72 – 0.76 |
| Mesa comedor 6 personas | 1.60 – 2.00 | 0.90 – 1.00 | 0.72 – 0.76 |
| Silla de comedor | 0.40 – 0.50 | 0.40 – 0.50 | 0.80 – 0.95 |

### Dormitorio
| Mueble | Ancho (m) | Largo (m) | Alto (m) |
|---|---|---|---|
| Cama individual | 0.90 – 1.00 | 1.90 – 2.00 | 0.45 – 0.55 (colchón) |
| Cama doble | 1.35 – 1.40 | 1.90 – 2.00 | 0.45 – 0.55 |
| Cama queen | 1.50 – 1.60 | 2.00 – 2.10 | 0.45 – 0.55 |
| Cama king | 1.80 – 2.00 | 2.00 – 2.10 | 0.45 – 0.55 |
| Cabecero | igual cama | — | 0.80 – 1.20 |
| Armario / closet 2 puertas | 1.60 – 2.00 | 0.55 – 0.65 | 2.00 – 2.40 |
| Armario / closet 3 puertas | 2.00 – 2.70 | 0.55 – 0.65 | 2.00 – 2.40 |
| Mesita de noche | 0.40 – 0.55 | 0.35 – 0.45 | 0.50 – 0.65 |

### Almacenaje
| Mueble | Ancho (m) | Fondo (m) | Alto (m) |
|---|---|---|---|
| Estantería / librero | 0.60 – 1.20 | 0.25 – 0.35 | 1.80 – 2.20 |
| Aparador / buffet | 1.20 – 1.80 | 0.40 – 0.50 | 0.80 – 0.90 |

> **En el DSL:** parámetros `ancho`, `fondo` / `largo`, `alto` en `crear_mesa`, `crear_silla`, `crear_sofa`, `crear_cama`, `crear_estanteria`, `crear_armario`.

---

## 8. Áreas mínimas de espacios (residencial)

| Espacio | Área mínima (m²) | Área recomendada (m²) |
|---|---|---|
| Alcoba principal | 9.00 | 12.00 – 18.00 |
| Alcoba secundaria | 7.00 | 9.00 – 12.00 |
| Sala-comedor | 16.00 | 20.00 – 30.00 |
| Cocina | 5.40 | 7.00 – 12.00 |
| Baño social | 2.50 | 3.00 – 4.00 |
| Baño principal | 4.00 | 5.00 – 7.00 |
| Garaje (1 vehículo) | 12.50 | 15.00 – 18.00 |

> Para calcular `ancho × fondo` en `crear_habitacion`: p. ej. alcoba 3.5 × 3.5 = 12.25 m².

---

## 9. Circulaciones y pasillos

| Espacio | Ancho libre mínimo (m) |
|---|---|
| Pasillo interior vivienda | 0.90 |
| Pasillo de circulación general | 1.20 |
| Circulación accesible (PMR) | 1.20 (giro 1.50 × 1.50) |
| Corredor público / comercial | 1.80 – 2.40 |

---

## 10. Cubiertas y tejados

| Tipo | Pendiente típica | Observaciones |
|---|---|---|
| Cubierta plana | 1 – 3 % | Requiere impermeabilización |
| Tejado a dos aguas | 20 – 35 % | `altura_cumbrera / (fondo/2)` |
| Tejado a cuatro aguas | 25 – 40 % | |
| Cubierta inclinada simple | 15 – 25 % | |

> Para `crear_tejado_dos_aguas`: pendiente = `altura_cumbrera / (fondo / 2)`.
> Pendiente 30% sobre fondo=6 m → `altura_cumbrera = 0.30 × 3.0 = 0.90 m`.
> Voladizo típico: 0.30 – 0.60 m.

---

## 11. Iluminación (referencia para DSL)

| Tipo de luz | Función DSL | Energía típica | Uso |
|---|---|---|---|
| Solar exterior | `agregar_luz(tipo='SUN')` | 3.0 – 6.0 | Iluminación general exterior |
| Área (techo interior) | `agregar_luz(tipo='AREA')` | 200 – 600 W | Habitación, oficina |
| Punto (lámpara) | `agregar_luz(tipo='POINT')` | 100 – 400 W | Accento, decorativa |
| Spot (foco dirigido) | `agregar_luz(tipo='SPOT')` | 400 – 1000 W | Entrada, escaparate |

---

## 12. Vegetación exterior (referencia)

| Especie / tipo | Radio copa (m) | Altura copa (m) | Altura tronco (m) |
|---|---|---|---|
| Arbusto pequeño | 0.50 – 0.80 | 0.60 – 1.00 | 0.10 – 0.20 |
| Árbol mediano (jardín) | 1.50 – 2.50 | 2.00 – 4.00 | 1.00 – 2.00 |
| Árbol grande (parque) | 3.00 – 6.00 | 4.00 – 8.00 | 2.00 – 4.00 |
| Palma | 0.80 – 1.50 | 1.00 – 2.00 | 4.00 – 8.00 |

> **En el DSL:** `radio_copa`, `altura_copa`, `altura_tronco` en `crear_arbol_simple`.
