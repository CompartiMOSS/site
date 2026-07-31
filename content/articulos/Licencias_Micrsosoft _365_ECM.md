---
title: "Licencias para ECM en Microsoft 365: cómo elegir sin gastar de más"
date: 2026-07-31
excerpt: "El modelo de licencias de Microsoft 365 es uno de los primeros temas que hay que resolver antes de diseñar cualquier arquitectura ECM. En este artículo recorro el mapa completo: planes Enterprise (E3, E5, E7), planes Business, licencias Frontline y los servicios de pago por uso como SharePoint Embedded, Microsoft 365 Archive y Purview. Aunque uso el sector financiero como referencia —por ser uno de los más exigentes en cumplimiento y volumen—, la guía aplica a cualquier organización que necesite ordenar su gestión documental, sea cual sea su rubro."
author: "Fabian Iman"
authorSlug: "fabian-imaz"
image: "../images/diagram_decision_licencias.png"
category: "ECM"
---

Una de las conversaciones que más se repite al arrancar un proyecto de ECM sobre Microsoft 365 es la de las licencias. Y casi siempre aparece tarde: cuando ya se armó el diseño y alguien pregunta "¿pero eso está incluido en lo que tenemos?". Lo que parece un detalle administrativo termina siendo una decisión de arquitectura. La licencia que el cliente tiene define lo que podés construir y cómo.

En mi experiencia, esto pasa en todo tipo de organizaciones: bancos, aseguradoras, clínicas, organismos públicos, empresas de servicios. El escenario cambia, pero la confusión con las licencias de Microsoft 365 es siempre la misma. En este artículo les ordeno el panorama completo para que entren a la reunión de diseño con los números claros.

## ¿Por qué la licencia define la arquitectura?

En un proyecto ECM sobre Microsoft 365 la licencia no es solo un tema de costos: es un habilitador de funcionalidades. Si el cliente no tiene Microsoft Purview Records Management, no puede implementar retención granular por tipo de contenido. Si no tiene SharePoint Embedded, no puede usar contenedores como primera capa de archivado. Definir primero el stack de licencias evita diseñar una arquitectura que después no se puede implementar.

Microsoft organiza sus licencias ECM en tres categorías: los planes base que habilitan la plataforma, los complementos que agregan capacidades específicas, y los servicios de pago por uso que escalan sin necesitar licencias adicionales por usuario.

## Los planes Enterprise: E3, E5 y el nuevo E7

Los tres planes enterprise relevantes para ECM en 2026 son M365 E3 ($39/usuario/mes), M365 E5 ($60/usuario/mes) y el reciente M365 E7 ($99/usuario/mes, disponible desde mayo de 2026). Estos planes no tienen límite de usuarios y son el punto de partida para organizaciones grandes o con requisitos de cumplimiento avanzados.

El plan **E3** incluye SharePoint Online completo: sitios, bibliotecas, tipos de contenido, Term Store, metadatos administrados y retención básica. Para un gestor documental sin requisitos avanzados de cumplimiento, E3 es el plan base.

El plan **E5** agrega el stack completo de Purview Compliance: Records Management, eDiscovery Premium, Insider Risk Management, Communication Compliance y Purview Information Protection P2. Para organizaciones con cumplimiento regulatorio exigente —sector financiero, salud, gobierno—, E5 es el punto de partida real.

El plan **E7** (mayo 2026) incluye todo E5 más Microsoft 365 Copilot en el paquete base. Para quienes ya pagaban E5 + Copilot add-on, E7 puede representar un costo similar con una factura más simple.

La Imagen 1 resume qué capacidades ECM incluye cada plan Enterprise y cuáles requieren complemento adicional.

![Capacidades ECM por plan de licencia Microsoft 365](../images/diagram_licencias_ecm.png)

*Imagen 1.- Capacidades ECM por plan de licencia Microsoft 365: verde = incluido, naranja = add-on, violeta = PAYG vía Azure.*

## ¿Necesita E3 o E5 todo el mundo? Licencias mixtas para colaboradores

No todos los usuarios de un gestor documental hacen lo mismo. El compliance officer que configura las políticas de Purview necesita E5; el operador documental que carga expedientes puede trabajar con E3 o Business Standard; el gerente de sucursal que solo consulta documentos puede usar Business Basic. En el mismo tenant pueden convivir distintos planes sin ningún problema.

Microsoft organiza las opciones de menor costo en dos familias adicionales:

