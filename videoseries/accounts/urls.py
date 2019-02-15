from django.urls import path
from .views import loginView, registerView,loginView

app_name = "accounts"

urlpatterns = [
    path('login/', loginView, name='login'),
    path('register/', registerView, name='register'),
    path('logout/', loginView, name='logout'),
]
