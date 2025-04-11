# MCP Configuration & Logic

Este archivo describe la lógica utilizada para la integración del protocolo MCP (*Modular Command Protocol*) en esta solución, junto con detalles de implementación, estructura de datos y flujos principales.

---

## Estructura General

```
.
├── fastapi/             # API REST con FastAPI para manejar 'assistants'
└── mcp/                 # Lógica del servidor MCP y conexión con la IA
    └── mcp_server.py    # Script principal que ejecuta el flujo MCP
```

---

## Conexiones

- **Supabase**: Almacena los `assistants` con sus instrucciones.
- **FastAPI**: Provee endpoints REST para consultar y actualizar asistentes.
- **OpenAI GPT-4**: Se usa para generar sugerencias de mejora a partir de las instrucciones actuales.
- **MCP Server (`mcp_server.py`)**: Es el punto que coordina el flujo:
  1. Recibe un `assistant_id` por consola.
  2. Consulta las instrucciones asociadas desde la API.
  3. Llama a OpenAI para sugerencias.
  4. Muestra al usuario el cambio propuesto.
  5. Aplica la mejora si el usuario acepta.

---

## Prompt Engineering (IA)

La IA recibe un `prompt` estructurado con ejemplos, una introducción de rol, y el bloque actual de instrucciones. El formato de respuesta esperado es JSON:

```json
{
  "assistant_id": "ID del asistente",
  "comparison": {
    "original": "Texto original",
    "suggested": "Texto mejorado",
    "differences": ["Lista de cambios relevantes"]
  },
  "reasoning": "Justificación clara del cambio"
}
```

### Estructura de prompt enviado:

```plaintext
Estás actuando como un editor experto de instrucciones para asistentes virtuales.

Tu tarea es analizar instrucciones actuales, detectar oportunidades de mejora y devolver una propuesta clara, profesional y útil para los usuarios.

Devuelve tu respuesta en formato JSON con las siguientes claves:
- assistant_id: ID del asistente.
- comparison:
    - original: Instrucciones originales.
    - suggested: Versión mejorada.
    - differences: Lista de diferencias clave entre ambas versiones.
- reasoning: Justificación clara de por qué tu versión es mejor.

Ejemplo 1:
Original: "Responde a lo que te digan."
Sugerido: "Responde de manera clara y breve a cada consulta, adaptando el nivel de detalle al contexto del usuario."
Diferencias: ["Se agrega claridad", "Se menciona el nivel de detalle", "Se adapta al contexto"]
Justificación: "La nueva versión establece expectativas más precisas y guía mejor el comportamiento del asistente."

Ejemplo 2:
Original: "Sé amable y útil."
Sugerido: "Mantén un tono amable y profesional en todas tus respuestas. Prioriza la claridad, ofrece ayuda práctica y adapta tu nivel de detalle según la complejidad de la consulta."
Diferencias: ["Se especifica el tono", "Se agrega enfoque en claridad y utilidad", "Se incluye contexto de complejidad"]
Justificación: "La versión mejorada convierte una sugerencia vaga en una guía concreta para la interacción."

Ahora mejora estas instrucciones:

ID del asistente: {assistant_id}
Instrucciones actuales:
"""
{instructions}
"""
```

---

## MCP Function Call (Simulada)

Aunque no se usó un SDK formal de MCP, este flujo simula una `function call` con los siguientes pasos:

```python
def mcp_flow(assistant_id):
    current = get_instructions(assistant_id)
    suggestion = ask_openai_for_suggestions(current, assistant_id)
    update_instructions(assistant_id, suggestion["comparison"]["suggested"])
```

Esto representa el corazón de la función MCP: **consultar, procesar, sugerir y actualizar**.

---

## Variables de Entorno

Define en `.env`:

```env
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=eyxxxxxx
OPENAI_API_KEY=sk-proj-xxxxxxxx
API_BASE_URL=http://localhost:8000
```

