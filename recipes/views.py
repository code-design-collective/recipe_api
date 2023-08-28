from django.http import JsonResponse

def index(request):
    response_data = {"message": "Hello, world. You're at the recipes endpoint."}
    return JsonResponse(response_data)
