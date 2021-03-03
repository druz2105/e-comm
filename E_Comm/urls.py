"""E_Comm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from E_app import views, seller_view
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings

urlpatterns = [
    path('', views.urlredirect),
    path('admin/', admin.site.urls),
    path('login/', views.user_login),
    path('accounts/login/', views.user_login),
    path('logout/', views.user_logout),
    path('edit_user_profile/', views.edit_profile),
    path('register_user/', views.register),
    path('home/', views.Home, name='home'),
    path('contact_us/', views.post_email, name='post_email'),
    path('contact/', views.Contact),
    path('add_cart/<int:pk>/', views.add_cart, name='add_cart'),
    path('update_cart/<str:pk>/', views.update_cart, name='update_cart'),
    path('short_product_type/<str:pk>/', views.product_short_view, name='product_short_view'),
    path('remove_item_cart/<str:pk>/', views.remove_item_cart, name='remove_item_cart'),
    path('remove-cart/<str:pk>/', views.remove_cart, name='remove_cart'),
    path('view_more/<int:pk>/', views.details_product, name='details_product'),
    path('cart/', views.cart),
    path('checkout/', views.checkout),
    path('payment/<str:pk>/<str:id>/', views.payment, name='payment'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"),
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="link_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset_confirm.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_complete.html"),
         name="password_reset_complete"),
    # _________________________________________SELLER_______________________________________________
    path('register_seller/', seller_view.register_seller, name='register_seller'),
    path('seller_home/', seller_view.seller_home),
    path('register_seller_product/<str:pk>/', seller_view.register_seller_product, name="register_seller_product"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
