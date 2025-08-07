from backend.clause_retriever import retrieve_relevant_clauses
from backend.llm_agent import make_decision

def handle(query: str, entities: dict) -> str:
    relevant_clauses = retrieve_relevant_clauses(query)
    decision = make_decision(query, relevant_clauses)

    return (
        f"Decision: {decision['decision']}\n"
        f"Amount: {decision.get('amount', 'N/A')}\n"
        f"Justification: {decision['justification']}\n"
        f"Clause(s): {', '.join(decision['clauses'])}"
    )
