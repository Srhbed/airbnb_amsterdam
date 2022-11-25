from django.urls import path
# from .views import home_view
from . import views

urlpatterns = [
    path('app/',views.home_view, name='app'),
    path('',views.home_page,name='home'),

    ]