from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer

# Create your views here.

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    

    
class VerifyEmailView(views.APIView):
    def post(self, request):
        token = request.data.get('token')
        user = User.objects.filter(verification_token=token).first()
        if user:
            user.is_verified = True
            user.is_active = True
            user.verification_token = None
            user.save()
            return Response({'message': 'Account verified.'})
        return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def retrieve(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully.'})
        except Exception:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

