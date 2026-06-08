---
title: "Gestión Documental Empresarial con Microsoft 365: un caso de uso en el sector financiero"
date: 2026-06-08
excerpt: "En este artículo les presento la arquitectura de un gestor documental empresarial sobre Microsoft 365 y SharePoint Online, pensado para organizaciones que administran múltiples productos por cliente. Vamos a recorrer la estructura de expedientes, los tipos de contenido, el modelo de metadatos, el ciclo de vida documental, el archivado inteligente y las capacidades de búsqueda. Este escenario es el hilo conductor de la serie sobre ECM que vamos a ir desarrollando en los próximos números de la revista."
author: "Fabian Iman"
authorSlug: "fabian-imaz"
image: "../images/evaluacion-sistemas-ai-rag/diagram_arquitectura.png"
category: "ECM"
---

En estos últimos años vengo viendo cómo Microsoft 365 se metió en prácticamente todas las organizaciones con las que trabajamos, y el sector financiero no es la excepción. Bancos, aseguradoras, entidades de crédito… todos tienen hoy una oportunidad concreta delante: dejar atrás los repositorios desparramados, las carpetas en red y los sistemas de escaneo aislados, y pasarse a una plataforma unificada de gestión documental en la nube. La pregunta que aparece enseguida es: ¿cómo se diseña esa plataforma para que sea robusta, auditable y escale de verdad, en un escenario donde un mismo cliente puede tener al mismo tiempo una cuenta corriente, una tarjeta de crédito, una caja de ahorro y un préstamo hipotecario?

Después de tantos años metido en proyectos de SharePoint y ECM, me crucé con más de una institución financiera que tenía la documentación repartida entre carpetas de red, escáneres aislados y vaya uno a saber cuántos sistemas más. Y siempre termina pasando lo mismo: nadie encuentra nada cuando lo necesita, y cuando aparece una auditoría regulatoria, es un dolor de cabeza. De ese tipo de problemas reales nace el caso que vamos a usar como hilo conductor de toda esta serie.

A lo largo de esta serie les voy a ir mostrando, capa por capa, cómo armamos un gestor documental empresarial sobre Microsoft 365, SharePoint Online, SharePoint Embedded y Azure. En este primer artículo arranco por el caso de uso que va a ordenar todo lo demás: una institución financiera que necesita gestionar expedientes digitales por cliente y por producto, con ciclo de vida documental controlado, seguridad basada en roles y búsqueda sobre metadatos. Ese escenario nos va a servir de referencia concreta para todos los conceptos técnicos que vayamos viendo en los artículos siguientes.

---

## ¿Cuál es el escenario?

Imaginemos una institución financiera con una base de clientes grande, tanto personas físicas como jurídicas, donde cada cliente puede acceder a un catálogo variado de productos: tarjetas de crédito y débito, cuentas corrientes, cajas de ahorro, préstamos automotores, hipotecarios y personales. La documentación de cada uno de esos productos tiene características propias: plazos de retención regulatoria distintos, tipos de documentos requeridos diferentes y procesos de aprobación específicos. Un préstamo hipotecario pide tasaciones, escrituras e informes de riesgo; una tarjeta de crédito, formularios de solicitud, declaraciones de ingresos y contratos de adhesión. Tratar toda esa documentación de la misma manera sería un error de diseño, y créanme que lo vi más de una vez.

El gestor documental que vamos a diseñar sobre Microsoft 365 tiene que resolver tres cosas: organizar la información para que cada documento esté bien clasificado y sea fácil de encontrar; proteger el acceso con un modelo de permisos granular y auditable; y gobernar el ciclo de vida de cada documento, asegurando que se conserve el tiempo necesario y se archive cuando corresponde. Lo bueno es que la plataforma nos da hoy todas las herramientas para lograrlo sin tener que montar infraestructura propia.

---

## Arquitectura de la solución en Microsoft 365

La arquitectura se apoya en tres capas: SharePoint Online como plataforma de almacenamiento y colaboración activa; SharePoint Embedded como primera instancia de archivado, por cliente; y Microsoft 365 Archive como almacenamiento frío de largo plazo. Separarlo en capas nos permite escalar cada parte por su cuenta y controlar los costos de almacenamiento según el ciclo de vida de cada expediente. En la Imagen 1 les dejo la arquitectura completa.

![Arquitectura del gestor documental](../images/diagram_arquitectura.png)

*Imagen 1.- Arquitectura del gestor documental: colecciones de sitios por cliente en SharePoint Online, con archivado en SharePoint Embedded (Tier 1) y Microsoft 365 Archive (Tier 2).*

