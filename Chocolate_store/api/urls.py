from django.urls import path

# from .views import ListChocos
from . import views
from .views import RegisterView, LoginView

# from api import views
#
#
# router = DefaultRouter()
# router.register("carts/", views.CartView, basename="carts")

urlpatterns = [
    path('home/',views.home,name='home'),
    path('register/',RegisterView.as_view(),name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # path('chocolates/',ListChocos.as_view(),name = 'list')
    path('chocolates/', views.ListChocolate.as_view(), name='list'),
    path('details/<int:pk>/', views.DetailChoco.as_view(), name='details'),
    path('checkout/<int:pk>/', views.ChocoCheckoutView.as_view(), name='checkout'),

]
# +router.urls
