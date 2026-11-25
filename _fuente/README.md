# Fuente del mockup

El `index.html` de la raíz **no se edita a mano**: es el resultado de este
generador. Para cambiar algo del feed, se toca lo de aquí y se vuelve a generar.

```bash
python _fuente/build.py
```

## Qué hay aquí

| Archivo | Qué es |
|---|---|
| `build.py` | El generador. Arma el `index.html` de la raíz. |
| `datos.json` | Las publicaciones: orden, títulos, fechas y captions. **Es lo que se edita.** |
| `tpl.html` | El esqueleto de la página: todo el HTML, el CSS y el JavaScript. |
| `assets.json` | Las imágenes ya comprimidas, en base64. Lo escribe el propio generador. |
| `artes/` | Los archivos originales de los artes que el generador vuelve a comprimir. |

## Cómo se agrega o cambia una publicación

Todo vive en `datos.json`, dentro de `posts`. El orden del arreglo es el orden
de la parrilla: **el primero es el más reciente** y sale arriba a la izquierda,
igual que en Instagram.

```jsonc
{
  "clave":   "w3500p",                    // identificador interno, sin espacios
  "titulo":  "W3500P / W3600P",           // lo que se lee en la fila y en la miniatura
  "meta":    "Pegasus · collaretera DD",  // la línea gris de la fila
  "dia":     "23 nov",                    // día y mes en tres letras; el año sale de ANIO
  "caption": "…",                         // sin el pie de contacto: se agrega solo
  "fuente":  "w3500p.jpg",                // opcional: un arte dentro de artes/
  "video":   "video/morgan.mp4",          // opcional: lo vuelve un Reel
  "carrusel": ["s0.jpg", "s1.jpg"]        // opcional: lo vuelve un carrusel
}
```

Reglas que el generador aplica solo:

- **El pie de contacto** (`pie` en `datos.json`) se le pega a todos los captions.
  No hay que escribirlo en cada uno.
- **El corte de Instagram** cae a los 125 caracteres. Conviene redactar el
  caption para que a esa altura termine una frase, no una palabra a medias.
- **Claro u oscuro** se mide, no se decide: el generador saca la luminancia de
  la miniatura y marca oscura la que baja de 170.
- **El icono** de la miniatura sale del tipo: Reel si hay `video`, pila de
  láminas si hay `carrusel`, nada si es un arte suelto.

Si una publicación **no** trae `fuente` ni `carrusel`, el generador reutiliza la
imagen que ya está guardada en `assets.json`. Así siguen funcionando las
publicaciones cuyo arte original ya no está en disco.

## Los artes que faltan

Los originales de los cuatro artes de producto (Pegasus, Repuestos, Juki y
Brother) y las portadas de los dos videos **se perdieron** cuando Windows limpió
la carpeta temporal donde vivía el generador anterior. Lo que sobrevive es la
versión comprimida que está dentro de `assets.json`: 360×360 para la miniatura y
520×650 para la vista de la publicación. Alcanza para el mockup, pero no para
volver a renderizar en grande.

Si vuelven a aparecer los originales, se dejan en `artes/` y se les agrega
`"fuente": "<archivo>"` a su publicación en `datos.json`.
