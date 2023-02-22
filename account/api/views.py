from rest_framework import generics
from rest_framework.response import Response
from .serializers import LoginSerializer, RegistrationSerializer, VerifySerializer, SendResetCodeSerializer,ChangePasswordSerializer
from django.contrib.auth import get_user_model, login, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class LoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data.get("email")
        password = serializer.data.get("password")

        user = authenticate(email=email, password=password)
        print(user)
        login(request, user)

        refresh = RefreshToken.for_user(user)
        tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
       
        return Response({"email": email, "tokens": tokens}, status=201)



class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # login(request, user)
        return Response({"Status": "success", "data": serializer.data}, status=200)


class VerifyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = VerifySerializer
    lookup_field = "id"

    def put(self, request, *args, **kwargs):
        obj=self.get_object()
        serializer = self.serializer_class(data=request.data,instance=obj)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # print(request.dat)
        login(request, user)
        return Response({"Status": "success"}, status=201)
    
    
class SendResetCodeView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SendResetCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = User.objects.filter(email=serializer.data['email'])[0].id
        print(id)


        return Response({"id":id,"data": serializer.data,"Status":"success"},status=201)

    
    
class ChangePasswordVerifyView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    lookup_field = "id"

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.serializer_class(data=request.data,instance=obj)
        
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        login(request, user)
        return Response({'Status':'Success'}, status=201)