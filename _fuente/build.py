# -*- coding: utf-8 -*-
"""
Genera index.html del mockup del feed.

  python _fuente/build.py

Lee datos.json (las publicaciones y sus captions), tpl.html (el esqueleto)
y assets.json (las imagenes ya comprimidas en base64). Si una publicacion
trae "fuente" o "carrusel", sus imagenes se regeneran desde _fuente/artes/;
si no, se reutiliza lo que ya esta guardado en assets.json.
"""
import base64
import io
import json
import os
import re

from PIL import Image, ImageStat

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
ARTES = os.path.join(AQUI, "artes")

TOP = 250        # desde donde se recorta el cuadrado 1:1 de un arte 4:5
CORTE = 125      # donde Instagram corta el caption y pone "... mas"
UMBRAL = 170     # luminancia bajo la cual una miniatura cuenta como oscura

MES = {"ene": "enero", "feb": "febrero", "mar": "marzo", "abr": "abril",
       "may": "mayo", "jun": "junio", "jul": "julio", "ago": "agosto",
       "sep": "septiembre", "oct": "octubre", "nov": "noviembre", "dic": "diciembre"}
ANIO = 2026

IC = {
 "back": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5 8 12l7 7"/></svg>',
 "dots": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h.01M12 12h.01M19 12h.01"/></svg>',
 "heart": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20.3 3.9 12.2a4.9 4.9 0 0 1 '
          '6.9-6.9l1.2 1.2 1.2-1.2a4.9 4.9 0 0 1 6.9 6.9z"/></svg>',
 "chat": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 9 9 0 0 '
         '1-3.3-.6L3 21l1.8-5.2A8.3 8.3 0 0 1 3.6 11 8.4 8.4 0 0 1 12 3a8.4 8.4 0 0 1 9 8.5z"/></svg>',
 "send": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.5 2.5 2 9.9l7.6 2.6 2.6 7.6z"/>'
         '<path d="M21.5 2.5 9.6 12.5"/></svg>',
 "save": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h12v18l-6-4.6L6 21z"/></svg>',
 "caret": '<svg class="caret" viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>',
 "reel": '<svg class="carr-ic" viewBox="0 0 24 24" fill="#fff" aria-hidden="true">'
         '<path d="m9.5 8.6 6.4 3.4-6.4 3.4z"/></svg>',
 "pila": '<svg class="carr-ic" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.1" '
         'stroke-linejoin="round" aria-hidden="true"><rect x="7.6" y="3.6" width="12.8" height="12.8" '
         'rx="3"/><path d="M16.4 20.4h-8.8a4 4 0 0 1-4-4V7.6"/></svg>',
 "prev": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5 8 12l7 7"/></svg>',
 "next": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 5 7 7-7 7"/></svg>',
}


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def entidades(t):
    """Deja ASCII puro: todo lo demas pasa a entidad numerica, como el original."""
    sal = []
    for c in t:
        o = ord(c)
        sal.append(c if o < 128 else "&#x%X;" % o)
    return "".join(sal)


def uri(im, calidad):
    b = io.BytesIO()
    im.save(b, "WEBP", quality=calidad, method=6)
    return len(b.getvalue()), "data:image/webp;base64," + base64.b64encode(b.getvalue()).decode()


def larga(dia):
    n, mes = dia.split()
    return "%s de %s de %d" % (n, MES[mes], ANIO)


def luminancia(data_uri):
    crudo = base64.b64decode(data_uri.split(",", 1)[1])
    im = Image.open(io.BytesIO(crudo)).convert("L")
    return round(ImageStat.Stat(im).mean[0], 1)


# ---------------------------------------------------------------- datos
D = json.load(io.open(os.path.join(AQUI, "datos.json"), encoding="utf-8"))
A = json.load(io.open(os.path.join(AQUI, "assets.json"), encoding="utf-8"))
POSTS = D["posts"]
PIE = D["pie"]

# ------------------------------------------------- imagenes que se regeneran
kb_mini = kb_arte = 0
for p in POSTS:
    k = p["clave"]
    laminas = p.get("carrusel")
    fuente = p.get("fuente") or (laminas[0] if laminas else None)

    if fuente:
        im = Image.open(os.path.join(ARTES, fuente)).convert("RGB")
        W, H = im.size
        lado = min(W, H)
        y = min(TOP, H - lado)
        n, A[k] = uri(im.crop((0, y, lado, y + lado)).resize((360, 360), Image.LANCZOS), 82)
        kb_mini += n
        n, A["big_" + k] = uri(im.resize((520, 650), Image.LANCZOS), 80)
        kb_arte += n

    if laminas:
        for i, fn in enumerate(laminas):
            lam = Image.open(os.path.join(ARTES, fn)).convert("RGB")
            n, A["carr_%s_%d" % (k, i)] = uri(lam.resize((520, 650), Image.LANCZOS), 76)
            kb_arte += n

    assert k in A and "big_" + k in A, "faltan las imagenes de %s" % k

json.dump(A, io.open(os.path.join(AQUI, "assets.json"), "w", encoding="utf-8"))

# ---------------------------------------------------------------- armado
tiles, filas, articulos = [], [], []

