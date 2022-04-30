from django.urls import path

from .views import ClientAmountView

urlpatterns = [
    path('/client', ClientAmountView.as_view()),
]