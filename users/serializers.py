from rest_framework import serializers

from users.models import User, Payments


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentsSerializer(source="payments_set", many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'avatar', 'phone', 'city', 'last_login', 'payments']


class UserSerializerForOthers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'avatar', 'last_login', 'phone', 'city']


