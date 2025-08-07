from nlu.intent_classifier import classify_intent
from nlu.entity_extractor import extract_entities
from intents import (
    claim_status,
    policy_clause_checker,
    # hospital_network
)

INTENT_HANDLERS = {
    "claim_status_inquiry": claim_status.handle,
    "policy_coverage_query": policy_clause_checker.handle,
    # "hospital_network_lookup": hospital_network.handle
}

def main():
    query = input("Ask your insurance question: ")
    
    intent = classify_intent(query)
    entities = extract_entities(query, intent)

    handler = INTENT_HANDLERS.get(intent)
    
    if not handler:
        print("Sorry, I couldn't understand your query.")
        return

    response = handler(query, entities)
    print(response)

if __name__ == "__main__":
    main()
