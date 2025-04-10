import json
import re
import requests
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = "http://localhost:8000"  # API local de FastAPI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def get_instructions(assistant_id: str) -> str:
    response = requests.get(f"{API_BASE_URL}/assistants/{assistant_id}")
    if response.status_code == 200:
        print(response.json())
        return response.json()['instructions']
    else:
        raise Exception("No se pudo obtener el assistant")

def update_instructions(assistant_id: str, new_instructions: str):
    response = requests.put(
        f"{API_BASE_URL}/assistants/{assistant_id}",
        json={"instructions": new_instructions}
    )
    if response.status_code == 200:
        print("✅ Instrucciones actualizadas.")
    else:
        print("❌ Error al actualizar:", response.text)

def ask_openai_for_suggestions(instructions: str, assistant_id: str) -> dict:
    prompt = f"""
Estás actuando como un editor experto de instrucciones para asistentes virtuales.

Ejemplo 1:
Instrucción original: "Responde a lo que te digan."
Sugerencia: "Responde de manera clara y breve a cada consulta, adaptando el nivel de detalle al contexto del usuario."

Ejemplo 2:
Intrucción: Sé amable y útil.
Sugerencia: Mantén un tono amable y profesional en todas tus respuestas. Prioriza la claridad, ofrece ayuda práctica y adapta tu nivel de detalle según la complejidad de la consulta.

Ahora, dado el siguiente bloque de instrucciones, sugiere una mejora clara, profesional y concisa.

ID del asistente: {assistant_id}
Instrucciones actuales:
\"\"\" 
{instructions}
\"\"\"

Devuelve tu respuesta en formato JSON con las claves:
- suggested_instructions
- explanation
"""

    response = client.chat.completions.create(model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Eres un asistente que mejora instrucciones para otros asistentes."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=500,
    temperature=0.7)

    try:
        suggestion = response.choices[0].message.content.strip()
        match = re.search(r'\{[\s\S]*\}', suggestion)
        if match:
            suggestion_dict = json.loads(match.group(0))
            return suggestion_dict
        else:
            raise ValueError("OpenAI no devolvió un JSON válido.")

        
    except Exception as e:
        raise ValueError(f"Error al procesar la respuesta de OpenAI: {e}")

def mcp_flow(assistant_id: str):
    print("📥 Obteniendo instrucciones...")
    current = get_instructions(assistant_id)

    print("🤖 Pidiendo sugerencias a OpenAI...")
    suggestion = ask_openai_for_suggestions(current, assistant_id)

    print("\n💡 Sugerencia de OpenAI:")
    print(f"- Nueva versión:\n{suggestion['suggested_instructions']}")
    print(f"- Explicación: {suggestion['explanation']}")

    if input("\n¿Aplicar esta sugerencia? (s/n): ").lower() == "s":
        update_instructions(assistant_id, suggestion["suggested_instructions"])
    else:
        print("🛑 No se aplicaron cambios.")

if __name__ == "__main__":
    assistant_id = input("🆔 Ingresa el ID del assistant: ")
    mcp_flow(assistant_id)
