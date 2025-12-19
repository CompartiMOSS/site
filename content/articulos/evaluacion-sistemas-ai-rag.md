---
title: "Evaluación de sistemas AI RAG"
date: 2025-05-20
excerpt: "Cómo evaluar sistemas de IA, en particular arquitecturas basadas en RAG, usando el ecosistema .NET y la biblioteca Microsoft.Extensions.AI.Evaluation."
author: "Luis Mañez"
authorSlug: "luis-manez"
image: "../images/evaluacion-sistemas-ai-rag/picture1.png"
category: "AI"
---

A medida que la adopción de la IA sigue acelerándose, las organizaciones dependen cada vez más de los Large Language Models (LLMs) para alimentar aplicaciones inteligentes —desde chatbots hasta copilotos y asistentes de conocimiento—. Pero crear un sistema de IA es solo el principio. Uno de los aspectos más críticos, y a menudo pasados por alto, del ciclo de vida de desarrollo de IA es la evaluación: comprender el rendimiento del sistema, identificar modos de fallo y tomar decisiones fundamentadas sobre modelos, prompts y arquitectura.

Esto resulta aún más crucial cuando se trabaja con sistemas de Retrieval-Augmented Generation (RAG), donde un modelo de lenguaje se combina con una fuente de conocimiento externa para mejorar la relevancia y reducir las alucinaciones. Los sistemas RAG introducen nuevas variables —como la calidad de recuperación de documentos y la consistencia del “grounding”— que hacen que los métodos tradicionales de evaluación sean insuficientes.

En esta entrada recorreremos cómo evaluar sistemas de IA, en particular arquitecturas basadas en RAG, usando el ecosistema .NET y la biblioteca Microsoft.Extensions.AI.Evaluation. Cubriremos criterios de evaluación, los retos exclusivos de los sistemas RAG y cómo crear una canalización de evaluación estructurada y repetible para obtener información profunda sobre el comportamiento de tu IA.

## ¿Qué queremos decir con «evaluación»?
Cuando hablamos de evaluar sistemas de IA, no nos referimos solo a precisión, recall o puntuaciones BLEU. Esas métricas tradicionales —aunque útiles en ciertos contextos— no captan toda la complejidad de las interacciones con los LLM modernos, especialmente en entornos RAG.

La evaluación en este contexto consiste en valorar cualitativamente cuánto satisface el sistema las expectativas del usuario. Se trata de responder preguntas como:

- ¿La respuesta ayuda realmente al usuario?
- ¿La información es precisa, completa y está bien estructurada?
- ¿Un modelo o prompt distinto podría mejorar el resultado?
- ¿El componente de recuperación aporta el conocimiento adecuado para respaldar la respuesta?

Estas preguntas van más allá del rendimiento puro del modelo y entran en el ámbito de la calidad extremo-a-extremo.

Por ejemplo, puedes tener un LLM excelente, pero si los documentos recuperados no son relevantes, la salida seguirá siendo pobre. O puedes obtener una respuesta fácticamente correcta que resulte difícil de leer, incoherente o engañosa por matices sutiles.

Por eso la evaluación debe ser holística, considerando no solo lo que produce el modelo, sino también cómo llega a ello y si tiene sentido desde la perspectiva del usuario y del negocio. En la práctica, esto implica definir un conjunto claro de criterios, aplicarlos de forma coherente y analizar los resultados en distintas configuraciones, modelos o prompts. No se trata solo de obtener una puntuación, sino de construir confianza en tu sistema de IA.

## Criterios de evaluación comunes en los sistemas de IA

![Criterios de evaluación.](../images/evaluacion-sistemas-ai-rag/picture1.png)

