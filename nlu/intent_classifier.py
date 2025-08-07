import subprocess
import difflib
import re

# Define all valid intent codes
VALID_INTENTS = {
    "claim_registration",
    "premium_calculator",
    "grievance_filing",
    "policy_issuance_tracker",
    "claim_status_inquiry",
    "branch_locator",
    "hospital_network_lookup",
    "garage_network_lookup",
    "claim_settlement_flow",
    "surveyor_duties",
    "non_motor_docs_list",
    "hospital_standards_info",
    "policy_coverage_query"
}

# Prompt with few-shot examples to improve consistency
INTENT_PROMPT_TEMPLATE = """
You are an intent classification engine for an insurance assistant.

Classify the user's query into one of the following intents:
- claim_registration
- premium_calculator
- grievance_filing
- policy_issuance_tracker
- claim_status_inquiry
- branch_locator
- hospital_network_lookup
- garage_network_lookup
- claim_settlement_flow
- surveyor_duties
- non_motor_docs_list
- hospital_standards_info
- policy_coverage_query

Below are examples:

Query: "I want to register a claim for knee surgery."
Intent: claim_registration

Query: "What is the premium for a 60-year-old in Mumbai?"
Intent: premium_calculator

Query: "I have a complaint about the delay in my claim."
Intent: grievance_filing

Query: "Has my policy been issued?"
Intent: policy_issuance_tracker

Query: "What's the status of claim ID 123456?"
Intent: claim_status_inquiry

Query: "Where is your branch in Bangalore?"
Intent: branch_locator

Query: "Which hospitals are in your network in Pune?"
Intent: hospital_network_lookup

Query: "Where can I get my car repaired under insurance?"
Intent: garage_network_lookup

Query: "What is the claim settlement process?"
Intent: claim_settlement_flow

Query: "What are the duties of a loss surveyor?"
Intent: surveyor_duties

Query: "What documents do I need for a non-motor claim?"
Intent: non_motor_docs_list

Query: "How are hospitals in your provider network evaluated?"
Intent: hospital_standards_info

Query: "Is ACL reconstruction covered in my policy?"
Intent: policy_coverage_query

Now classify the following:

Query: "{query}"
Intent:
"""

def call_ollama(prompt: str, model: str = "llama3") -> str:
    """Call local LLM using Ollama subprocess."""
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode().strip()

def extract_intent(raw_response: str) -> str:
    """Extract the correct intent from LLM response using regex."""
    pattern = r"\b(" + "|".join(re.escape(intent) for intent in VALID_INTENTS) + r")\b"
    match = re.search(pattern, raw_response, flags=re.IGNORECASE)
    if match:
        return match.group(1).lower()

    # Optional: fuzzy match fallback
    close_matches = difflib.get_close_matches(raw_response.lower(), VALID_INTENTS, n=1, cutoff=0.7)
    return close_matches[0] if close_matches else "unknown"

def classify_intent(query: str, model: str = "llama3") -> str:
    """Use LLM to classify the user query into a predefined intent."""
    intent_list = "\n- " + "\n- ".join(sorted(VALID_INTENTS))
    prompt = INTENT_PROMPT_TEMPLATE.format(query=query, intent_list=intent_list)

    raw_response = call_ollama(prompt, model=model)
    # print("LLM raw output:", raw_response)  # Debugging output

    return extract_intent(raw_response)
    

# TESTING
# def main():
#     query = "46 year old male, knee injury, 3 month policy"
#     intent = classify_intent(query)

#     print(intent)

# if __name__ == "__main__":
#     main()
