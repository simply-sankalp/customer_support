def handle(query: str, entities: dict) -> str:
    claim_id = entities.get("claim_id")
    if not claim_id:
        return "Could you please provide a valid claim ID?"

    # Simulated result
    return f"Your claim ID {claim_id} was approved for ₹85,000 on July 14, 2025."
