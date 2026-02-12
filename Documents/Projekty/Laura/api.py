import os
import json
import sys
from typing import Annotated, TypedDict, List, Literal, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, END
from prompts import SYSTEM_PROMPT, PROMPT_TOPIC_TYPE, SCHEDULING_PROMPT, CLASSIFY_MEETING_PROMPT, CLASSIFY_DATE_PROMPT, CLASSIFY_TIME_PROMPT, CLASSIFY_DURATION_PROMPT, CLASSIFY_EMAIL_PROMPT, CLASSIFY_PHONE_PROMPT, EXTRACT_QUESTIONS_PROMPT

# Načtení environment variables
load_dotenv()

app = FastAPI()

# Povolení CORS pro frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from datetime import datetime

# Definice stavu grafu
class State(TypedDict):
    messages: Annotated[List[BaseMessage], "The messages in the conversation"]
    topic: Optional[Literal["info", "date"]] = None
    question: Optional[List[str]] = None
    meeting_type: Optional[Literal["initial", "business_consultation", "technical_consultation", "urgent", "other"]] = None
    meeting_date: Optional[str] = None
    meeting_time: Optional[str] = None
    meeting_duration: int = 60
    meeting_email: Optional[str] = None
    meeting_phone: Optional[str] = None
    date_now: str = datetime.now().strftime("%Y-%m-%d")

# Inicializace LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

