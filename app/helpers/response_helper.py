def success_response(data, message="OK", status_code=200):
    return {
        "status": "success",
        "message": message,
        "data": data
    }, status_code

def error_response(message="Error", status_code=400):
    return {
        "status": "error",
        "message": message
    }, status_code
