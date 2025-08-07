import subprocess

def call_ollama(prompt: str, model="llama3") -> str:
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode()

def make_decision(query: str, clauses: list) -> dict:
    prompt = f"""
You are an insurance decision engine. Based on the following query and policy clauses, determine:
- Whether the claim should be approved
- If yes, the amount
- Justification
- Cite the clause numbers used

Query: {query}
Policy Clauses:
{clauses}

Return your answer in this JSON format:
{{
    "decision": "approved/rejected",
    "amount": "₹...",
    "justification": "...",
    "clauses": ["C.1", "Table 3"]
}}
"""
    raw_output = call_ollama(prompt)
    # You can add JSON parsing + error handling here
    return eval(raw_output.strip())
