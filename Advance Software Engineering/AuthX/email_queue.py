# Simulated message queue
QUEUE = []

def publish_event(event_type, username):
    QUEUE.append({
        "event": event_type,
        "user": username
    })