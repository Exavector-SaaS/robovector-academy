from django.urls import path
from .views import RegisterView

urlpatterns = [
    # API endpoint for user registration
    path("register/", RegisterView.as_view(), name="register"),
]
