# Patrones de distribución espacial — Layout AEC

Reglas y convenciones sobre cómo se organizan y relacionan los espacios
en arquitectura residencial y comercial. Guía para generar layouts coherentes
con el DSL blender_arch.

---

## 1. Principios generales de organización

### Zonificación
Los espacios se agrupan por función y grado de privacidad:

| Zona | Espacios | Característica |
|---|---|---|
| **Zona social** | Sala, comedor, terraza | Públicos, acceso directo desde entrada |
| **Zona privada** | Alcobas, baños privados | Alejados de la entrada, quieto |
| **Zona de servicio** | Cocina, lavadero, depósito | Acceso desde zona social o exterior |
| **Zona de circulación** | Pasillos, escaleras, hall | Conecta las tres zonas |

### Orientación solar (hemisferio norte — Colombia)
- **Sur**: zona social (sala, comedor) → mayor soleamiento
- **Norte**: zona de servicio (cocina, baños) → sombra
- **Este**: dormitorios → sol de mañana
- **Oeste**: evitar dormitorios → sol de tarde caliente

---

## 2. Vivienda unifamiliar — distribución por pisos

### Piso 1 (zona social + servicios)
```
[Garaje] — [Entrada / Hall] — [Sala]
                                 |
                             [Comedor]
                                 |
                            [Cocina] — [Patio/Lavadero]
                                 |
                          [Baño social]
```

**Reglas:**
- Garaje adyacente a la entrada pero sin comunicación directa con dormitorios
- Cocina adyacente al comedor (conexión directa o puerta)
- Baño social accesible desde sala/comedor sin pasar por zonas privadas
- Escalera cerca al hall de entrada

### Piso 2 (zona privada)
```
[Hall / corredor] — [Alcoba principal + Baño privado]
        |
        +——————— [Alcoba 2]
        |
        +——————— [Alcoba 3 / Estudio]
```

**Reglas:**
- Corredor corto (máximo 3 puertas en línea)
- Alcoba principal: la más grande, con baño privado, alejada de escalera
- Baño compartido accesible desde corredor, nunca solo desde una alcoba

---

## 3. Edificio multifamiliar — distribución de planta tipo

```
[Escalera / Ascensor] — [Corredor central]
                               |
              +————————————————+————————————————+
              |                                  |
       [Apto A]                            [Apto B]
     (fachada N)                         (fachada S)
```

**Reglas:**
- Núcleo de circulación (escalera + ascensor) en el centro de la planta
- Fachadas con ventanas simétricas o en rejilla
- Cada unidad debe tener ventilación e iluminación natural directa
- Circulación horizontal ≤ 30 m desde núcleo a puerta de apto

---

## 4. Oficina — distribución abierta (open office)

```
[Recepción / Lobby] — [Área de trabajo abierta]
                               |
              +———————————————+—————————————————+
              |               |                  |
     [Sala reuniones]   [Oficinas privadas]  [Cocineta]
              |
         [Baños H/M]
```

**Reglas:**
- Recepción visible desde acceso principal
- Salas de reuniones con paredes de vidrio (visibilidad + privacidad acústica)
- Baños al fondo, alejados de zona de trabajo
- Cocineta / cafetería no adyacente a salas de reuniones

---

## 5. Adyacencias recomendadas

### Espacios que deben estar contiguos (puerta directa)
| Espacio A | Espacio B | Motivo |
|---|---|---|
| Cocina | Comedor | Servicio de alimentos |
| Alcoba principal | Baño privado | Privacidad |
| Sala | Comedor | Flujo social |
| Sala | Terraza / balcón | Extensión de zona social |
| Garaje | Zona de servicio | Descarga de compras |

### Espacios que NO deben estar contiguos
| Espacio A | Espacio B | Motivo |
|---|---|---|
| Baño | Cocina / Comedor | Higiene y olores |
| Dormitorio | Sala / comedor | Ruido |
| Garaje | Dormitorios | Gases y ruido |

---

## 6. Dimensiones mínimas de circulación

| Elemento | Dimensión mínima | Recomendado |
|---|---|---|
| Pasillo interior | 0.90 m | 1.00 – 1.20 m |
| Hall de entrada | 1.50 × 1.50 m | 2.00 × 2.00 m |
| Corredor edificio | 1.20 m | 1.50 m |
| Descanso de escalera | ancho escalera | +0.20 m c/lado |

---

## 7. Patrones de fachada

### Fachada residencial simple
- Puerta centrada o desplazada un tercio del ancho total
- Ventanas simétricas respecto a la puerta o alineadas verticalmente entre pisos
- Alféizar de ventanas al mismo nivel en toda la fachada

### Fachada de oficinas o comercio
- Ventanería corrida o muro cortina (80 – 100% del vano)
- Entrada destacada: mayor ancho, marquesina o voladizo
- Módulo estructural visible en fachada (ritmo de columnas)

### Fachada industrial
- Ventanas altas y estrechas para iluminación sin generar calor
- Puerta vehicular a nivel de suelo, centrada o lateral
- Cubierta a dos aguas visible en fachada lateral (hastial)

---

## 8. Correspondencia con funciones DSL

### Generar una casa de 2 pisos con layout típico
```python
import blender_arch as A

# Piso 1 — zona social
A.crear_habitacion('PB_SalaComedor', ancho=7.0, fondo=4.5, alto=2.7,
                   origen=(0, 0, 0))
A.crear_habitacion('PB_Cocina', ancho=3.5, fondo=3.0, alto=2.7,
                   origen=(7.0, 0, 0))
A.crear_habitacion('PB_Garaje', ancho=3.5, fondo=5.5, alto=2.5,
                   origen=(0, 4.5, 0))

# Piso 2 — zona privada (offset en Z)
A.crear_habitacion('P2_AlcobaPpal', ancho=4.0, fondo=4.0, alto=2.7,
                   origen=(0, 0, 2.9))
A.crear_habitacion('P2_Alcoba2', ancho=3.5, fondo=3.5, alto=2.7,
                   origen=(4.0, 0, 2.9))

# O directamente con la función compuesta:
A.crear_casa_n_pisos('Casa', pisos=2, ancho=10.0, fondo=8.0,
                     alto_piso=2.80, con_tejado=True)
```

### Generar un edificio de apartamentos
```python
# Edificio de 6 pisos, planta 12 × 15 m
A.crear_edificio_n_pisos('Edificio_Res', pisos=6,
                          ancho=12.0, fondo=15.0, alto_piso=2.80,
                          grosor_muro=0.20, grosor_losa=0.20,
                          material_muro='Muro_Pintura',
                          material_losa='Hormigon',
                          origen=(0, 0, 0))
```

---

## 9. Orientación de muros y ejes en el DSL

El DSL usa el sistema de coordenadas de Blender:
- **X** = ancho (Este–Oeste)
- **Y** = fondo/profundidad (Norte–Sur)
- **Z** = altura

| Fachada | Eje | `rotacion_z` en `crear_muro` |
|---|---|---|
| Sur (principal) | X, Y=0 | 0° |
| Norte (posterior) | X, Y=fondo | 0° |
| Este (lateral dcha) | Y, X=ancho | 90° |
| Oeste (lateral izq) | Y, X=0 | 90° |

> `crear_habitacion` genera los 4 muros automáticamente con la orientación correcta.
> Para layouts más complejos, combinar múltiples llamadas a `crear_habitacion`
> con diferentes `origen` y dimensiones.
