import subprocess
import difflib

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
    """Call the local LLM using Ollama subprocess."""
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode().strip().lower()

def classify_intent(query: str, model: str = "llama3") -> str:
    """Classify the intent of the user query using an LLM."""
    prompt = INTENT_PROMPT_TEMPLATE.format(query=query)
    raw_intent = call_ollama(prompt, model=model)

    # Clean up the LLM output
    intent = raw_intent.split()[0].strip(",.").lower()

    # Validate against known intents
    if intent in VALID_INTENTS:
        return intent
    else:
        # Try fuzzy matching if there's a small typo
        close_matches = difflib.get_close_matches(intent, VALID_INTENTS, n=1, cutoff=0.7)
        if close_matches:
            return close_matches[0]
        return "unknown"
