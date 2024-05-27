from django.urls import path

from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import PaymentsViewSet, UserListView, UserCreateView, UserDetailView, UserUpdateView, UserDeleteView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'payments', PaymentsViewSet, basename='payments')

urlpatterns = [
                  path('user/', UserListView.as_view(), name='user_list'),
                  path('user/create/', UserCreateView.as_view(), name='user_create'),
                  path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
                  path('user/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
                  path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
                  path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ] + router.urls
