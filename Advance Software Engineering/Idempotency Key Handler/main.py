import json
from datetime import datetime

# In-memory store to track processed requests
# Key   -> request_id
# Value -> stored response
PROCESSED_REQUESTS = {}


def log_event(request_id, status):
    """
    Structured logging.
    Helps in debugging duplicate or failed requests.
    """
    print(json.dumps({
        "request_id": request_id,
        "status": status,
        "timestamp": datetime.utcnow().isoformat()
    }))


def process_payment(request_id: str, amount: float) -> dict:
    """
    Ensures idempotent payment processing.

    Why idempotency is important:
    - Clients may retry requests due to network failures
    - Without idempotency, retries could cause double charges

    Production note:
    - request_id is usually stored in DB or Redis
    - API gateways or payment providers enforce this automatically
    """

    # Input validation
    if amount <= 0:
        log_event(request_id, "INVALID")
        return {"error": "Invalid amount"}

    # Check for duplicate request
    if request_id in PROCESSED_REQUESTS:
        log_event(request_id, "DUPLICATE")
        return PROCESSED_REQUESTS[request_id]

    # Simulate payment processing
    response = {
        "request_id": request_id,
        "amount": amount,
        "status": "SUCCESS"
    }

    # Store result to ensure idempotency
    PROCESSED_REQUESTS[request_id] = response

    log_event(request_id, "PROCESSED")
    return response



# --------------------------------------------------------
# Example Execution
# print(process_payment("req-1001", 250))
# print(process_payment("req-1001", 250))  # Duplicate request
# print(process_payment("req-1002", -10))  # Invalid request
# --------------------------------------------------------