from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('stocks/', views.get_stock_list, name='get_stock_list'),
    path('predict/', views.predict_stock, name='predict_stock'),
]
