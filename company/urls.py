from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('home/', views.home),
    path('connect/',views.redirect),
    path('login/',views.login),
    path('signup/', views.signup),
    path('addProduct/', views.addProduct),
    path('addProductTo/', views.addProductTo),
    path('deleteProduct/', views.deleteProduct),
    path('deleteProd/<int:prod_id>/', views.deleteProd),
    path('updateProduct/', views.updateProduct),
    path('updateProd/<int:prod_id>/', views.updateProd),
    path('saveChanges/<int:prod_id>/', views.saveChanges),
    path('viewProduct/', views.viewProduct),
    path('addCategory/', views.addCategory),
    path('submitCategory/', views.submitCategory),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
