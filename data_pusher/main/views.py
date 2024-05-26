from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
import requests
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

@api_view(['GET'])
def get_destinations(request, account_id):
    account = get_object_or_404(Account, account_id=account_id)
    destinations = account.destinations.all()
    serializer = DestinationSerializer(destinations, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def incoming_data(request):
    token = request.headers.get('CL-X-TOKEN')
    if not token:
        return Response({"message": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        account = Account.objects.get(app_secret_token=token)
    except Account.DoesNotExist:
        return Response({"message": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)

    if not request.content_type == 'application/json':
        return Response({"message": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data
    destinations = account.destinations.all()

    for destination in destinations:
        headers = destination.headers
        url = destination.url
        method = destination.http_method

        if method == 'GET':
            response = requests.get(url, headers=headers, params=data)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data)

        # Handle response if needed

    return Response({"message": "Data pushed to destinations"}, status=status.HTTP_200_OK)

# Create your views here.
