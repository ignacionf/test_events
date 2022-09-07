from django.urls import path, include
from .views import EventView, BookView


urlpatterns = [
    path('', EventView.as_view()),
    path('<int:pk>/', EventView.as_view()),
    path('<int:pk>/book/', BookView.as_view()),
]
