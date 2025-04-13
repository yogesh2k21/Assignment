import uuid

# Enhanced discount generator with length parameter
def generate_discount_code(prefix="DISC", length=8, separator="-"):
    code = uuid.uuid4().hex[:length].upper()
    return f"{prefix}{separator}{code}"