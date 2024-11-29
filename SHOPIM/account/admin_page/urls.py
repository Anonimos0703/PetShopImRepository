from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),  # Landing page
    path('product-list/', views.product_list, name='product_list'),  # Product list
    path('create-product/', views.create_product, name='create_product'),  # Create product
    path('edit-product/<int:id>/', views.edit_product, name='edit_product'),  # Edit product
    path('delete-product/<int:id>/', views.delete_product, name='delete_product'),  # Delete product
    path('create-inventory/', views.create_inventory, name='create_inventory'),  # Create inventory
    path('add-product-to-inventory/<int:inventory_id>/', views.add_product_to_inventory, name='add_product_to_inventory'),
    path('admin_cart/', views.admin_cart,name='admin_cart'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
