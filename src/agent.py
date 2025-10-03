import os
import json
from typing import Dict, Any, List
import google.generativeai as genai
from google.generativeai import types

from dotenv import load_dotenv
from tools import kb, tickets, http_tool

load_dotenv()  # loads .env

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)


GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-exp")
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Set GEMINI_API_KEY environment variable")

client = genai.GenerativeModel(GEMINI_MODEL)

TOOLS = {
    "search_kb": {
        "description": "Search local knowledge-base. Input: a query string. Returns: list of kb items.",
        "args": {"query": "string", "top_k": "int"}
    },
    "create_ticket": {
        "description": "Create a support ticket. Input: customer_name, customer_email, subject, body. Returns ticket_id."
    },
    "http_get": {
        "description": "Make a HTTP GET request to an external API when needed."
    }
}

def call_gemini_planner(user_message: str, context: Dict[str, Any]=None) -> str:
    prompt = f"""
You are an autonomous Customer Support planner. Given the user's message, produce a JSON plan with an array 'plan'.
Each step is an object with fields:
- action: one of ['search_kb','create_ticket','http_get','respond']
- args: object with arguments for the action
- reason: short explanation

Return only valid JSON.

User message: {user_message}
Available tools and descriptions: {json.dumps(TOOLS, indent=0)}
"""
    response = client.generate_content(prompt)
    text = response.text
    try:
        j = json.loads(text)
        return j
    except Exception:
        import re
        m = re.search(r'(\{.*\})', text, re.S)
        if m:
            try:
                return json.loads(m.group(1))
            except Exception:
                raise RuntimeError("Planner produced non-JSON response: " + text)
        else:
            raise RuntimeError("Planner produced non-JSON response: " + text)

def execute_plan(plan: List[Dict[str,Any]]):
    trace = []
    final_text = None
    for step in plan:
        action = step.get("action")
        args = step.get("args", {})
        reason = step.get("reason", "")
        entry = {"action":action, "reason": reason, "args": args, "result": None}
        if action == "search_kb":
            q = args.get("query")
            top_k = args.get("top_k", 5)
            res = kb.search_kb(q, top_k=top_k)
            entry["result"] = res
        elif action == "create_ticket":
            cid = tickets.create_ticket(args.get("customer_name","unknown"),
                                        args.get("customer_email","unknown"),
                                        args.get("subject","no-subject"),
                                        args.get("body",""))
            entry["result"] = {"ticket_id": cid}
        elif action == "http_get":
            url = args.get("url")
            res = http_tool.http_get(url)
            entry["result"] = res
        elif action == "respond":
            final_text = args.get("text")
            entry["result"] = {"delivered_text": final_text}
        else:
            entry["result"] = {"error": f"unknown action {action}"}
        trace.append(entry)
    if not final_text:
        summary = {"trace": trace}
        prompt = f"""
Given the following execution trace of tools and findings, write a friendly customer-facing reply summarizing what we found, next steps, and a polite closing.

Execution trace (JSON): {json.dumps(summary)}
"""
        response = client.generate_content(prompt)
        final_text = response.text
        trace.append({"action":"synthesize_reply","result": final_text})
    return {"final_text": final_text, "trace": trace}

def handle_user_message(user_message: str, metadata: Dict[str,Any]=None):
    planner_out = call_gemini_planner(user_message, metadata)
    plan = planner_out.get("plan", [])
    res = execute_plan(plan)
    return res