A continuación, los criterios clave que utilizamos:
- Relevancia
¿La respuesta es útil y está en contexto con la pregunta?
Ejemplo: preguntas por Azure OpenAI y la respuesta habla de AWS SageMaker → Pobre relevancia.
- Veracidad
¿Los hechos son correctos?
Ejemplo: el modelo da la fecha de lanzamiento equivocada de .NET 8 → Pobre veracidad.
- Integridad
¿La respuesta cubre todos los aspectos importantes?
Ejemplo: una guía de despliegue que omite pasos clave → Pobre integridad.
- Fluidez
¿El lenguaje es gramaticalmente correcto y fácil de entender?
Ejemplo: «Modelo entrenar Azure subir luego funciona.» → Pobre fluidez.
- Coherencia
¿Las ideas tienen sentido y fluyen lógicamente?
Ejemplo: una respuesta que se contradice a sí misma → Pobre coherencia.
- Equivalencia
¿Dos respuestas distintas expresan el mismo significado, aunque se formulen de otra manera?
Útil al comparar variantes de modelo o al evaluar paráfrasis.
- Groundedness
¿La respuesta se basa en información verificable (p. ej. documentos recuperados) o alucina?
Especialmente importante en RAG, donde el grounding es un objetivo clave.

Cada una de estas dimensiones ofrece una perspectiva diferente para comprender la calidad del sistema, y muchas herramientas de evaluación —incluida la que exploraremos más adelante— las admiten de forma nativa.

![](../images/evaluacion-sistemas-ai-rag/picture2.png)

Retos de evaluación en los sistemas RAG
- El problema de la doble canalización
En RAG no solo se evalúa un modelo; se evalúa un pipeline. Una mala respuesta puede deberse al modelo, al recuperador o a ambos.
- Grounding alucinado
A veces la IA inventa contenido y lo atribuye falsamente a documentos recuperados. Detectarlo requiere revisión manual o evaluadores personalizados.
- La calidad de recuperación es difícil de puntuar
Un documento puede parecer relevante para un buscador, pero ser inútil en contexto.
- Compromisos coste-rendimiento
Evaluar distintas configuraciones (modelos, temperaturas, estilos de prompt) es necesario para optimizar costes sin degradar la experiencia.
- Similitud semántica ≠ corrección
Una respuesta puede «sonar bien» y estar equivocada. Por eso grounding y veracidad son ejes separados en nuestra evaluación.

En resumen: la evaluación en RAG debe profundizar más que preguntarse «¿fue una buena respuesta?». Debe explorar por qué lo fue (o no) y qué parte del sistema es responsable.

## Creación de un conjunto de datos de evaluación de alta calidad
La calidad de tu evaluación solo es tan buena como tu dataset.
En nuestro caso, creamos manualmente un conjunto de consultas y respuestas esperadas con la ayuda de expertos de dominio internos. Estos expertos conocen a fondo la documentación de la empresa, la lógica de negocio y la terminología, lo que los convierte en socios ideales para definir qué es «correcto».

Por qué lo manual importa
- Los expertos pueden definir no solo respuestas, sino también qué debe incluir una buena respuesta.
- La redacción real garantiza que las consultas reflejen lo que los usuarios preguntan en verdad.
- Podemos etiquetar no solo la verdad terreno, sino matices (p. ej. «aceptable pero incompleta»).

También analizamos —aunque aún no usamos— herramientas que generan datasets sintéticos directamente desde tu índice vectorial. Pueden ser un buen punto de partida si los recursos manuales son limitados. Algunas opciones:
- LlamaIndex eval
- Ragas (de ExplodingGradients)
- AutoRAG

Sin embargo, nada supera el juicio experto cuando tu caso de uso requiere precisión o tiene implicaciones de cumplimiento normativo.

## Microsoft.Extensions.AI.Evaluation: Panorama general
Microsoft ha presentado un marco de evaluación flexible dentro del ecosistema Microsoft.Extensions.AI, creado específicamente para desarrolladores .NET.

Microsoft.Extensions.AI.Evaluation ofrece herramientas para definir escenarios de evaluación, aplicar evaluadores integrados y personalizados, y generar informes estructurados que puedes analizar o visualizar después.

## Arquitectura de alto nivel

![](../images/evaluacion-sistemas-ai-rag/picture3.png)

## Ejemplo práctico
Primero, partiremos de un fichero JSON que será nuestro dataset origen para la evaluación. El fichero JSON es de este estilo:

![](../images/evaluacion-sistemas-ai-rag/picture4.png)

