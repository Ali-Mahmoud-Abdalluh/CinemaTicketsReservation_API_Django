from encodings import search_function
from shutil import move
from django.http.response import JsonResponse
from .models import Guest, Movie, Reservation
from rest_framework.decorators import api_view
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins, viewsets, filters

from tickets import serializers

# FBV (Function Based View)
# 1) without REST Framework and no model query


def no_rest_no_model(request):
    guests = [
        {
            'id': 1,
            'name': 'Omar',
            'mobile': "01000000000"
        },
        {
            'id': 2,
            'name': 'Khalid',
            'mobile': '01220000000'
        },
        {
            'id': 3,
            'name': 'Mik',
            'mobile': '01550000000'
        }
    ]
    return JsonResponse(guests, safe=False)

# 2) Without REST Framework , but from model


def no_rest_from_model(request):
    guests = Guest.objects.all()
    response = {
        # if values() left blank this will make it return all values
        'guests': list(guests.values('id', 'name', 'mobile'))
    }
    return JsonResponse(response)

# List == GET
# Create == POST
# Update == PUT
# Delete == DELETE

# 3) Function based views
# 3-1) GET POST


@api_view(['GET', 'POST'])
def FBV_List(request):
    # GET
    if request.method == 'GET':
        guest = Guest.objects.all()
        serializer = GuestSerializer(guest, many=True)
        return Response(serializer.data)
    # POST
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

# 3-2) GET PUT DELETE


@api_view(["GET", "PUT", "DELETE"])
def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CBV (Class Based View):
# 4.1 List and Create == GET and POST
class CBV_List(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializers = GuestSerializer(guests, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializers = GuestSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)


# 4.2 GET PUT DELETE classs based view pk
class CBV_pk(APIView):

    def get_object(self, pk):
        try:
            guest = Guest.objects.get(pk=pk)
            return guest
        except Guest.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        guest = self.get_object(pk=pk)
        serializers = GuestSerializer(guest)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        guest = self.get_object(pk=pk)
        serializers = GuestSerializer(guest, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk=pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 5 Maxins GET , POST
class mixins_list(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

# 5.2 Maxins GET , PUT , DELETE PK


class mixins_pk(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)

    def delete(self, request, pk):
        return self.delete(request)


# 6 Generics
# 6.1 GET and POST
class Generics_list(generics.ListAPIView, generics.CreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

# 6.2 GET and PUT and DELETE


class Generics_pk(generics.UpdateAPIView, generics.DestroyAPIView, generics.RetrieveAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

# 7 viewsets
# Guests
class Viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


# I will use viewsets for all other serializers models
# Movies
class Viewsets_movies(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["movie"]

# Reservations
class Viewsets_reservations(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

# make function based view to search for movie
@api_view(['GET'])
def find_movie(request):
    movie = Movie.objects.filter(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )
    serializer = MovieSerializer(movie, many=True)
    return Response(serializer.data)

# make function based view to create a reservation 
@api_view(['POST'])
def create_reservation(request):
    movie = Movie.objects.get(
        hall= request.data['hall'],
        movie= request.data['movie'],
    )
    
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()
    
    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()
    
    return Response(status = status.HTTP_201_CREATED)