**Planes Business** (hasta 300 usuarios por organización): incluyen SharePoint Online, Teams y Exchange con distintos niveles de apps Office.

- **Business Basic ($7/usuario/mes)**: SharePoint Online vía web y mobile, Teams y Exchange. Sin apps de escritorio. Suficiente para usuarios que solo colaboran en documentos desde el navegador.
- **Business Standard ($14/usuario/mes)**: todo lo anterior más las apps de Office en escritorio.
- **Business Premium ($22/usuario/mes)**: agrega Intune, Defender for Business y Purview Information Protection P1. Apto para organizaciones medianas con necesidades básicas de cumplimiento.

**Licencias Frontline Worker** (F1/F3): pensadas para trabajadores de campo o usuarios de consulta ocasional en tenants Enterprise y Business.

- **F1**: acceso de solo lectura a SharePoint Online vía web y mobile. Ideal para usuarios que solo necesitan consultar documentos.
- **F3 ($10/usuario/mes desde julio 2026)**: acceso completo de edición a SharePoint y Teams. Para usuarios de campo que también necesitan cargar documentos.

Una aclaración clave para proyectos ECM: las políticas de retención de Purview y las etiquetas de sensibilidad actúan sobre el **contenido**, no sobre la licencia del usuario que lo accede. Un usuario Business Basic que sube un documento a una biblioteca protegida por una política de Purview queda igualmente bajo esa política. Lo que sí requiere licencia E5 o Purview Add-on es la **administración** de esas políticas: quienes las configuran, aplican etiquetas regulatorias o participan en revisiones de disposición necesitan la licencia adecuada.

Vale mencionar también que desde mayo de 2026, Microsoft retiró los planes SharePoint Online Plan 1 y Plan 2 como productos independientes. El acceso a SharePoint hoy se licencia únicamente a través de los planes Microsoft 365 (Business, Enterprise o Frontline).

La tabla siguiente resume el criterio para elegir el nivel de licencia según el perfil de usuario en un proyecto ECM:

| Perfil de usuario | Rol en el gestor ECM | Licencia recomendada |
|---|---|---|
| Administrador de compliance / Records Manager | Configura políticas Purview, Records Management, disposición | M365 E5 o E3 + Purview Add-on |
| Arquitecto / Admin de SharePoint | Diseña y administra la arquitectura de sitios y tipos de contenido | M365 E3 o E5 |
| Operador documental | Carga, clasifica y gestiona expedientes diariamente | M365 E3 o Business Standard |
| Colaborador ocasional | Edita y consulta documentos, participa en flujos de aprobación | M365 E3, Business Basic o Business Standard |
| Usuario de consulta | Solo consulta documentos desde el navegador o mobile | M365 Business Basic o F1 |
| Usuario de campo con edición | Carga documentos desde terreno vía app móvil | M365 F3 |

## SharePoint Premium: cuando la IA clasifica sola

SharePoint Premium —el producto que antes se llamaba Syntex— es un complemento de aproximadamente $5/usuario/mes que agrega clasificación automática de documentos e inteligencia artificial aplicada al contenido. Con SharePoint Premium se pueden entrenar modelos para que clasifiquen documentos automáticamente y extraigan metadatos sin intervención del usuario: el sistema reconoce un contrato, le asigna su tipo de contenido y completa los campos de metadatos directamente en el momento de la carga.

Para la arquitectura ECM que vamos construyendo en esta serie esto es especialmente relevante en el punto de ingreso: el operador sube el documento, SharePoint Premium lo clasifica y le asigna el tipo de contenido correcto sin que el operador tenga que seleccionarlo a mano. No es un complemento obligatorio para arrancar, pero marca una diferencia importante en la experiencia de los operadores documentales.

## SharePoint Embedded: sin licencias de usuario, pago por uso

SharePoint Embedded es el servicio de contenedores de Microsoft, facturado 100% por consumo a través de una suscripción de Azure, sin licencias por usuario. Tiene cuatro medidores de facturación:

- **Almacenamiento activo**: por GB almacenado en contenedores activos
- **Almacenamiento archivado**: tarifa más baja para contenedores en estado archivado
- **Transacciones de API**: por llamada a Microsoft Graph desde la aplicación
- **Egress**: por GB de datos que salen de la plataforma (con exenciones para clientes Office Desktop y para el WAC)

