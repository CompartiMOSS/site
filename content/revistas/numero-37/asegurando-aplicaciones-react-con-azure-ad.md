---
title: "Asegurando Aplicaciones React con Azure AD"
slug: "asegurando-aplicaciones-react-con-azure-ad"
magazineSlug: "numero-37"
author: "Luis Valencia"
authorSlug: "luis-valencia"
keywords: ['SharePoint Framework','Azure AD']
image: "../images/asegurando-aplicaciones-react-con-azure-ad/image8.png"
---

La mayoría de los desarrolladores, actualmente han estudiado las tecnologías ReactJS, Angular y VUE como fundamentales para la creación de nuevas aplicaciones. Esta información es de conocimiento de programadores incluso de los que trabajan en ASP.NET, para crear aplicaciones que hagan más ágil la transmisión de información, ya que la aplicación no se refrescaría constantemente del lado del servidor. Desde mi punto de vista, crear aplicaciones ASP.NET MVC ya no es suficiente para tener una buena experiencia de usuario, es necesario tener un framework del lado del cliente para hacer una experiencia que agrade al usuario final.

A pesar de la diversidad de textos, artículos, blogs y manuales, aún existen lagunas en la información. Al no encontrar alguna publicación con las explicaciones que necesitaba surgió la idea de este artículo. El presente texto es creado con el objetivo de mostrar cómo se configurar una aplicación ReactJS que consume un Web API para que se autentique con usuarios creados en el directorio Activo de Azure (el WebAPI también está protegido por Azure AD).

Lo primero que debemos hacer es crear un registro de aplicación en el directorio activo de Azure, como se muestra en las imágenes siguientes:

![Imagen 1.- Acceso al registro de aplicaciones en Azure AD.](../images/asegurando-aplicaciones-react-con-azure-ad/image1.png)

Luego creamos una aplicación con los siguientes datos:

![Imagen 2.- Creación del registro de aplicación.](../images/asegurando-aplicaciones-react-con-azure-ad/image2.png)

Al terminar de crear la aplicación, debemos tomar nota del App Id:

![Imagen 3.- App ID de la aplicación creada.](../images/asegurando-aplicaciones-react-con-azure-ad/image3.png)

Para este articulo asumimos que el lector tiene conocimientos básicos en ReactJS y que ya tiene una aplicación básica creada.

Ahora en nuestra app, tenemos que instalar el paquete React-adal, las instrucciones se encuentran en este sitio web: [https://github.com/salvoravida/react-adal](https://github.com/salvoravida/react-adal)

Después de haber instalado el paquete React-adal, debemos configurarlo, para esto debemos crear un archivo adal-config.js

```

```

En este archivo, debemos cambiar los valores de:

·       Tenant: es el id del directorio activo.

·       clientId: es el id del registro de la app en el directorio activo.

·       Endpoints:  es un arreglo de objetos clave valor, en este arreglo se listan los API que queremos consumir desde la aplicación React, y que también están protegidos por Azure AD. (es el ID de la App registrada en el directorio activo, no es el ID del App Service).

Después de esto y, para terminar, apiURL es la URL del web api que vamos a consumir (En un momento detallaremos mas la parte de configuración del web api). Volviendo a la aplicación React, debemos crear un archivo index.js, es en este archivo es donde utilizamos el paquete instalado anteriormente en el texto.

```

```

```
registerServiceWorker();​
```

En el código anterior se puede observar la utilización del método runWithAdal, y dentro del este se coloca el componente principal desarrollado en ReactJS y así concluye el proceso.

Al correr nuestra aplicación por primera vez, la app se direccionará a la página de login de Microsoft, una vez autenticados, Microsoft nos enviará de vuelta a nuestra aplicación local de React con el Bearer token, el cual será guardado en el almacenamiento local del navegador según lo configuramos en los pasos anteriores.

Hasta esta sección solo hemos hecho la parte de la autenticación de la aplicación del lado del cliente, es decir el frontend, pero como es sabido las aplicaciones tienen también funcionalidad del lado del servidor, es decir la aplicación ReactJS al procesar algo del lado del servidor a través de un Web API.  Es importante mencionar que este Web API también tiene que estar protegido para que solo puedan utilizarlos usuarios o aplicaciones registradas en el directorio activo de Azure.

Para poder realizar este procedimiento es necesario regresar al portal de Azure para registrar una segunda aplicación, esta vez, será el Reply URL,  el Web API que tiene que existir previo a este procedimiento, si no se tiene se puede referir a la página: ([Como crear un Web API](https://msdn.microsoft.com/es-es/communitydocs/web-dev/webapi/mi-primer-proyecto?f=255&amp;MSPPError=-2147217396))

Es importante que al final de la URL de nuestro Web API publicado, se agregue lo siguiente: .auth/login/aad/callback. Esto es necesario para que la autenticación del directorio activo de Azure también funcione con nuestro web api.
![Imagen 4.- Registro de la nueva aplicación.](../images/asegurando-aplicaciones-react-con-azure-ad/image4.png)

Después de esto se debe editar el manifiesto de nuestra aplicación registrada y es importante cambiar la configuración que se muestra a continuación, a través de KnownClientApplications. KnownClientApplications, es un arreglo de aplicaciones que pueden consumir nuestro Web API. En nuestro caso es el id de la aplicación registrada anteriormente.

![Imagen 6.- Valor del KnowClientApplications.](../images/asegurando-aplicaciones-react-con-azure-ad/image5.png)

No se debe dejar de lado la configuración de nuestro Web API para autenticación con el directorio activo, seleccionamos nuestra web app en el portal. Y nos aseguramos de que el Web API este configurado como se muestra a continuación:

![Imagen 7.- Configuración de la autenticación del Web API.](../images/asegurando-aplicaciones-react-con-azure-ad/image6.png)

Para proseguir, se necesita el ClientID, ya que es el id de la Web API registrada en el directorio activo de Azure, y así el Issuer Url termina con el ID del directorio activo de Azure.

![Imagen 8.- Client ID e Issuer Url.](../images/asegurando-aplicaciones-react-con-azure-ad/image7.png)

Como ya se había mencionado anteriormente, en el archivo adalconfig.js debemos configurar el id del Web API registrado y la Url del api, como se observa a continuación.

![](../images/asegurando-aplicaciones-react-con-azure-ad/image8.png)

Una vez realizamos esto, ya podemos utilizar un controlador del API de manera segura como en el siguiente componente:

```

```

En este último ejemplo se observa cómo se puede consumir un web api que simplemente devuelve dos valores (value1, value2), pero lo interesante de esto, es que este web api está protegido con Azure AD así como la aplicación que lo consume.  El token que se obtiene al autenticarse por primera vez en la aplicación ReactJS, es reutilizado al consumir el Web API, y por lo tanto no es necesario una segunda autenticación.

Este articulo sirve como referencia para la construcción de una aplicación ReactJS la cual consume toda su funcionalidad a través de un web api, para poder realizar cualquier aplicación, espero que sea de utilidad para el lector. En próximos textos se revisará como utilizar este conocimiento para utilizar funcionalidades de SharePoint Online con los paquetes de OfficePnP.

**Luis Valencia**

[www.luisevalencia.com](http://www.luisevalencia.com/)

@levalencia

Office Development MVP