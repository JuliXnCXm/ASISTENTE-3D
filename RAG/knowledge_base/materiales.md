# Materiales disponibles — DSL blender_arch

Estos son los nombres válidos para el parámetro `material=` en las funciones del DSL.
El sistema crea materiales Blender con color base (BSDF Principled) y nombre exactamente
igual al string indicado. Si el material ya existe en la escena, se reutiliza.

Uso: `A.crear_muro('Muro_1', material='Hormigon')`

---

## Estructurales y obra gris

| Nombre (string exacto) | Descripción | Color base aprox. |
|---|---|---|
| `Hormigon` | Concreto liso, gris medio | #9E9E9E |
| `Hormigon_Visto` | Concreto con textura aparente | #8C8C8C |
| `Mamposteria` | Ladrillo común / bloque gris | #A0887A |
| `Ladrillo` | Ladrillo a la vista, tono rojizo | #B5603A |
| `Ladrillo_Rojo` | Ladrillo artesanal, rojo intenso | #C0522A |
| `Bloque_Concreto` | Bloque de hormigón, gris claro | #AEAEAE |
| `Adobe` | Adobe / tapia, tierra cruda | #C4A882 |
| `Acero` | Acero estructural, gris metálico | #707070 |
| `Acero_Galvanizado` | Acero galvanizado, plateado | #C0C0C0 |
| `Acero_Inox` | Acero inoxidable, brillante | #D4D4D4 |
| `Aluminio` | Perfil de aluminio | #BDBDBD |

---

## Acabados de muros y cielos

| Nombre | Descripción | Color base aprox. |
|---|---|---|
| `Muro_Pintura` | Muro con pintura blanca mate | #F5F5F5 |
| `Muro_Pintura_Gris` | Muro con pintura gris claro | #DCDCDC |
| `Muro_Pintura_Beige` | Muro con pintura beige cálido | #EDE0C8 |
| `Estuco` | Estuco liso, blanco roto | #EFEFEF |
| `Estuco_Textura` | Estuco rugoso / grafiado | #E0D8CC |
| `Pintura_Blanca` | Pintura blanca pura | #FFFFFF |
| `Pintura_Crema` | Pintura crema / marfil | #FFF8E7 |
| `Enchape_Ceramica` | Cerámica de pared, blanca | #F8F8F8 |
| `Enchape_Metro` | Subway tile blanco brillante | #FAFAFA |
| `Yeso` | Yeso o drywall, blanco | #F2F2F2 |

---

## Pisos y suelos

| Nombre | Descripción | Color base aprox. |
|---|---|---|
| `Piso_Madera` | Piso de madera genérico, castaño | #A0724A |
| `Parquet` | Parquet de roble, tono claro | #C8A96E |
| `Parquet_Oscuro` | Parquet wengué / oscuro | #5C3A1E |
| `Madera_Pino` | Madera de pino, amarillo claro | #D4B896 |
| `Ceramica_Piso` | Baldosa cerámica gris claro | #C8C8C0 |
| `Ceramica_Blanca` | Baldosa blanca lisa | #F0F0F0 |
| `Porcelanato` | Porcelanato pulido, gris frio | #D8D8D8 |
| `Porcelanato_Marmol` | Porcelanato imitación mármol | #F0EDEA |
| `Concreto_Piso` | Piso de concreto pulido | #B0B0A8 |
| `Vinilo` | Piso vinílico, beige | #D4C4A8 |
| `Alfombra` | Alfombra, gris medio | #9E9E9E |
| `Alfombra_Beige` | Alfombra beige / arena | #D4C8A8 |
| `Losacero` | Losa colaborante / steel deck | #787878 |
| `Piso_Exterior` | Piso exterior / andén, gris | #A8A89C |
| `Adoquin` | Adoquín gris / beige | #B4ADA0 |
| `Gravilla` | Gravilla suelta | #C0B8A8 |
| `Cesped` | Pasto / césped verde | #5A8A3C |
| `Tierra` | Tierra / suelo natural | #8B6340 |

---

## Cubiertas y techos

| Nombre | Descripción | Color base aprox. |
|---|---|---|
| `Teja` | Teja de barro / arcilla, terracota | #B55A30 |
| `Teja_Zinc` | Teja de zinc corrugado, plateado | #B0B0B0 |
| `Teja_Asfalt` | Shingle asfáltico, gris oscuro | #5A5A5A |
| `Cubierta_Verde` | Cubierta verde / jardín | #5A8A3C |
| `Membrana_Imperm` | Membrana impermeabilizante negra | #2A2A2A |
| `Panel_Sandwich` | Panel sándwich metálico | #C8C8C8 |

---

## Madera (mobiliario y acabados)

