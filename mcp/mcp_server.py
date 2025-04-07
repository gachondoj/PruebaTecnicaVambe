import requests
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()  # Carga tu API key de .env

API_BASE_URL = "http://localhost:8000"  # Tu API local de FastAPI
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

def get_instructions(assistant_id: str) -> str:
    response = requests.get(f"{API_BASE_URL}/assistants/{assistant_id}")
    if response.status_code == 200:
        return response.json()["instructions"]
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

def ask_claude_for_suggestions(instructions: str, assistant_id: str) -> dict:
    prompt = f"""
Estás actuando como un editor experto de instrucciones para asistentes virtuales.
Dado el siguiente bloque de instrucciones, sugiere una mejora clara, profesional y concisa.

ID del asistente: {assistant_id}
Instrucciones actuales:
\"\"\"
{instructions}
\"\"\"

Devuelve tu respuesta en formato JSON con las claves:
- suggested_instructions
- explanation
"""

    response = client.messages.create(
        model="claude-3-sonnet-20240229",  # o haiku u opus si tienes acceso
        max_tokens=500,
        temperature=0.7,
        system="Eres un asistente que mejora instrucciones para otros asistentes.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Claude responde con texto. Intentamos parsearlo como JSON.
    import json
    import re

    # Busca el primer bloque de texto tipo JSON entre llaves
    match = re.search(r'\{[\s\S]*\}', response.content[0].text)
    if match:
        return json.loads(match.group(0))
    else:
        raise ValueError("Claude no devolvió un JSON válido.")

def mcp_flow(assistant_id: str):
    print("📥 Obteniendo instrucciones...")
    current = get_instructions(assistant_id)

    print("🤖 Pidiendo sugerencias a Claude...")
    suggestion = ask_claude_for_suggestions(current, assistant_id)

    print("\n💡 Sugerencia de Claude:")
    print(f"- Nueva versión:\n{suggestion['suggested_instructions']}")
    print(f"- Explicación: {suggestion['explanation']}")

    if input("\n¿Aplicar esta sugerencia? (s/n): ").lower() == "s":
        update_instructions(assistant_id, suggestion["suggested_instructions"])
    else:
        print("🛑 No se aplicaron cambios.")

if __name__ == "__main__":
    assistant_id = input("🆔 Ingresa el ID del assistant: ")
    mcp_flow(assistant_id)
