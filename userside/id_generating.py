import uuid

def generate_order_id():
    return uuid.uuid4().hex[:10].upper() 