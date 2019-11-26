from showroom import views
from django.urls import path

urlpatterns = [
    path('dashboard/', views.index),
    path('admin/', views.login),
    path('logout/', views.logout),
    path('product-category-add/', views.add_product_cat),
    path('category-list/', views.category_list),
    path('add-brance/', views.add_brance),
    path('branch-list/', views.branch_list),
    # .......for branch...........
    path('login/', views.branch_login),
    path('signout/', views.branch_logout),
    path('my-dashboard/', views.branch_dashboard),
]
