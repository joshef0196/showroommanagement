from showroom import views
from django.urls import path

urlpatterns = [
    path('dashboard/', views.index),
    path('admin/', views.login),
    path('logout/', views.logout),
    path('product-category-add/', views.add_product_cat),
    path('category-list/', views.category_list),
    path('edit-category/<int:id>', views.edit_product_cat),
    path('delete-category/<int:id>', views.delete_pro_category),
    path('add-brance/', views.add_branch),
    path('edit/<int:id>', views.edit_branch),
    path('remove/<int:id>/', views.delete_branch),
    path('branch-list/', views.branch_list),
    path('add-product/', views.add_product),
    path('product-list/', views.product_list),
    # .......for branch...........
    path('login/', views.branch_login),
    path('signout/', views.branch_logout),
    path('my-dashboard/', views.branch_dashboard),
    path('customer-registration/', views.customer_reg),
    path('add-sales-product/',views.add_selling_product),
    path('category/product-load/',views.load_category_product),
]
