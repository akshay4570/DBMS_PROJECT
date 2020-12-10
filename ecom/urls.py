from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('login/',views.login),
    path('signup/', views.signup),
    path('connect/', views.redirect),
    path('home/', views.home),
    path('about/',views.about),
    path('contact/',views.contact),
    path('sendmail/', views.sendMail),
    path('thanks/',views.thanks),
    path('profile/',views.profile, name='profile'),
    path('account/', views.account),
    path('settings/', views.setting),
    path('changes/', views.changes),
    path('edit/', views.edit),
    path('browse/',views.browse),
    path("products/<int:myid>/", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    path("search/", views.search),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
