import os
from typing import Annotated, TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from prompts import SYSTEM_PROMPT

# Načtení environment variables
load_dotenv()

# Definice stavu grafu
class State(TypedDict):
    messages: Annotated[list[BaseMessage], "The messages in the conversation"]

# Inicializace LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

import json

def get_resume():
    """Načte obsah životopisu ze souboru JSON."""
    try:
        with open("resume.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return json.dumps(data, indent=2, ensure_ascii=False)
    except FileNotFoundError:
        return "Životopis nebyl nalezen."
    except json.JSONDecodeError:
        return "Chyba při čtení JSON životopisu."

def laura_node(state: State):
    """Uzel asistentky Laury."""
    resume_content = get_resume()
    
    # Sestavení zpráv
    system_message = SystemMessage(content=SYSTEM_PROMPT.format(resume_content=resume_content))
    
    # Spuštění LLM
    response = llm.invoke([system_message] + state["messages"])
    
    return {"messages": [response]}

# Sestavení grafu
workflow = StateGraph(State)
workflow.add_node("laura", laura_node)
workflow.set_entry_point("laura")
workflow.add_edge("laura", END)

# Kompilace grafu
app = workflow.compile()

if __name__ == "__main__":
    print("Laura je připravena! (Napiš 'exit' pro ukončení)")
    messages = []
    while True:
        user_input = input("Vy: ")
        if user_input.lower() in ["exit", "quit", "konec"]:
            break
            
        messages.append(HumanMessage(content=user_input))
        
        # Spuštění grafu
        result = app.invoke({"messages": messages})
        
        # Získání poslední odpovědi
        ai_message = result["messages"][-1]
        print(f"Laura: {ai_message.content}")
        
        # Aktualizace historie zpráv
        messages.append(ai_message)
