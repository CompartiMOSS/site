---
title: "Introducción a Azure Data Factory"
date: 2025-09-18
excerpt: "Cómo evaluar sistemas de IA, en particular arquitecturas basadas en RAG, usando el ecosistema .NET y la biblioteca Microsoft.Extensions.AI.Evaluation."
author: "Alberto Escola Fiz"
authorSlug: "alberto-escola-fiz"
image: "../images/into-azure-data-factory/picture1.png"
category: "AI"
---

Dentro del mundo de los datos muchas veces nos encontramos situaciones donde nuestra aplicación ha de trabajar con una o varias fuentes de datos heterogéneas en cuanto a su formato, origen, esquema, periodos de refresco, carga… 
Es en esas situaciones donde surgen los procesos de ETL (Extract, Transform, Load) como un mecanismo de integración de esos datos que nos permite cargar, combinar y homogeneizar esos datos y almacenarlos típicamente en un dataware house o data lake.
Las tareas habituales de un proceso ETL son:
- Extraer
  - Conexiones a uno o varios orígenes heterogéneos de datos
    - Repositorios de ficheros (SMB, SharePoint, FTP…)
    - Bases de datos SQL y no SQL
    - Servicios Web
    - …..
  - Manejar distintos formatos
    - Texto plano (CSV, XML, JSON…)
    - Excel

  - Verificación de los datos para descartar valores no esperados o no permitidos.
- Transformar
  - Aplicación reglas de negocio sobre el conjunto de datos de entrada que manipulan esos datos
    - Filtrado de filas y/o columnas
    - Cambio de tipo de dato (string a int p.ej)
    - Cambios de formato de datos (mm/dd/yyyy a yyyy/mm/dd p.ej)
    - Obtener columnas con valores calculados
    - Pivotar/despivotar
    - Separar una columna en varias
    - Totalización 
    - Anexar
    - Combinación 
    - …..
  - Cargar
    - Operaciones CRUD en uno o más destinos 

Estos sistemas típicamente deben afrontar los siguientes desafíos:
- Diversidad de las fuentes de datos
- Validez de los datos
- Volumen de los datos
- Escalabilidad
- Carga en los sistemas (CPU, RAM…) 
- Paralelismo y concurrencia
- Periodos de sincronización
- Privacidad y cumplimiento

Tradicionalmente, ha sido SQL Server Integration Services (SSIS) el componente utilizado para realizar estas tareas en entornos On Premise, pero en entorno cloud Microsoft pone a nuestra disposición Azure Data Factory (en adelante  ADF) llamada a ser la evolución de SSIS.
ADF viene en dos versiones: ADF v2 que será que veamos en este articulo y la versión en Fabric.

Dentro de ADF v2 tenemos varias opciones:
- Canalizaciones: Permiten realizar tareas de ETL pero sin transformaciones complicadas. Esta será la opción que desarrollaré mas adelante
- Flujos de datos: Permiten realizar operaciones de transformación de datos más complicadas (p.ej pivotaje)
- SSIS Shift and Lift: Permite migrar procesos de SSIS a la nube sin tener que modificarlos.

## Creación de una factoría
Una factoría es un entorno donde tendremos una o varias canalizaciones que ejecutarán procesos ETL.
Para crear una factoría tendremos que tener una suscripción de Azure y desde el portal de Azure ir a factoría de datos v2, donde tendremos disponible la opción de crear una factoría

![](../images/into-azure-data-factory/picture1.png)

Una vez creada tendremos disponibles algunas opciones generales de configuración, opciones de supervisión y automatización asi como el acceso a la herramienta de programación.

![](../images/into-azure-data-factory/picture2.png)

## Azure Data Studio
Es la herramienta Web que nos permite desarrollar nuestras canalizaciones en una factoría. Podemos acceder a ella una vez creada la factoría de datos.

![](../images/into-azure-data-factory/picture4.png)

Los principales recursos dentro de una fábrica de datos son los siguientes:
•	Canalizaciones: Flujo de trabajo que organiza actividades de datos en ADF. Se usa para extraer, transformar y cargar datos desde diversas fuentes a diferentes destinos.
•	Captura de datos modificados: Permite identificar y procesar sólo los datos nuevos o modificados, en lugar de volver a copiar toda la fuente de datos. 
•	Conjuntos de datos: Son representaciones de las fuentes o destinos de datos en ADF. 
•	Flujos de datos: Son procesos visuales de transformación de datos sin necesidad de escribir código. Permiten realizar operaciones como filtrado, unión, agregación y limpieza antes de cargar los datos al destino.

