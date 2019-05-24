from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Member


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'is_staff','is_active','date_joined', 'groups', 'user_permissions', 'last_login', 'is_superuser')


class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Member
        # fields = '__all__'
        exclude = ('id',)
