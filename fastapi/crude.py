from database import supabase

def get_assistant(assistant_id: str):
    response = supabase.table("assistants").select("*").eq("id", assistant_id).single().execute()
    return response.data

def create_assistant(name: str, instructions: str):
    response = supabase.table("assistants").insert({"name": name, "instructions": instructions}).execute()
    return response.data

def update_assistant(assistant_id: str, new_instructions: str):
    response = supabase.table("assistants").update({"instructions": new_instructions}).eq("id", assistant_id).execute()
    return response.data