![](../images/into-azure-data-factory/picture3.png)


Vamos a desarrollar un poco más en detalle cada uno de estos recursos.

## Canalizaciones
Una canalización es un conjunto de actividades que realizan un proceso ETL orquestando el movimiento y la transformación de los datos. Estas actividades se ejecutarán según un flujo establecido entre ellas por conectores.
Una actividad tiene un punto de entrada y varios puntos de salida:  al omitir, ejecución con éxito, ejecución con error y al finalizar. 
Podremos tener uno o varios conectores en cada punto de salida y a un punto de entrada de una actividad podrán llegar uno o varios conectores. 
En la siguiente figura podemos ver 5 actividades unidas por conectores

![](../images/into-azure-data-factory/picture5.png)

Las actividades disponibles dentro de una canalización pueden agruparse en los siguientes grupos:
- Mover y transformar
- Synapse
- AzureData Explorer
- Función de Azure
- Data lake analytics
- Servicios de batch
- General
- HDInsight
- Iteración y condicionales
- Machine Learning
Y son las mostradas en la imagen siguiente

![](../images/into-azure-data-factory/picture6.png)

Cada actividad tiene propiedades que definirán su comportamiento. Una de las enormes ventajas de ADF es que estas propiedades son parametrizables, bien con resultados obtenidos en actividades previas o bien utilizando parámetros o variables de la canalización.

## Conjuntos de datos
Un conjunto de datos describe que datos van a utilizarse y a su vez utiliza un servicio vinculado que describe como conectarse a esos datos.
Por ejemplo, Si queremos conectarnos a una tabla de una base de datos SQL Server el conjunto de datos describe la tabla a la que vamos a conectarnos y el servicio vinculado describe como conectarse (servidor, instancia, credenciales…)

ADF ofrece una gran multitud de servicios vinculados para poder conectarnos, 

![](../images/into-azure-data-factory/picture7.png)

Una posibilidad muy interesante es conectarse a fuentes de datos onPremise utilizando el entorno de ejecución autohospedado (self-hosted IR). 
Consiste en un servicio Windows que se instala en el entorno OnPremise y que permite conectarse desde la nube sin tener que realizar apertura de puertos en nuestra red.
Una vez instalado y configurado, podremos conectarnos desde la factoría de datos para acceder a los datos locales necesarios.

## Flujos de datos
Un flujo de datos define una serie de transformaciones de datos que se realizarán dentro de una canalización. 

![](../images/into-azure-data-factory/picture8.png)

Estas transformaciones ya implican operaciones sobre filas y columnas de los datos como se puede apreciar en la imagen anterior.
Los flujos de datos tendrán uno o varios orígenes y uno o varios destinos y entremedias realizaremos las operaciones de transformación 


![](../images/into-azure-data-factory/picture9.png)

En la imagen anterior un ejemplo sencillo de flujo de datos en con 2 orígenes, un divisor condicional múltiple que nos permite tener varias ramas de ejecución de distintas operaciones como un join, llamar a otro flujo de datos o volcar datos en la salida de datos.
Tanto las entradas como las salidas de datos utilizan orígenes de datos que pueden ser los mismos que los definidos para actividades de canalizaciones.
La ejecución de un flujo de datos se realiza mediante la actividad flujo de datos en una canalización donde configuraremos la llamada al flujo de datos

![](../images/into-azure-data-factory/picture10.png)

Es importante señalar la configuración del tamaño del proceso (por defecto small) ya que impacta tanto en el rendimiento como en el coste de ejecución del flujo de datos.

## Creando una canalización sencilla

Como ejemplo, vamos a crear una canalización que se conecta a una tabla llamada TablasACopiar con dos campos NombreTabla y CopiarTabla, lee los registros de dicha tabla y copia desde el mismo origen las tablas que figuren en ella y tengan el campo CopiarTabla a true.
Lo primero será definir los servicios vinculados para el origen y destino. Para ello vamos a la sección conexionesservicios vinculados y creamos las conexiones. En el ejemplo será una conexión única a una base de datos SQL Azure.
Para definir un servicio vinculado de este tipo hay que introducir en el asistente los datos de conexión : nombre de la BBDD, tipo de autenticación, credenciales y algunos elementos como el nivel de TLS.

![](../images/into-azure-data-factory/picture11.png)

Con este servicio vinculado definido podremos crear y configurar las actividades de la canalización.

