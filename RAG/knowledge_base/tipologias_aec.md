# Tipologías arquitectónicas — Referencia AEC

Clasificación de tipos de edificación con sus características espaciales,
dimensiones habituales y correspondencia con funciones del DSL blender_arch.

---

## 1. Vivienda unifamiliar (casa)

**Descripción:** Edificio residencial de uso exclusivo de una familia. Puede ser
de uno o varios pisos. Predomina en zonas suburbanas y rurales.

**Características:**
- 1 a 3 pisos
- Lote típico: 6 × 12 m a 12 × 20 m
- Área construida: 60 – 250 m²
- Cubierta inclinada (teja) o plana según clima

**Espacios típicos y orden usual:**
| Espacio | Piso | Área aprox. (m²) |
|---|---|---|
| Sala | 1 | 16 – 24 |
| Comedor | 1 | 10 – 16 |
| Cocina | 1 | 6 – 12 |
| Baño social | 1 | 3 – 4 |
| Garaje | 1 | 13 – 18 |
| Alcoba principal + baño | 2 | 14 – 22 |
| Alcoba secundaria × 1–2 | 2 | 9 – 14 c/u |
| Estudio / habitación extra | 2 | 8 – 12 |
| Terraza / balcón | 2 | 4 – 10 |

**Funciones DSL relevantes:**
`crear_habitacion`, `crear_muro`, `crear_losa_rectangular`, `crear_tejado_dos_aguas`,
`crear_ventana`, `crear_puerta`, `crear_escalera_recta`, `crear_baranda_lineal`,
`crear_terreno_plano`, `crear_arbol_simple`, `crear_casa_n_pisos`

---

## 2. Apartamento / unidad residencial en edificio

**Descripción:** Unidad de vivienda dentro de un edificio multifamiliar.
Comparte estructura, circulaciones y servicios con otras unidades.

**Características:**
- Área: 45 – 150 m² por unidad
- Sin garaje propio (puede tener parqueadero en sótano)
- Acceso por corredor o hall compartido

**Espacios típicos:**
| Espacio | Área aprox. (m²) |
|---|---|
| Sala-comedor integrado | 18 – 30 |
| Cocina | 5 – 10 |
| Alcoba principal | 12 – 18 |
| Alcoba secundaria | 8 – 12 |
| Baño principal | 4 – 6 |
| Baño social | 2.5 – 4 |
| Balcón (opcional) | 3 – 8 |

---

## 3. Edificio de apartamentos (multifamiliar)

**Descripción:** Edificio residencial con múltiples unidades de vivienda
distribuidas en pisos. Incluye zonas comunes.

**Características:**
- 4 a 20+ pisos
- Planta tipo repetida por piso
- Altura de entrepiso: 2.60 – 2.80 m
- Circulación vertical: escaleras + ascensores
- Zonas comunes: lobby, parqueadero, cuarto de basuras

**Planta tipo habitual:**
- 2 a 4 apartamentos por piso
- Corredor central o lateral
- Fachada con ventanas repetidas en rejilla

**Funciones DSL relevantes:**
`crear_edificio_n_pisos`, `crear_habitacion`, `crear_losa_rectangular`,
`crear_columna`, `abrir_vanos_grid_local`, `crear_escalera_recta`,
`crear_baranda_lineal`, `crear_techo_plano`

---

## 4. Oficina corporativa

**Descripción:** Espacio de trabajo administrativo. Puede ser planta libre
(open office) o con células cerradas (despachos).

**Características:**
- Altura libre: 2.80 – 3.20 m
- Iluminación cenital o lateral abundante
- Modulación estructural: 6 × 6 m a 8 × 8 m
- Falso cielo, piso técnico

**Espacios típicos:**
| Espacio | Observación |
|---|---|
| Área de trabajo abierta | 8 – 10 m² por puesto |
| Sala de reuniones | 15 – 40 m² |
| Recepción / lobby | 15 – 30 m² |
| Oficina privada / gerencia | 12 – 20 m² |
| Cocineta / cafetería | 8 – 15 m² |
| Baños (H/M) | 6 – 12 m² c/u |
| Archivo | 10 – 20 m² |

**Mobiliario DSL relevante:**
`crear_mesa`, `crear_silla`, `crear_estanteria`

---

## 5. Local comercial

**Descripción:** Espacio para actividades de comercio o servicios al público.
Planta libre con fachada vidriada.

**Características:**
- Altura: 3.00 – 4.50 m
- Fachada con grandes ventanales o muro cortina
- Sin divisiones internas fijas (planta libre)
- Área: 20 – 200 m²

**Funciones DSL relevantes:**
`crear_muro`, `crear_ventana` (ancho grande), `crear_puerta`, `crear_techo_plano`

---

## 6. Bodega / nave industrial

**Descripción:** Espacio para almacenamiento o producción. Gran altura libre,
estructura metálica o de concreto, cubierta a dos aguas o shed.

**Características:**
- Altura libre: 4.00 – 12.00 m
- Modulación: 10 × 10 m a 20 × 20 m
- Cubierta: dos aguas con pendiente 15 – 25%
- Puertas vehiculares: 3.00 × 3.50 m a 4.00 × 4.50 m

**Funciones DSL relevantes:**
`crear_muro`, `crear_columna`, `crear_losa_rectangular`,
`crear_tejado_dos_aguas`, `crear_puerta` (ancho 3–4 m)

---

## 7. Equipamiento educativo (aula / colegio)

**Descripción:** Espacios para actividades de enseñanza y aprendizaje.

**Características:**
- Altura: 2.80 – 3.20 m
- Aula estándar: 7.00 × 8.00 m (28 – 35 estudiantes)
- Iluminación bilateral, ventanas altas

**Espacios típicos:**
| Espacio | Área (m²) |
|---|---|
| Aula estándar | 50 – 60 |
| Laboratorio | 60 – 80 |
| Biblioteca | 80 – 150 |
| Dirección | 15 – 25 |
| Batería de baños | 20 – 40 |

---

## 8. Parqueadero / garaje

**Descripción:** Espacio para estacionamiento de vehículos.

**Características:**
- Cajón individual: 2.50 × 5.00 m (mínimo 2.30 × 4.50 m)
- Altura libre: ≥ 2.20 m (subterráneo), 2.40 m (superficie)
- Rampa de acceso: pendiente 15 – 20%, ancho ≥ 3.00 m
- Circulación: 5.50 – 6.50 m entre filas de cajones

---

## Resumen — Alturas de piso por tipología

| Tipología | Alto piso típico (m) | Observaciones |
|---|---|---|
| Casa / vivienda unifamiliar | 2.60 – 2.80 | Libre mínimo 2.40 m |
| Apartamento | 2.60 – 2.80 | Estructura delgada |
| Oficinas | 2.80 – 3.50 | Con falso cielo |
| Comercio | 3.00 – 4.50 | Planta libre |
| Industrial / bodega | 4.00 – 12.00 | Nave sin mezzanine |
| Educativo | 2.80 – 3.20 | |

> En `crear_casa_n_pisos` y `crear_edificio_n_pisos`, el parámetro `alto_piso`
> corresponde a la altura de entrepiso (libre + losa).
