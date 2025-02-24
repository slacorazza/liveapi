class CorsMiddleware:
    """
    Middleware to add Access-Control-Allow-Origin header to responses.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "https://ofiservices.pythonanywhere.com/"
        return response