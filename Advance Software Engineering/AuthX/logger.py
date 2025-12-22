import json
import time
import uuid

def log_info(endpoint, status, start):
    print(json.dumps({
        "request_id": str(uuid.uuid4()),
        "endpoint": endpoint,
        "status": status,
        "execution_time": round(time.time() - start, 4)
    }))

def log_warn(endpoint, status, start):
    log_info(endpoint, status, start)