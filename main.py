from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import psycopg2
from typing import List, Optional

app = FastAPI(title="AI-Assistant Ontology API")

@app.get("/v1/db-check")
def check_db():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "postgres"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS", "postgres")
        )
        return {"status": "connected", "database": "PostgreSQL"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

class UserIssue(BaseModel):
    raw_text: str


class EnrichmentResult(BaseModel):
    issue_id: int
    detected_concepts: List[str]
    status: str


class UpdateReport(BaseModel):
    additional_info: str
    confirmed: bool

# Список терминов из Protege
ontology = [
    {"id": 1, "term": "Сбой авторизации", "class": "SoftwareIssue"},
    {"id": 2, "term": "Проблема с роутером", "class": "HardwareIssue"},
    {"id": 3, "term": "Низкая скорость", "class": "NetworkIssue"}
]

# Хранилище созданных отчетов
reports_db = {}


# --- GET: Получить все термины из онтологии ---
@app.get("/v1/ontology/terms", tags=["Ontology"])
def get_all_terms():
    return {"source": "Protege KB", "terms": ontology}


# --- GET: Получить конкретный термин по ID ---
@app.get("/v1/ontology/terms/{term_id}", tags=["Ontology"])
def get_term_by_id(term_id: int):
    term = next((t for t in ontology if t["id"] == term_id), None)
    if not term:
        raise HTTPException(status_code=404, detail="Термин не найден в базе знаний")
    return term


# --- POST: Анализ ---
@app.post("/v1/enrichment/analyze", response_model=EnrichmentResult, tags=["AI Logic"])
def analyze_issue(issue: UserIssue):
    # Здесь в будущем будет логика сопоставления текста с онтологией
    new_id = len(reports_db) + 1
    concepts = ["Detected: " + t["term"] for t in ontology if t["term"].lower() in issue.raw_text.lower()]

    result = {
        "issue_id": new_id,
        "detected_concepts": concepts if concepts else ["General Issue"],
        "status": "waiting_for_refinement"
    }
    reports_db[new_id] = {"raw": issue.raw_text, "concepts": concepts, "extra": ""}
    return result


# --- POST: Создание финального тикета ---
@app.post("/v1/tickets", status_code=201, tags=["Support"])
def create_ticket(issue: UserIssue):
    ticket_id = len(reports_db) + 100
    return {"ticket_id": ticket_id, "message": "Тикет успешно создан в системе техподдержки"}


# --- PUT: Уточнение данных ---
@app.put("/v1/enrichment/refine/{issue_id}", tags=["AI Logic"])
def refine_issue(issue_id: int, update: UpdateReport):
    if issue_id not in reports_db:
        raise HTTPException(status_code=404, detail="Запрос не найден")

    reports_db[issue_id]["extra"] = update.additional_info
    return {
        "message": f"Данные для запроса {issue_id} обновлены",
        "current_report": reports_db[issue_id]
    }


# --- DELETE: Удаление запроса ---
@app.delete("/v1/enrichment/cancel/{issue_id}", tags=["AI Logic"])
def cancel_analysis(issue_id: int):
    if issue_id in reports_db:
        del reports_db[issue_id]
        return {"status": "success", "message": f"Запрос {issue_id} удален"}
    raise HTTPException(status_code=404, detail="Запрос не найден")