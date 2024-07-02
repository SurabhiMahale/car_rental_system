from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Car
from .serializers import UserSerializer, CarSerializer

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Account successfully created", "status_code": 200, "user_id": serializer.data['id']})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    try:
        user = User.objects.get(username=request.data['username'])
        if user.check_password(request.data['password']):
            refresh = RefreshToken.for_user(user)
            return Response({
                "status": "Login successful",
                "status_code": 200,
                "user_id": user.id,
                "access_token": str(refresh.access_token),
                # "refresh_token": str(refresh)
            })
        else:
            return Response({"status": "Incorrect username/password provided. Please retry", "status_code": 401})
    except User.DoesNotExist:
        return Response({"status": "User not found", "status_code": 404})

# Add new car for renting
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_car(request):
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        
    # if request.user.role != 'admin':
    #     return Response({'detail': 'Permission denied. Only admins can add cars.'}, status=status.HTTP_403_FORBIDDEN)
    
    data = request.data
    car = Car.objects.create(
        category=data['category'],
        model=data['model'],
        number_plate=data['number_plate'],
        current_city=data['current_city'],
        rent_per_hr=data['rent_per_hr'],
        rent_history=data.get('rent_history', [])
    )
    return Response({
        'message': 'Car added successfully',
        'car_id': car.id,
        'status_code': 200
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_rides(request):
    origin = request.query_params.get('origin')
    destination = request.query_params.get('destination')
    category = request.query_params.get('category')
    required_hours = int(request.query_params.get('required_hours'))

    cars = Car.objects.filter(current_city=origin, category=category)
    available_cars = []
    for car in cars:
        total_payable_amt = car.rent_per_hr * required_hours
        available_cars.append({
            "car_id": car.id,
            "category": car.category,
            "model": car.model,
            "number_plate": car.number_plate,
            "current_city": car.current_city,
            "rent_per_hr": car.rent_per_hr,
            "rent_history": car.rent_history,
            "total_payable_amt": total_payable_amt
        })
    return Response(available_cars)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rent_car(request):
    try:
        car = Car.objects.get(id=request.data['car_id'])
        rent_history = car.rent_history
        rent_history.append({
            "origin": request.data['origin'],
            "destination": request.data['destination'],
            "amount": car.rent_per_hr * request.data['hours_requirement']
        })
        car.rent_history = rent_history
        car.save()
        return Response({"status": "Car rented successfully", "status_code": 200, "rent_id": car.id, "total_payable_amt": car.rent_per_hr * request.data['hours_requirement']})
    except Car.DoesNotExist:
        return Response({"status": "No car is available at the moment", "status_code": 400})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_rent_history(request):
    if request.user.role != 'admin':
        return Response({"message": "Unauthorized", "status_code": 403})

    try:
        car = Car.objects.get(id=request.data['car_id'])
        car.rent_history = request.data['rent_history']
        car.save()
        return Response({"message": "Rent history updated successfully", "status_code": 200})
    except Car.DoesNotExist:
        return Response({"message": "Car not found", "status_code": 404})