En la capa activa, cada cliente de la institución va a tener su propia colección de sitios en SharePoint Online, identificada de forma única con un patrón de URL que incorpora el identificador del cliente: `https://tenant.sharepoint.com/sites/{ID-CLIENTE}`. Con esto conseguimos un aislamiento total entre los espacios documentales de distintos clientes, podemos aplicar permisos específicos a nivel de colección de sitios, y escalamos horizontalmente a medida que la base de clientes crece, sin que el crecimiento de un cliente afecte el rendimiento de los demás.

Dentro de cada colección de sitios la cosa se organiza en dos piezas: el Expediente del Cliente, que concentra la documentación de identidad e información general de la persona, y una biblioteca de documentos por cada tipo de producto que el cliente tenga contratado. Cada biblioteca tiene sus propios tipos de contenido, columnas de metadatos y políticas de retención, así que las reglas de cumplimiento quedan exactamente como tienen que estar para cada producto, sin pisarse entre ellas.

---

## El núcleo del modelo: expedientes de cliente y de producto

El concepto de expediente es el eje que ordena toda la información del gestor. Acá distingo dos niveles bien diferentes, tal como van a ver en la Imagen 2.

![Modelo de expedientes](../images/diagram_expedientes.png)

*Imagen 2.- Modelo de expedientes: el sitio del cliente alberga el Expediente del Cliente y una biblioteca de documentos por cada tipo de producto contratado.*

El Expediente del Cliente concentra toda la documentación que identifica a la persona, sin importar qué productos tenga contratados: documentos de identidad, comprobantes de domicilio, declaraciones de ingresos y formularios de conocimiento del cliente (KYC). En SharePoint Online lo implemento como un Conjunto de Documentos (Document Set) en la biblioteca principal del sitio del cliente. Este expediente no caduca: se mantiene activo mientras el cliente tenga alguna relación con la institución.

El Expediente del Producto, en cambio, existe en una instancia separada por cada tipo de producto contratado, alojado en la biblioteca correspondiente dentro del mismo sitio del cliente. Un mismo cliente puede tener al mismo tiempo un expediente de tarjeta de crédito, uno de cuenta corriente y uno de préstamo hipotecario, cada uno en su propia biblioteca, con su documentación, sus metadatos y sus políticas de retención.

Los expedientes de producto los armo también con Conjuntos de Documentos de SharePoint Online, que permiten agrupar varios documentos bajo una entidad con propiedades propias, página de portada personalizada y metadatos que se propagan solos a todos los documentos que la componen.

---

## Taxonomía y tipos de contenido

La taxonomía la centralizo en el Term Store de SharePoint Online, y los Tipos de Contenido los publico desde un Content Type Hub hacia todos los sitios de clientes. Con esto me aseguro consistencia en toda la plataforma: si agrego un nuevo tipo de documento a un producto, el cambio se propaga solo a todos los sitios. Los tipos de contenido los organizo con herencia: tipos base para el Expediente del Cliente y para cada categoría de producto (tarjetas, cuentas, préstamos), de los que después heredan los tipos específicos de cada documento.

En Microsoft 365 esto se complementa con SharePoint Premium (lo que antes era Syntex), que suma la capacidad de clasificar y extraer metadatos de los documentos de forma automática, con modelos de inteligencia artificial entrenados sobre el propio contenido de la organización.

---

## Ciclo de vida documental y retención con Microsoft Purview

Cada tipo de contenido lleva asociada una etiqueta de retención de Microsoft Purview que define cuánto tiempo tiene que quedarse el documento en el repositorio activo. Esa configuración se aplica sola cuando el documento se clasifica con su tipo de contenido. Cuando vence el plazo, Purview puede eliminarlo, retenerlo para revisión o disparar un flujo de Power Automate que avise al responsable para que decida qué hacer.

Hoy Microsoft recomienda usar Microsoft Purview Data Lifecycle Management y Records Management como mecanismo estándar de retención en SharePoint Online, en reemplazo de las viejas políticas de administración de información de SharePoint, cuyo soporte terminó en abril de 2026.

---

## Archivado en dos capas: SharePoint Embedded y Microsoft 365 Archive

El archivado lo armo en dos instancias. La primera, sobre SharePoint Embedded, hace de repositorio de archivado activo por cliente: cuando un expediente o documento tiene que salir del repositorio operativo, creo un contenedor en SharePoint Embedded asociado al identificador del cliente, y ahí consolido todos los expedientes archivados de ese cliente en un espacio lógicamente separado del sitio activo.

