from datetime import date, datetime
from fastapi.responses import JSONResponse


def convert_dates(obj):
    if isinstance(obj, dict):
        return {k: convert_dates(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_dates(item) for item in obj]
    elif isinstance(obj, (date, datetime)):
        return obj.strftime('%Y-%m-%d')  # También podés usar '%d/%m/%Y'
    return obj


def success_response(data, message='success'):
    return JSONResponse(content={
        "status": "success",
        "data": convert_dates(data),
        "message": message
    })


def error_response(message='error', status_code=400):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message
        }
    )