for i, p in enumerate(POSTS, 1):
    k, t = p["clave"], p["titulo"]
    cap = p["caption"] + PIE
    oscura = luminancia(A[k]) < UMBRAL

    icono = IC["reel"] if "video" in p else (IC["pila"] if "carrusel" in p else "")
    tiles.append('<button class="tile" type="button" data-pos="%d" '
                 'aria-label="Abrir publicaci&oacute;n: %s"><img src="%s" alt="%s">%s</button>'
                 % (i, entidades(esc(t)), A[k], entidades(esc(t)), icono))

    # el bloque visual: video, carrusel o arte suelto
    if "video" in p:
        medio = ('<video class="post-vid" controls playsinline preload="metadata" '
                 'poster="%s" src="%s"></video>' % (A["big_" + k], p["video"]))
    elif "carrusel" in p:
        n = len(p["carrusel"])
        lams = "".join('<img src="%s" alt="%s, l&aacute;mina %d de %d">'
                       % (A["carr_%s_%d" % (k, j)], entidades(esc(t)), j + 1, n) for j in range(n))
        puntos = "".join('<span%s></span>' % (' class="on"' if j == 0 else "") for j in range(n))
        medio = ('<div class="carr" data-n="%d"><div class="carr-track">%s</div>'
                 '<button class="carr-nav prev" type="button" aria-label="L&aacute;mina anterior" hidden>%s</button>'
                 '<button class="carr-nav next" type="button" aria-label="L&aacute;mina siguiente">%s</button>'
                 '<span class="carr-n">1/%d</span><div class="carr-dots">%s</div></div>'
                 % (n, lams, IC["prev"], IC["next"], n, puntos))
    else:
        medio = '<img class="post-art" src="%s" alt="%s">' % (A["big_" + k], entidades(esc(t)))

    c1, c2 = cap[:CORTE], cap[CORTE:]
    articulos.append(
        '<article class="post" id="post-%d" aria-label="Publicaci&oacute;n: %s">'
        '<div class="post-nav"><button class="post-back" type="button" '
        'aria-label="Volver al perfil">%s</button><b>Publicaciones</b></div>'
        '<div class="post-hd"><img src="%s" alt=""><b>agenciajehandal</b>%s</div>'
        '%s'
        '<div class="post-acts">%s%s%s<span class="save">%s</span></div>'
        '<p class="post-likes">&nbsp;</p>'
        '<p class="post-tx"><b>agenciajehandal</b> <span class="c1">%s</span>'
        '<button class="post-mas" type="button">&#x2026; m&aacute;s</button>'
        '<span class="c2" hidden>%s</span></p>'
        '<p class="post-fecha">%s</p></article>'
        % (i, entidades(esc(t)), IC["back"], A["avatar"], IC["dots"], medio,
           IC["heart"], IC["chat"], IC["send"], IC["save"],
           entidades(esc(c1)), entidades(esc(c2)), entidades(esc(larga(p["dia"])))))

    chip = ('<span class="chip o">Oscuro</span>' if oscura
            else '<span class="chip c">Claro</span>')
    filas.append(
        '<li class="row" data-pos="%d"><button class="row-hd" type="button" '
        'aria-expanded="false" aria-controls="cap-%d"><span class="n">%02d</span>'
        '<span class="t"><b>%s</b><span>%s<em>%s</em></span></span>%s%s</button>'
        '<div class="cap" id="cap-%d" hidden><div class="cap-bar">'
        '<span class="cap-lbl">Caption</span><span class="cap-n">%d caracteres</span>'
        '<button class="cap-copy" type="button">Copiar</button></div>'
        '<p class="cap-tx">%s</p></div></li>'
        % (i, i, i, entidades(esc(t)), entidades(esc(p["meta"])), entidades(esc(p["dia"])),
           chip, IC["caret"], i, len(cap), entidades(esc(cap))))

destacados = "".join(
    '<div class="hl-item"><div class="hl-ring"><img src="%s" alt=""></div><span>%s</span></div>'
    % (A["hl_" + k], entidades(esc(nombre))) for k, nombre in D["highlights"])

# ---------------------------------------------------------------- salida
html = io.open(os.path.join(AQUI, "tpl.html"), encoding="utf-8").read()
for marca, trozo in [("TILES_HERE", "".join(tiles)),
                     ("ROWS_HERE", "".join(filas)),
                     ("POSTS_HERE", "".join(articulos)),
                     ("HIGHLIGHTS_HERE", destacados)]:
    assert marca in html, "falta el marcador %s en tpl.html" % marca
    html = html.replace(marca, trozo, 1)
html = html.replace("AVATAR_SRC", A["avatar"])

n_filas = (len(POSTS) + 2) // 3
html = re.sub(r'<p class="sub">.*?</p>',
              '<p class="sub">%s</p>' % entidades(esc(D["sub"])), html, count=1, flags=re.S)
html = re.sub(r'(<meta name="description" content=")[^"]*(")',
              lambda m: m.group(1) + entidades(esc(D["descripcion"])) + m.group(2), html, count=1)
html = re.sub(r'(<meta property="og:description" content=")[^"]*(")',
              lambda m: m.group(1) + entidades(esc(D["descripcion"])) + m.group(2), html, count=1)
html = re.sub(r'<span class="lbl">[^<]*</span>',
              '<span class="lbl">%d publicaciones en %d filas</span>' % (len(POSTS), n_filas),
              html, count=1)

salida = os.path.join(REPO, "index.html")
io.open(salida, "w", encoding="utf-8").write(html)

print("miniaturas %3d kB | artes y laminas %4d kB" % (kb_mini // 1024, kb_arte // 1024))
print("index.html: %.2f MB" % (os.path.getsize(salida) / 1048576.0))
print("publicaciones: %d | filas: %d" % (len(POSTS), n_filas))
oscuras = [p["clave"] for p in POSTS if luminancia(A[p["clave"]]) < UMBRAL]
print("oscuras: %s | claras: %d" % (oscuras, len(POSTS) - len(oscuras)))
