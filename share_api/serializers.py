from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User

class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    firstName = serializers.CharField(max_length=100)
    lastName = serializers.CharField(max_length=100)

    city = serializers.CharField(max_length=100)
    street = serializers.CharField(max_length=100)
    contact = serializers.CharField(max_length=100)

    # created_at = serializers.DateField(allow_null=True)

    def create_save(self, validated_data):

        firstName =validated_data.pop('firstName')
        lastName = validated_data.pop('lastName')
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')

        print("Printing validated data")
        print(validated_data)

        user = User.objects.create(username=username, email = email, first_name=firstName, last_name=lastName)
        user.set_password(raw_password=password)
        user.save()

        profile = Profile.objects.create(user = user, **validated_data)
        profile.save()
        print("Profile saved")

class ProfileSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'first_name', 'last_name', 'email')
