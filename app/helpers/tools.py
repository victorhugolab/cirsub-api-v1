from fastapi import Request
import json

def get_client_ip(request: Request) -> str:
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.client.host
    return ip



def parse_json(row: dict) -> dict:
    """
    Recorre cada campo del diccionario y convierte los que sean JSON válidos.
    """
    for k, v in row.items():
        if isinstance(v, str):
            try:
                row[k] = json.loads(v)
            except (json.JSONDecodeError, TypeError):
                pass  # Si no es JSON válido, lo deja como está
    return row
