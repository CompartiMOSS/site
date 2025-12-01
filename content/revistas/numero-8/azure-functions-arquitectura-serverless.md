---
title: "Azure Functions: Arquitectura Serverless"
slug: "azure-functions-arquitectura-serverless"
magazineSlug: "numero-8"
author: "Adrián Díaz Cervera"
authorSlug: "adrian-diaz-cervera"
excerpt: "Implementa soluciones escalables con Azure Functions."
---

Azure Functions permite crear aplicaciones sin gestionar infraestructura, enfocándote únicamente en el código de negocio.

## Introducción a Serverless

### ¿Qué es Serverless?

Serverless no significa "sin servidores", sino que:
- No gestionas la infraestructura
- Pagas solo por lo que usas
- Escalas automáticamente
- Te enfocas en el código

### Beneficios

- **Reducción de costos**: Sin servidores ociosos
- **Escalabilidad automática**: Responde a la demanda
- **Desarrollo ágil**: Deploy más rápido
- **Menos operaciones**: Microsoft gestiona la infraestructura

## Triggers y Bindings

### Triggers Comunes

Azure Functions puede activarse por:
- **HTTP**: APIs y webhooks
- **Timer**: Tareas programadas
- **Queue**: Procesamiento de mensajes
- **Blob**: Eventos de almacenamiento
- **Event Grid**: Eventos de Azure

### Bindings

Los bindings simplifican la integración:
```csharp
[FunctionName("ProcessOrder")]
public static async Task Run(
    [QueueTrigger("orders")] Order order,
    [CosmosDB("db", "orders")] IAsyncCollector<Order> output)
{
    await output.AddAsync(order);
}
```

## Patrones de Arquitectura

### Fan-out/Fan-in

Para procesamiento paralelo:
1. Divide el trabajo en tareas
2. Ejecuta en paralelo
3. Consolida resultados

### Function Chaining

Para workflows secuenciales:
1. Function A procesa y llama a B
2. Function B procesa y llama a C
3. Function C completa el flujo

### Async HTTP APIs

Para operaciones largas:
1. Recibe request, retorna 202 Accepted
2. Procesa en background
3. Cliente consulta estado

## Durable Functions

### Orquestaciones

Durable Functions permite:
- Workflows de larga duración
- Estado persistente automático
- Retry automático

### Ejemplo de Orquestación

```csharp
[FunctionName("OrderWorkflow")]
public static async Task<string> RunOrchestrator(
    [OrchestrationTrigger] IDurableOrchestrationContext context)
{
    var order = context.GetInput<Order>();
    
    await context.CallActivityAsync("ValidateOrder", order);
    await context.CallActivityAsync("ProcessPayment", order);
    await context.CallActivityAsync("ShipOrder", order);
    
    return "Completed";
}
```

## Mejores Prácticas

### Diseño

- Mantén las funciones pequeñas y enfocadas
- Usa dependency injection
- Implementa idempotencia

### Rendimiento

- Minimiza cold starts con plan Premium
- Reutiliza conexiones (HttpClient estático)
- Usa async/await correctamente

### Seguridad

- Usa Managed Identity
- Almacena secrets en Key Vault
- Implementa autenticación apropiada

## Monitoreo

### Application Insights

Integra Application Insights para:
- Traces y logs
- Métricas de rendimiento
- Alertas automáticas
- Dashboards personalizados

## Conclusión

Azure Functions es una herramienta poderosa para construir soluciones modernas y escalables. Con el diseño correcto, puedes crear arquitecturas que escalan automáticamente y minimizan costos operativos.
