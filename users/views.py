from django.http import JsonResponse

def index(request):
    response_data = {"message": "Hello, world. You're at the users endpoint."}
    return JsonResponse(response_data)
