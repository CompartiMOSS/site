# Revista CompartiMOSS 

## ¿Deseas colaborar con CompartiMOSS?

La subsistencia del magazine depende de los aportes en contenido de todos. Por ser una revista dedicada a información sobre tecnología Microsoft en español, todo el contenido deberá ser directamente relacionado con esa tecnología y escrito en castellano. No hay limitaciones sobre el tipo de articulo o contenido, lo mismo que sobre el tipo de versión. Si desea publicar algo, por favor, utilice uno de los siguientes formatos:

- Artículos de fondo: tratan sobre un tema en profundidad. Normalmente entre 2000 y 3000 palabras y alrededor de 4 o 5 figuras. El tema puede ser puramente técnico, tanto de programación como sobre infraestructura, o sobre implementación o utilización.

- Artículos cortos: Máximo 1000 palabras y 1 o 2 figuras. Describen rápidamente una aplicación especial de SharePoint, o explica algún punto poco conocido o tratado. Experiencias de aplicación de SharePoint en empresas o instituciones puede ser un tipo de artículo ideal en esta categoría.

- Ideas, tips y trucos: Algunos cientos de palabras máximo. Experiencias sobre la utilización de SharePoint, problemas encontrados y como solucionarlos, ideas y trucos de utilización, etc.

Los formatos son para darle una idea sobre cómo organizar su información, y son una manera para que los editores le den forma al magazine, pero no son obligatorios. Los artículos deben ser enviados en formato Word (.doc o .docx), utilizando la plantilla por defecto de Word (normal.dot) sin ninguna modificación (no utilice columnas o tipos especiales de letras) con el nombre del autor y del artículo. Si desea escribir un artículo de fondo o corto, preferiblemente envíe una proposición antes de escribirlo, indicando el tema, aproximada longitud y número de figuras. De esta manera evitaremos temas repetidos y permitirá planear el contenido de una forma efectiva. Envíe sus proposiciones, artículos, ideas y comentarios a revista@compartimoss.com. 

## Tecnología 

Este repositorio contiene el código y contenido del sitio **CompartiMOSS**, construido con **Hugo**.

- Producción: https://www.compartimoss.com/
- Tema: `themes/compartimoss/`
- Contenido: `content/`

## Ejecutar en local

Requisitos:

- **Git**
- **Hugo** (recomendado: *Hugo Extended*)

Comandos útiles desde la raíz del repositorio:

- Desarrollo (incluye borradores): `hugo server -D`
- Build: `hugo`

Notas:

- `public/` es salida de build y está en `.gitignore` (no lo incluyas en commits/PRs).

## Estructura del repositorio

- `content/articulos/`: artículos
- `content/autores/`: perfiles de autores
- `content/revistas/`: números de la revista
- `static/`: assets estáticos servidos tal cual
- `public/`: salida de build (generado)

## Contribuir

Para proponer artículos o cambios, consulta la guía: `CONTRIBUTING.MD`.

Preguntas frecuentes: [FAQs.md](FAQs.md)