La segunda instancia entra en juego cuando el cliente deja de tener relación con la institución: el contenedor completo de SharePoint Embedded se archiva con Microsoft 365 Archive y pasa a almacenamiento frío, sin consumir cuota activa del tenant. El detalle fino del proceso de archivado y la configuración de los contenedores se los dejo para el artículo dedicado al tema, que va a dar para rato.

---

## Seguridad, permisos y auditoría

El modelo de seguridad lo articulo sobre grupos de Microsoft 365 y políticas de acceso condicional de Microsoft Entra ID. Defino roles funcionales —Administrador, Supervisor, Operador Documental, Consultor y Solo Lectura— que se asignan a nivel de colección de sitios del cliente, de manera que cada operador solo puede acceder a los expedientes de los clientes que le tocan.

La auditoría registra todo lo que pasa con cada expediente: creación, modificación, eliminación y archivado. Purview centraliza esos registros en el Unified Audit Log, con capacidad de alertar ante comportamientos raros y de exportar hacia sistemas SIEM corporativos.

---

## Búsqueda y acceso a la información

El acceso a la documentación lo resuelvo con Microsoft Search, que indexa el contenido de todos los sitios de SharePoint Online de forma continua. Los usuarios pueden hacer búsquedas avanzadas con el lenguaje KQL, filtrando por número de cliente, tipo de producto, fecha de vigencia y estado del documento. Y acá viene algo que me entusiasma: el SharePoint Knowledge Agent —disponible con licencia Microsoft 365 Copilot desde 2026— ya permite hacer consultas en lenguaje natural directamente sobre el contenido del gestor documental.

---

## Conclusión

En este primer artículo quise mostrarles cómo una institución financiera puede armar un gestor documental robusto y escalable sobre Microsoft 365, ordenado alrededor de la idea de una colección de sitios por cliente, con una biblioteca de documentos por tipo de producto y un archivado en dos capas que combina SharePoint Embedded y Microsoft 365 Archive. En los próximos artículos vamos a ir bajando a tierra, uno por uno, cada pilar de esta arquitectura —como venimos haciendo siempre en CompartiMOSS—. Acá les dejo el temario completo de la serie:

1. **Artículo 1: Licencias para ECM en Microsoft 365** — planes M365, SharePoint Premium, SharePoint Embedded y Microsoft Purview Add-on
2. **Artículo 2: Estructura Documental** — jerarquía de sitios, hub sites, bibliotecas y tipos de contenido
3. **Artículo 3: Metadatos** — Term Store, columnas de sitio, herencia y metadatos en la era Copilot
4. **Artículo 4: Gobernabilidad y Seguridad** — permisos, grupos de Microsoft 365, SharePoint Advanced Management y Data Access Governance
5. **Artículo 5: Procesos y flujos de trabajo** — Power Automate, aprobaciones y ciclo de vida documental
6. **Artículo 6: Cumplimiento y retención con Microsoft Purview** — etiquetas de retención, Records Management y DLP
7. **Artículo 7: Catalogación y clasificación** — SharePoint Premium / Syntex, clasificación automática y etiquetas de sensibilidad
8. **Artículo 8: Migración a ECM moderno** — auditoría de contenido, estrategia de migración y gestión del cambio
9. **Artículo 9: Almacenamiento — Sitios SharePoint Online** — colecciones de sitios, cuotas y políticas de ciclo de vida
10. **Artículo 10: Almacenamiento — SharePoint Embedded** — contenedores, API, modelo de costos y archivado
11. **Artículo 11: Búsquedas** — Microsoft Search, KQL, conectores de Graph y SharePoint Knowledge Agent
12. **Artículo 12: Integración con APIs y Graph** — Microsoft Graph API, SPFx, REST API y webhooks
13. **Artículo 13: Azure AI e inteligencia documental** — Azure Document Intelligence, OCR y procesamiento multimodal
14. **Artículo 14: Copilot y ECM** — cómo la arquitectura de información impacta las respuestas de Copilot
15. **Artículo 15: Copilot Studio Agents sobre contenido documental** — agentes autónomos sobre repositorios SharePoint
16. **Artículo 16: Formularios y captura inteligente de documentos** — custom upload forms y captura estructurada en el ingreso

---

**Fabián Imaz**
Office Apps and Services MVP
CEO Siderys | CTO qualitaslearning.com
fabiani@siderys.com.uy | @fabianimaz
