# Feed Septiembre 2026 — Agencia J. E. Handal

Presentación del feed de Instagram de septiembre: los doce artes montados en la
parrilla real de Instagram, vista desde la pantalla de un celular, con el caption
de cada publicación y la fecha sugerida.

**Al tocar cualquier arte de la parrilla se abre la publicación completa**, como en
Instagram: el arte en su formato original 4:5 (no el recorte cuadrado), la fila de
acciones, los «Me gusta» y el caption cortado justo donde Instagram lo corta, con su
«… más» para expandirlo. Se vuelve con la flecha de atrás o con la tecla Esc.

Sitio estático, sin dependencias ni proceso de compilación. Las veinticuatro imágenes
—doce recortes cuadrados y doce artes completos— y el logo van incrustados dentro de
`index.html`, así que el archivo se abre solo, incluso sin conexión.

## Contenido

| Archivo | Para qué sirve |
|---|---|
| `index.html` | La presentación completa (1.3 MB) |
| `og.png` | Miniatura que aparece al compartir el enlace por WhatsApp, Facebook o LinkedIn |
| `icon.png` | Ícono de la pestaña del navegador |
| `netlify.toml` | Encabezados de caché y bloqueo de buscadores |
| `robots.txt` | Impide que los buscadores indexen la presentación |

## Publicar en Netlify

### Opción 1 — arrastrar la carpeta (la más rápida, sin cuenta técnica)

1. Entre a **app.netlify.com/drop**
2. Arrastre **esta carpeta completa** (`feed-jehandal-netlify`) a la ventana
3. Netlify le devuelve un enlace tipo `https://algo-random-123.netlify.app`
4. En *Site configuration → Change site name* le puede poner algo legible,
   por ejemplo `feed-jehandal-septiembre`

Ese enlace ya se puede repartir. Cualquiera que lo tenga entra sin contraseña.

### Opción 2 — línea de comandos

Requiere Node.js instalado.

```bash
npm install -g netlify-cli
```

```bash
netlify deploy --dir "C:\Claude\mockups\feed-jehandal-netlify" --prod
```

## Actualizar

Cambie `index.html` y vuelva a arrastrar la carpeta (o repita el `netlify deploy`).
Se mantiene la misma dirección.

## Dos ajustes que puede necesitar

**Si la miniatura no sale en WhatsApp.** Algunos lectores de enlaces exigen una
dirección absoluta. Abra `index.html`, busque la línea:

```html
<meta property="og:image" content="og.png">
```

y reemplácela por la dirección completa de su sitio ya publicado:

```html
<meta property="og:image" content="https://SU-SITIO.netlify.app/og.png">
```

**Si quiere restringir quién entra.** El enlace de Netlify es público para quien lo
tenga. Para pedir contraseña se necesita el plan Pro de Netlify
(*Site configuration → Access control → Password protection*).

---

## Notas de revisión

Se quitaron de la presentación por pedido, pero conviene tenerlas a mano al momento
de programar las publicaciones.

**1. Instagram es cronológico: la casilla 01 es lo último que se publica.**
La bandera va el 1 de septiembre, así que en la parrilla queda de última
(casilla 12), no de primera. La independencia, sexta publicación del mes, cae
en la casilla 07. Si prefiere leer la ficha como calendario en vez de como
parrilla, se invierte el orden completo.

**2. El tablero de ajedrez queda perfecto: cero vecindades del mismo tono.**
Midiendo el brillo de cada recorte cuadrado, los artes con el logo de Atria se
parten en 6 oscuros y 6 claros exactos —el corte natural cae entre 160.5 y
185.7—, y con esa proporción sí existe alternancia perfecta en una parrilla de
3×4. En la versión anterior eran 7 claros y 5 oscuros y sobraba un claro, así
que quedaban dos vecindades iguales en la esquina inferior. Ya no.

LZ-2290C (150.1) y W3600P/W3500P (160.5) son los dos «medios» del grupo oscuro:
no son azul sólido como LH-4500C o MXneo, pero leen claramente más oscuros que
los de fondo blanco. Si algún arte se rediseña, vuelva a medir antes de reordenar.

**3. Las parejas que se confunden quedan lejos.**
W500P/W600P y W3600P/W3500P son casi idénticas en miniatura: van en 04 y 09.
Lo mismo EX Series y MXneo, las dos overlock oscuras: 11 y 01, en esquinas
opuestas. Y ninguna fila queda de una sola marca.

**4. Las historias destacadas ya usan las portadas definitivas.**
Son los cuatro PNG de `Desktop\Septiembre\Highlights Instagram`, montados a 198 px
(3× los 66 px que mide el círculo en pantalla). Los nombres —Ubicación, Contactos,
Marcas, Servicios— caben dentro de los ~10 caracteres que muestra Instagram, así
que ninguno se corta. Si más adelante agrega otro, respete ese límite: «Misión y
Visión» o «Marcas que Distribuimos» aparecerían truncados.

**5. La miniatura cuadrada recorta el arte.**
Con 2160×2700 (4:5), el recorte 1:1 centrado se come 270 px arriba y abajo: se
pierde parte del logo superior y de la barra de contacto. Al arte de la Bandera
se le ancló el recorte abajo para salvar el logo. Al publicar, ajuste el
encuadre de cada miniatura o diseñe una versión 1:1 del cabezal.

**6. Instagram corta el caption a unos 125 caracteres.**
Todos los captions pasan de 190, así que la línea 👉 y la de contacto quedan
detrás de «…más». Por eso el modelo va en el primer renglón: es lo único
garantizado a la vista.

**7. Cifras de relleno.**
Las fechas son una cadencia sugerida, días hábiles, cada 2–4 días; las dos fechas
patrias son las únicas fijas. Seguidores, seguidos y los «Me gusta» de cada
publicación son números de relleno para el mockup, no datos reales de la cuenta.

**8. La bandera 🇭🇳 se ve como «HN» en Windows.**
No es un error del archivo: Windows no trae los glifos de banderas de países, así
que Chrome y Edge muestran las dos letras. En iPhone y Android sale la bandera
correcta, y en Instagram también. No cambie el caption por esto.

**9. Los artes llevan el logo de Grupo Atria.**
Los diez artes de máquina se actualizaron el 28 de agosto con el logo de Atria
en la esquina superior izquierda; los dos de fecha patria no lo llevan. El de
coverstitch además cambió de nombre: ahora dice **W3600P / W3500P**, en ese
orden, y así quedó en la ficha y en su caption.

**10. Pendiente de marca.**
`icon.png` es el logo horizontal metido en un cuadro blanco, que a 32 px se lee
apenas. Vale la pena encargar una versión cuadrada del logo para íconos y avatar.