Lo siguiente es inicializar el ReportingConfiguration, donde pasaremos aquellos Evaluators que queremos utilizar, en esta caso solo queremos evaluar Equivalence, Groundedness y Relevance. 

![](../images/evaluacion-sistemas-ai-rag/picture5.png)
Además de los Evaluadores, también le proporcionamos la configuracion del Modelo que usaremos para realizar la Evaluación:

![](../images/evaluacion-sistemas-ai-rag/picture6.png)

Ahora, para evaluar todas las preguntas de nuestro dataset, y hacerlo como test individual, haremos uso de una Theory de xUnit:

![](../images/evaluacion-sistemas-ai-rag/picture7.png)
El metodo GetQuestionsToEvaluate, simplemente lee el fichero JSON, lo mapea a una lista de un modelo Question, y lo retorna.

Dentro del metodo EvaluateQuestion, primero de todo hacemos una llamada a nuestro sistema de AI. Normalmente nuestra solución tendrá algún tipo de API a la que lanzar la pregunta / chat. En este ejemplo, estamos usando directamente KernelMemory para lanzar la pregunta.

![](../images/evaluacion-sistemas-ai-rag/picture8.png)

En este punto, como estamos usando el Evaluador de Groundedness, necesitamos obtener el Contexto (Facts) que se pasó al modelo junto con la pregunta. Esto nos lo da fácil KernelMemory con el siguiente código:

![](../images/evaluacion-sistemas-ai-rag/picture9.png)
Lo siguiente, es preparar el contexto extra que necesitan los Evaluadores de Groundedness y Equivalence:

![](../images/evaluacion-sistemas-ai-rag/picture10.png)

Finalmente lanzamos la evaluación:

![](../images/evaluacion-sistemas-ai-rag/picture11.png)
Lo último que nos queda ya, es realizar las assertions:

![](../images/evaluacion-sistemas-ai-rag/picture12.png)

Así, al ejecutar los tests, tendriamos los resultados:

![](../images/evaluacion-sistemas-ai-rag/picture13.png)
El test que ha fallado, era en realidad esperado, ya que modifique la respuesta esperada de una de las preguntas para comprobar que efectivamente fallaba. Aún así, es importante tener en cuenta que en ocasiones, podemos obtener tanto falsos positivos como falsos negativos, ya que es un Modelo de AI el que realiza la evaluación, y puede equivocarse.

Podéis encontrar el ejemplo concreto en mi repositorio de GitHub:
https://github.com/luismanez/global-azure-bootcamp-mad-2025

## Lecciones aprendidas del uso en el mundo real
- La evaluación aporta claridad
Ahora tenemos una forma coherente de hablar de la calidad del sistema más allá del «parece que va bien».
- La verdad terreno lo es todo
Un dataset bien construido hace o deshace el proceso de evaluación. Invierte en esto pronto.
- Los criterios integrados ayudan, pero los evaluadores personalizados son oro
Adaptar evaluadores a tu dominio (cumplimiento, tono) desbloquea insights más profundos.
- No subestimes fluidez y coherencia
Las respuestas correctas pueden fracasar si confunden o frustran a los usuarios.
- Automatiza cuanto antes
Incluso la automatización parcial de la evaluación ayuda a escalar la iteración y las pruebas A/B.

## La IA RAG fiable necesita evaluación
En la carrera por crear apps impulsadas por IA, es tentador saltar del prototipo a producción. Pero sin una evaluación rigurosa, vuelas a ciegas. Para sistemas que usan LLM —y especialmente RAG— la calidad es sutil y multidimensional.
Aplicando una evaluación estructurada con herramientas como Microsoft.Extensions.AI.Evaluation y basando tu proceso en datasets etiquetados por expertos, puedes construir sistemas de IA que sean no solo potentes, sino también fiables.

La evaluación no es una casilla final que marcar: es un proceso continuo que posibilita mejor arquitectura, mejores decisiones y, en última instancia, mejores experiencias de usuario.

Y hasta aquí el artículo. Espero que os sea de utilidad.

¡Hasta el próximo artículo!

Luis Mañez – Chief Architect en ClearPeople LTD
@luismanez
https://github.com/luismanez