| Nombre | Descripción | Color base aprox. |
|---|---|---|
| `Madera` | Madera genérica, castaño medio | #9C6B3C |
| `Madera_Roble` | Roble natural, dorado claro | #C4904A |
| `Madera_Nogal` | Nogal, marrón cálido | #7A4E2D |
| `Madera_Wengue` | Wengué, marrón muy oscuro | #3C2010 |
| `Madera_Pino` | Pino, amarillo pálido | #D4B896 |
| `Madera_Barniz` | Madera barnizada, brillante | #A87840 |
| `MDF_Blanco` | MDF lacado en blanco | #F8F8F8 |
| `MDF_Gris` | MDF lacado en gris | #DCDCDC |
| `Melanina_Blanca` | Melamina blanca | #FAFAFA |
| `Melanina_Gris` | Melamina gris | #D8D8D8 |

---

## Vidrio y transparentes

| Nombre | Descripción | Transmisión |
|---|---|---|
| `Vidrio` | Vidrio claro, transparente | ~90% |
| `Vidrio_Templado` | Vidrio templado, ligeramente azulado | ~88% |
| `Vidrio_Esmerilado` | Vidrio esmerilado, translúcido difuso | ~60% |
| `Vidrio_Tintado` | Vidrio tintado gris oscuro | ~40% |
| `Policarbonato` | Policarbonato translúcido | ~70% |

> Nota: En el DSL, `crear_ventana` acepta `material_vidrio=` y `material_marco=` por separado.
> Ejemplo: `material_vidrio='Vidrio_Templado'`, `material_marco='Marco_Blanco'`

---

## Marcos, perfiles y herrajes

| Nombre | Descripción | Color base aprox. |
|---|---|---|
| `Marco_Blanco` | Marco de ventana/puerta blanco | #F5F5F5 |
| `Marco_Negro` | Marco negro / aluminio anodizado | #2A2A2A |
| `Marco_Aluminio` | Marco aluminio anodizado natural | #BDBDBD |
| `Marco_Madera` | Marco de madera natural | #9C6B3C |
| `PVC_Blanco` | Perfil PVC blanco | #F8F8F8 |

---

## Textiles y tapizados

| Nombre | Descripción | Color base aprox. |
|---|---|---|
| `Tela_Gris` | Tapizado tela gris medio | #9E9E9E |
| `Tela_Beige` | Tapizado tela beige | #D4C8A8 |
| `Tela_Azul` | Tapizado tela azul navy | #3A5478 |
| `Cuero` | Tapizado cuero marrón | #7A4E2D |
| `Cuero_Negro` | Tapizado cuero negro | #1E1E1E |
| `Textil_Blanco` | Ropa de cama / colchón blanco | #F5F5F5 |
| `Tela_Verde` | Tapizado tela verde | #4A7A4A |

---

## Metales decorativos y sanitarios

| Nombre | Descripción | Color base aprox. |
|---|---|---|
| `Cobre` | Tubería de cobre | #B87333 |
| `Bronce` | Acabado bronce | #A07020 |
| `Metal` | Metal genérico pintado gris | #787878 |
| `Metal_Negro` | Metal negro mate | #2A2A2A |
| `Concreto` | Alias de Hormigon (uso en perfiles) | #9E9E9E |

---

## Exterior y terreno

| Nombre | Descripción | Color base aprox. |
|---|---|---|
| `Terreno` | Suelo / terreno natural, café | #8B6340 |
| `Asfalto` | Pavimento asfáltico | #3C3C3C |
| `Concreto_Gris` | Piso de concreto exterior | #AEAEAE |
| `Agua` | Agua / piscina, azul translúcido | #3A9ECC |

---

## Uso en el DSL — referencia rápida

```python
import blender_arch as A

# Muro con acabado de ladrillo visto
A.crear_muro('Fachada', largo=8, alto=3, grosor=0.2, material='Ladrillo_Rojo')

# Ventana con vidrio templado y marco de aluminio
A.crear_ventana('V1', ancho=1.5, alto=1.1, material_vidrio='Vidrio_Templado',
                material_marco='Marco_Aluminio')

# Piso de parquet en sala
A.crear_piso('Piso_Sala', ancho=5, fondo=4, espesor=0.02, material='Parquet')

# Tejado de teja de barro
A.crear_tejado_dos_aguas('Tejado', ancho=8, fondo=6, altura_cumbrera=1.8,
                          material='Teja')

# Sofá tapizado en tela gris
A.crear_sofa('Sofa', ancho=2.2, material='Tela_Gris')

# Tubería de cobre (instalaciones)
A.crear_tuberia('TB_Agua', puntos_3d=[(0,0,0.3),(0,4,0.3)],
                radio=0.025, material='Cobre')
```