def get_simulated_slots(date: str):
    """Simuluje volné termíny pro dané datum."""
    return ["09:00", "11:00", "14:00", "16:00"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_resume():
    """Načte obsah životopisu ze souboru JSON."""
    try:
        resume_path = os.path.join(BASE_DIR, "resume.json")
        with open(resume_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return json.dumps(data, indent=2, ensure_ascii=False)
    except Exception:
        return "Informace nejsou momentálně k dispozici."

def function_topic_type(state: State):
    """Rozhodne, zda jde o info nebo o schůzku, a zkusí identifikovat všechny parametry."""
    last_message = state["messages"][-1].content
    date_now = state.get("date_now") or datetime.now().strftime("%Y-%m-%d")
    
    router_resp = llm.invoke([
        SystemMessage(content=PROMPT_TOPIC_TYPE),
        HumanMessage(content=last_message)
    ])
    task = router_resp.content.strip().lower()
    
    # Základní stav
    res = {
        "topic": "info",
        "question": state.get("question"),
        "meeting_type": state.get("meeting_type"),
        "meeting_date": state.get("meeting_date"),
        "meeting_time": state.get("meeting_time"),
        "meeting_duration": state.get("meeting_duration") or 60,
        "meeting_email": state.get("meeting_email"),
        "meeting_phone": state.get("meeting_phone"),
        "date_now": date_now
    }

    if "date" in task:
        res["topic"] = "date"
        
        # Zkusíme vytáhnout parametry hned
        prompts = {
            "meeting_type": CLASSIFY_MEETING_PROMPT,
            "meeting_date": CLASSIFY_DATE_PROMPT.format(date_now=date_now),
            "meeting_time": CLASSIFY_TIME_PROMPT,
            "meeting_duration": CLASSIFY_DURATION_PROMPT,
            "meeting_email": CLASSIFY_EMAIL_PROMPT,
            "meeting_phone": CLASSIFY_PHONE_PROMPT
        }
        
        for key, pr in prompts.items():
            if not res[key] or res[key] == "none":
                resp = llm.invoke([SystemMessage(content=pr), HumanMessage(content=last_message)])
                val = resp.content.strip()
                if val.lower() != "none":
                    if key == "meeting_duration":
                        try: res[key] = int(val)
                        except: pass
                    else:
                        res[key] = val
    else:
        # Pokud je topic == "info", zkusíme extrahovat otázky
        questions_resp = llm.invoke([
            SystemMessage(content=EXTRACT_QUESTIONS_PROMPT),
            HumanMessage(content=last_message)
        ])
        questions_text = questions_resp.content.strip()
        
        if questions_text.lower() != "none" and questions_text:
            # Rozdělíme na jednotlivé otázky (každá na novém řádku)
            questions = [q.strip() for q in questions_text.split("\n") if q.strip()]
            if questions:
                res["question"] = questions
        else:
            # Pokud nebyly extrahovány otázky, ponecháme stávající nebo None
            if not res["question"]:
                res["question"] = None
        
    return res

def function_give_info(state: State):
    """Uzel pro poskytování informací o Davidovi."""
    resume_content = get_resume()
    
    # Sestavení systémové zprávy s životopisem
    system_msg = SystemMessage(content=SYSTEM_PROMPT.format(resume_content=resume_content))
    
    # Příprava zpráv pro LLM (systémová zpráva + historie konverzace)
    # state["messages"] již obsahuje poslední zprávu uživatele
    response = llm.invoke([system_msg] + state["messages"])
    
    # Vrátíme nový stav s přidanou odpovědí a vymazanými otázkami (protože byly zodpovězeny)
    return {
        "messages": [response],
        "question": state.get("question")
    }

def scheduling_node(state: State):
    """Uzel pro domlouvání schůzky s kalendářem."""
    last_message = state["messages"][-1].content
    date_now = state.get("date_now") or datetime.now().strftime("%Y-%m-%d")
    
    # Aktuální hodnoty
    res = {
        "meeting_type": state.get("meeting_type"),
        "meeting_date": state.get("meeting_date"),
        "meeting_time": state.get("meeting_time"),
        "meeting_duration": state.get("meeting_duration") or 60,
        "meeting_email": state.get("meeting_email"),
        "meeting_phone": state.get("meeting_phone")
    }

    # Pokus o extrakci chybějících
    prompts = {
        "meeting_type": CLASSIFY_MEETING_PROMPT,
        "meeting_date": CLASSIFY_DATE_PROMPT.format(date_now=date_now),
        "meeting_time": CLASSIFY_TIME_PROMPT,
        "meeting_duration": CLASSIFY_DURATION_PROMPT,
        "meeting_email": CLASSIFY_EMAIL_PROMPT,
        "meeting_phone": CLASSIFY_PHONE_PROMPT
    }

    for key, pr in prompts.items():
        if not res[key] or res[key] == "none":
            resp = llm.invoke([SystemMessage(content=pr), HumanMessage(content=last_message)])
            val = resp.content.strip()
            if val.lower() != "none":
                if key == "meeting_duration":
                    try: res[key] = int(val)
                    except: pass
                else: res[key] = val

    slots = get_simulated_slots(res["meeting_date"]) if res["meeting_date"] and res["meeting_date"] != "none" else []
    
    system_msg = SystemMessage(content=SCHEDULING_PROMPT.format(
        meeting_type=res["meeting_type"] or "zatím neznámý",
        meeting_date=res["meeting_date"] or "zatím neznámé",
        meeting_time=res["meeting_time"] or "zatím neznámý",
        meeting_duration=res["meeting_duration"],
        meeting_email=res["meeting_email"] or "zatím neznámý",
        meeting_phone=res["meeting_phone"] or "zatím neznámý",
        available_slots=", ".join(slots) if slots else "budou k dispozici po výběru data",
        date_now=date_now
    ))
    
    response = llm.invoke([system_msg] + state["messages"])
    
    return {
        "messages": [response], 
        "meeting_type": res["meeting_type"],
        "meeting_date": res["meeting_date"],
        "meeting_time": res["meeting_time"],
        "meeting_duration": res["meeting_duration"],
        "meeting_email": res["meeting_email"],
        "meeting_phone": res["meeting_phone"]
    }

def route_selection(state: State):
    """Rozcestník pro graf."""
    return state.get("topic", "info")

# Sestavení grafu
workflow = StateGraph(State)

workflow.add_node("node_topic_type", function_topic_type)
workflow.add_node("node_give_info", function_give_info)
workflow.add_node("scheduling", scheduling_node)

workflow.set_entry_point("node_topic_type")

workflow.add_conditional_edges(
    "node_topic_type",
    route_selection,
    {
        "info": "node_give_info",
        "date": "scheduling"
    }
)

workflow.add_edge("node_give_info", END)
workflow.add_edge("scheduling", END)

graph = workflow.compile()

# API Modely
class ChatRequest(BaseModel):
    message: str
    history: List[dict] = []
    topic: Optional[str] = None
    question: Optional[List[str]] = None
    meeting_type: Optional[str] = None
    meeting_date: Optional[str] = None
    meeting_time: Optional[str] = None
    meeting_duration: int = 60
    meeting_email: Optional[str] = None
    meeting_phone: Optional[str] = None
    date_now: Optional[str] = None

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Převod historie na objekty zpráv
        messages = []
        for msg in request.history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
        
        messages.append(HumanMessage(content=request.message))
        
        # Spuštění grafu s aktuálním stavem
        now = request.date_now or datetime.now().strftime("%Y-%m-%d")
        initial_state = {
            "messages": messages,
            "topic": request.topic,
            "question": request.question,
            "meeting_type": request.meeting_type,
            "meeting_date": request.meeting_date,
            "meeting_time": request.meeting_time,
            "meeting_duration": request.meeting_duration,
            "meeting_email": request.meeting_email,
            "meeting_phone": request.meeting_phone,
            "date_now": now
        }
        
        result = graph.invoke(initial_state)
        ai_message = result.get("messages")[-1]
        
        # Zaručíme, že všechny klíče jsou v odpovědi, i ty s hodnotou None
        return {
            "response": ai_message.content,
            "topic": result.get("topic"),
            "question": result.get("question"),
            "meeting_type": result.get("meeting_type"),
            "meeting_date": result.get("meeting_date"),
            "meeting_time": result.get("meeting_time"),
            "meeting_duration": result.get("meeting_duration"),
            "meeting_email": result.get("meeting_email"),
            "meeting_phone": result.get("meeting_phone"),
            "date_now": result.get("date_now")
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Statické soubory pro frontend
static_dir = os.path.join(BASE_DIR, "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8021))
    uvicorn.run(app, host="0.0.0.0", port=port)
