from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User, Payments
from users.permissions import IsUserUser
from users.serializers import UserSerializer, PaymentsSerializer, UserSerializerForOthers
from users.services import create_stripe_product, create_stripe_session, create_stripe_price, check_status_stripe


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        password = serializer.data["password"]
        user = User.objects.get(pk=serializer.data["id"])
        user.set_password(password)
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        try:
            if self.request.user.id == self.get_object().pk:
                return UserSerializer
            return UserSerializerForOthers
        except AssertionError:
            return UserSerializerForOthers



class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUserUser]


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUserUser]


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializerForOthers
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentsViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_lesson', 'paid_course', 'pay_transfer')
    ordering_fields = ['pay_date']

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product = create_stripe_product(payment.paid_course)
        price = create_stripe_price(product=product, amount=payment.pay_sum)
        session_id, session_url = create_stripe_session(price)
        payment.session_id = session_id
        payment.payment_link = session_url
        payment.payment_status = check_status_stripe(payment.session_id)
        payment.save()

    @action(detail=True, methods=['get']) #доступно по адресу .../payments/<int:pk>/status/
    def status(self, request, pk=None):
        payment = self.get_object()
        payment_status = check_status_stripe(payment.session_id)
        return Response({"status": payment_status})