El modelo de precios exacto por GB está publicado en la página oficial del producto: [https://adoption.microsoft.com/en-us/sharepoint/embedded/](https://adoption.microsoft.com/en-us/sharepoint/embedded/). Lo importante desde la arquitectura es que SharePoint Embedded no requiere que los usuarios finales tengan licencias adicionales: el costo lo paga la organización por lo que consume, lo que lo hace ideal para archivado de largo plazo donde los accesos son esporádicos.

## Microsoft 365 Archive: almacenamiento frío al mejor costo

Microsoft 365 Archive cobra $0,05/GB/mes por el almacenamiento de sitios y archivos archivados —pero solo cuando ese almacenamiento supera la cuota incluida en las licencias del tenant. Si el tenant tiene cuota disponible sin usar, archivar no genera costo adicional.

Un dato que muchos proyectos no tienen en cuenta: desde el 31 de marzo de 2025, la reactivación de contenido archivado es gratuita. Ya no se cobra por reactivar un sitio o expediente. Lo que sí aplica es un período de 120 días donde el contenido recién reactivado no puede volver a archivarse. Para el diseño del ciclo de vida documental, este detalle importa.

## Microsoft Purview: el motor de retención y registros

Para implementar retención por tipo de contenido y Records Management completo, la funcionalidad mínima necesaria es Microsoft Purview Data Lifecycle Management y Records Management. Ambas están incluidas en M365 E5. Para usuarios con E3, se puede agregar el complemento Microsoft Purview Suite que incorpora el stack completo de cumplimiento avanzado sin necesidad de migrar al plan E5 completo, aunque en la mayoría de los proyectos ECM de cierta escala termina siendo más conveniente ir directamente a E5.

## Microsoft 365 Copilot: la licencia del Knowledge Agent

El SharePoint Knowledge Agent —la capa de búsqueda en lenguaje natural que mencionamos en el artículo de Arquitectura ECM— requiere Microsoft 365 Copilot. En el mercado enterprise el complemento cuesta $30/usuario/mes sobre E3 o E5. Como alternativa, el nuevo plan M365 E7 lo incluye dentro del paquete.

No todos los usuarios del gestor documental necesitan Copilot. En general se licencia solo para los perfiles que van a hacer consultas en lenguaje natural o usar capacidades de IA sobre el contenido. Los operadores documentales que solo cargan y consultan expedientes pueden trabajar perfectamente con E3 sin Copilot.

## ¿Qué necesita el escenario de Arquitectura ECM?

Para el gestor documental que vamos armando en esta serie —usando el sector financiero como referencia por su complejidad regulatoria, aunque el mismo stack aplica a cualquier organización con necesidades similares—, la combinación mínima recomendada sería la siguiente:

- **M365 E5** para administradores, compliance officers y usuarios con roles de Records Management.
- **M365 E3 o Business Standard** para operadores documentales que cargan y gestionan expedientes.
- **Business Basic o F1** para usuarios de consulta que solo necesitan visualizar documentos.
- **SharePoint Embedded** vía Azure (PAYG) para los contenedores de archivado por entidad o cliente.
- **Microsoft 365 Archive** (PAYG, $0,05/GB/mes) cuando el tenant supera su cuota de almacenamiento.
- **SharePoint Premium** (opcional, ~$5/usuario/mes) para operadores que van a aprovechar la clasificación automática en el ingreso.
- **Microsoft 365 Copilot** (opcional, +$30/usuario/mes) para perfiles que van a consultar el gestor con lenguaje natural.

La Imagen 2 muestra el árbol de decisión para elegir el stack según las necesidades de cada proyecto.

![Árbol de decisión: ¿qué licencias necesito?](../images/diagram_decision_licencias.png)

*Imagen 2.- Árbol de decisión para elegir el stack de licencias ECM en Microsoft 365.*

## Conclusión

En este artículo les presenté el mapa completo de licencias que intervienen en un proyecto ECM sobre Microsoft 365. La clave está en pensar en capas: E5 para quienes administran el cumplimiento, E3 o Business para operadores documentales, y F1 o Business Basic para usuarios de consulta. Sobre ese mix, SharePoint Embedded y Microsoft 365 Archive habilitan el archivado en dos capas sin licencias adicionales por usuario; y Copilot abre la puerta al Knowledge Agent para búsqueda en lenguaje natural. En el siguiente artículo arrancamos con la estructura documental: la jerarquía de sitios, los tipos de contenido y el rol de los hub sites en la plataforma ECM.

**Fabián Imaz**
Office Apps and Services MVP
CEO Siderys | CTO qualitaslearning.com
fabiani@siderys.com.uy | @fabianimaz
