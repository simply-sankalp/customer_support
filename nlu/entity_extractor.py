import re

def extract_entities(query: str, intent: str) -> dict:
    if intent == "claim_status_inquiry":
        claim_id = re.search(r'\d{6,}', query)
        return {"claim_id": claim_id.group() if claim_id else None}
    
    elif intent == "hospital_network_lookup":
        # crude location detection
        cities = ["Pune", "Mumbai", "Delhi", "Bangalore"]
        location = next((city for city in cities if city.lower() in query.lower()), None)
        return {"location": location}
    
    return {}