![](../images/into-azure-data-factory/picture12.png)

La primera actividad es del tipo script. Esta actividad nos permite ejecutar sentencias TSQL

![](../images/into-azure-data-factory/picture13.png)

En la figura vemos que la configuración de esta actividad es escoger el servicio vinculado que se usará en la actividad y el script a ejecutar. En nuestro caso será una query con una select sencilla que nos recupere el contenido de la tabla.
La segunda actividad es del tipo filtro, lo que nos permitirá quedarnos solamente con los registros que nos interesan (si, otra opción es incluir el filtro en el script de la primera actividad)

![](../images/into-azure-data-factory/picture14.png)
En este caso la configuración es por una parte la lista de elementos, que serán los recuperados de la actividad anterior usando las expresiones disponibles. En nuestro caso la expresión es:

@activity('Recuperar Lista TablasOrigen').output.ResultSets[0].rows
Esta expresión permite recuperar la salida de una actividad.
Tendremos que configurar también la condición de filtrado, la expresión es:
 @equals(item().CopiarTabla,true )
Esta expresión hará que la salida de la actividad solamente contenga los registros cuyo campo CopiarTabla sea true.
A continuación, tendremos que iterar sobre el conjunto de datos filtrado mediante una actividad foreach, su único parámetro de configuración serán los elementos con lo que la actividad realizará la iteración

![](../images/into-azure-data-factory/picture15.png)
En nuestro caso los elementos serán el resultado de salida del filtro
@activity('Filtrar').output.Value

La última actividad de nuestra canalización será la de copiar cada tabla indicada en los registros.

![](../images/into-azure-data-factory/picture16.png)

Para ello tendremos que configurar una actividad de copia a la que configuraremos con los conjuntos de datos de origen y destino, el nombre de las tablas (que vendrá como parámetro de la actividad foreach) y opciones muy interesantes como la opción de crear la tabla automáticamente o el comportamiento de escritura (inserción, actualizar/insertar o procedimiento almacenado), opciones de partición en el origen, ejecución de scripts previo a la operación de volcado de datos…
También señalar aquí la opción Unidad de integración de datos máxima (DIU) que por defecto viene en auto. Esta opción nos permite ajustar el rendimiento y coste de la operación de copia.

## SSIS Shift and Lift
La última opción es la de ejecutar paquetes SSIS en ADF sin reescribir el proceso. Algunas características de esta opción son:
- Integración con SSIS (SQL Server Integration Services)
  - Soporta la ejecución de paquetes SSIS en Azure-SSIS Integration Runtime sin modificaciones.
- Conectividad híbrida
  - Acceso a datos locales mediante Self-hosted Integration Runtime
- Orquestación y automatización
  - Coordina flujos de trabajo de datos mediante canalizaciones.
- Escalabilidad y rendimiento
  - Permite escalar dinámicamente los recursos.
- Compatibilidad con múltiples fuentes y destinos
  - Soporta una amplia variedad de almacenes de datos
- Monitorización y seguridad
  - Ofrece herramientas de monitoreo en tiempo real, alertas, compatibilidad con Azure Key Vault para la gestión segura de credenciales.
Esta opción básicamente consiste en configurar dentro de una factoría de datos un entorno de integración SSIS que define un cluster de integración SSIS. 

## ADF v2 vs Fabric
Como punto final, aquí tienes algunas diferencias entre ADF en la versión 2 y ADF en Fabric

| Funcionalidad              | Fabric                          | ADFv2                   |
|----------------------------|---------------------------------|-------------------------|
| OneLake como almacenamiento unificado | Sí                              | No                      |
| Shortcuts para acceso sin duplicación de datos    | Sí                              | No                      |
| Sin necesidad de Integration Runtime (IR) | Sí                              | No (IR requerido)                     |
| Modelo de ejecución basado en capacidad     | Sí                              | No (uso por consumo)                      |
| Integración nativa con Power BI    | Sí                              | No                      |
| Acceso a Data Science y AI         | Sí                              | No                      |
| Integración con Microsoft Purview sin configuración adicional | Sí                              | No (requiere configuración)                     |
| Orquestación mejorada sin necesidad de múltiples herramientas | Sí                              | No                      |
| Gestión de seguridad centralizada con Microsoft Entra ID  | Sí                              | No (requiere más configuraciones manuales)                      |
| Acceso a datos locales (SQL Server) | On premise data gateway    | IR autohospedado |

¡Espero que esta pequeña introducción pueda servirte para zambullirte en esta poderosa herramienta!

