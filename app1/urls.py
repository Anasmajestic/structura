from django.urls import path
from .import views

urlpatterns=[
    path('',views.home,name="home"),
    path('contact/',views.contact,name="contact"),
    path('category/',views.category,name="category"),
    path('product/<str:name>',views.product,name="product"),
    path('product/<str:cname>/<str:pname>',views.product_details,name="product_details"),
    path('add_cart/',views.add_cart,name="addCart"),
    path('cart/',views.cart,name="cart"),
    path('cart_remove/<int:id>',views.cart_remove,name="cart_remove"),
    path('signin/',views.signin,name="signin"),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutPage,name="logoutPage"),
    path('address/',views.address,name="address"),
    path('success/',views.success,name="success"),
    path('order/',views.order,name="order"),
    path('finals/',views.finals,name="finals"),
    path('clear/',views.clear,name="clear"),
]