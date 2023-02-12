from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.conf import settings
from account.utils import create_activation_code,create_password_reset_code

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})


    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError({"Sifre ve ya email yalnisdir"})

        #if len(password) < 6:
        #    raise serializers.ValidationError({"Sifre en azi 6 simvoldan ibaret olmalidir"})
        return attrs



class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type":"password"})
    matchPassword = serializers.CharField(style={"input_type":"password"},write_only=True)
    class Meta:
        model = User
        fields = ("email", "name", "surname","password","company_name", "id","matchPassword")
        extra_kwargs = {
            "password": {
                "write_only": True
            },
            "slug": {
                "read_only": True
            }
        }


    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        matchPassword = attrs.pop("matchPassword")

        email_qs = User.objects.filter(email=email).exists()
        if password != matchPassword:
            raise serializers.ValidationError("Password tekrarinda xeta bas verib")
        if email_qs:
            raise serializers.ValidationError("Bu email ile artiq qeydiyyatdan kecilib")
        if password:
            if len(password) < 6:
                raise serializers.ValidationError("Sifre en azi 6 simvoldan ibaret olmalidir")

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(
            **validated_data
        )
        user.set_password(password)
        user.activation_code = create_activation_code(size=6, model_=User)
        user.is_active = False
        user.save()

        # send mail
        send_mail(
            'Qeydiyyat tamamla',
            f'Asagidaki koddan istifade ederek qeydiyyati tamamlayin \n Kod: {user.activation_code}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        return user



class VerifySerializer(serializers.ModelSerializer):
    # verificationCode=serializers.CharField()
    # activation_code=serializers.CharField()
 
    class Meta:
        model = User
        fields = ("activation_code",)
        extra_kwargs = {
            "activation_code": {
                "write_only": True
            }
        }

    def validate(self, attrs):
        activation_code = self.instance.activation_code
        code=attrs.get("activation_code")
        if int(code) != int(activation_code):
            raise serializers.ValidationError({"Duzgun kod daxil edilmeyib"})
        return attrs

    def update(self, instance, validated_data):
        instance.activation_code = None
        instance.is_active = True
        instance.save()
        return instance
    
    
    
class SendResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        user = User(
            **attrs
        )
        email = attrs.get("email")

        user.password_reset_code = create_password_reset_code(size=10, model_=User)
        
        
        if email:

            send_mail(
            'Reset Password',
            f'Passwordu yenilemek ucun aktivlesdirme kodu:{user.password_reset_code}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        return attrs


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    password_reset_code = serializers.CharField()
    class Meta:
        model = User
        fields = ("password_reset_code", 'password')

    def validate(self, attrs):
        user = User(
            **attrs
        )
        
        password_reset_code = user.password_reset_code
        code = attrs.get("password_reset_code")
        password = attrs.get('password')
        if int(code) != int(password_reset_code):
            raise serializers.ValidationError({"Duzgun kod daxil edilmeyib"})
        return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        instance.password_reset_code = None
        instance.set_password(password)
        instance.save()
        return instance