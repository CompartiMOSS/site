# Contribuir a CompartiMOSS

Gracias por tu interés en colaborar con la revista.

Aceptamos contribuciones en forma de artículos (y mejoras puntuales del sitio). El flujo de trabajo es el habitual en GitHub: fork → cambios en una rama → Pull Request para revisión editorial.

## Requisitos

- **Git**
- **Hugo** (recomendado: *Hugo Extended*)

## Previsualizar el sitio en local

Desde la raíz del repositorio:

- Servidor de desarrollo: `hugo server -D`
- Build (genera `public/`): `hugo`

Notas:

- `public/` es salida de build y está en `.gitignore` (no lo incluyas en el PR).
- Si necesitas ver borradores, usa `-D`.

## Escribir un artículo

### 1) Haz un fork y crea una rama

1. Haz un **fork** de este repositorio en tu cuenta.
2. Clónalo en tu máquina.
3. Crea una rama descriptiva (ej.: `articulo/mi-tema`).

### 2) Crea (o reutiliza) tu perfil de autor

Los autores viven en `content/autores/`.

- Si ya existes, localiza tu fichero y reutiliza su `authorSlug`.
- Si no existes, crea `content/autores/<authorSlug>.md` siguiendo el estilo de los demás.

El avatar suele referenciarse así:

- `avatar: ./images/<authorSlug>.png`

Y la imagen se guarda en:

- `content/autores/images/<authorSlug>.png`

### 3) Añade el artículo en Markdown

Crea un fichero en:

- `content/articulos/<slug-del-articulo>.md`

Convenciones recomendadas:

- `<slug-del-articulo>` en *kebab-case* (minúsculas y guiones).
- Un artículo = un fichero `.md`.

#### Plantilla de front matter

Usa la misma estructura que el resto de artículos existentes:

```yaml
---
title: "Título del artículo por Nombre Apellido"
date: 2025-12-14
excerpt: "Resumen corto (1-2 frases)."
author: "Nombre Apellido"
authorSlug: "mi-slug-de-autor"
image: "https://..." # o una ruta a una imagen local (ver siguiente sección)
category: "Categoría"
---
```

Campos importantes:

- `authorSlug` debe coincidir con el fichero de autor en `content/autores/`.
- `excerpt` se usa como resumen/listado, cuídalo.
- `category` debe ser una categoría clara y consistente.

### 4) Imágenes del artículo

Para imágenes **en el repositorio** (en vez de URLs externas), guárdalas aquí:

- `content/imagenes/<slug-del-articulo>/` (una carpeta por artículo)

Y enlázalas desde el Markdown usando una ruta relativa desde `content/articulos/`:

```md
![Texto alternativo](../imagenes/<slug-del-articulo>/mi-imagen.png)
```

Recomendaciones:

- Nombra los ficheros en *kebab-case* (`diagrama-arquitectura.png`).
- Usa imágenes optimizadas (peso razonable) y añade siempre **texto alternativo**.
- Evita imágenes con datos sensibles (tokens, correos privados, etc.).

### 5) Abre un Pull Request (PR)

Cuando lo tengas listo, abre un **PR** contra la rama principal para revisión por el equipo editorial.

Checklist antes de abrir el PR:

- El sitio compila y el artículo se ve bien con `hugo server -D`.
- El artículo tiene `title`, `date`, `excerpt`, `author`, `authorSlug`, `category`.
- Si usas imágenes locales, están en `content/imagenes/<slug-del-articulo>/` y los enlaces funcionan.
- No incluyes `public/` ni artefactos generados.

Qué esperar en la revisión:

- Los editores pueden pedir ajustes de estilo, claridad, enlaces, imágenes o formato.
- Si todo está OK, se aprobará y se publicará según la planificación editorial.

## Ayuda

Si tienes dudas (estructura, `authorSlug`, categorías, imágenes, etc.), abre un Issue o deja una nota en el PR explicando lo que necesitas.
