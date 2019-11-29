from showroom import views
from django.urls import path

urlpatterns = [
    path('dashboard/', views.index),
    path('admin/', views.login),
    path('logout/', views.logout),
   
    # .......for branch...........
    path('', views.branch_login),
    path('login/', views.branch_login),
    path('signout/', views.branch_logout),
    path('my-dashboard/', views.branch_dashboard),
    path('customer-registration/', views.customer_reg),
    path('customer-list/', views.customer_list),
    path('cash-sales-product/',views.cash_selling_product),
    path('installment-sales-product/',views.installment_selling_product),
    path('sold-product-list/',views.sold_product_list),
    path('customer-product-list/',views.customer_product_list),
    path('installment-collection/',views.installment_collection),
    path('<int:id>/installment-details/',views.installment_details),
    path('category/product-load/',views.load_category_product),
    path('product-load/',views.load_product),
     path('add-category/', views.add_product_cat),
    path('category-list/', views.category_list),
    path('edit-category/<int:id>', views.edit_product_cat),
    path('delete-category/<int:id>', views.delete_pro_category),
    path('add-brance/', views.add_branch),
    path('edit/<int:id>', views.edit_branch),
    path('remove/<int:id>/', views.delete_branch),
    path('branch-list/', views.branch_list),
    path('add-product/', views.add_product),
    path('product-list/', views.product_list),
    path('change-password/', views.change_password),
    # ................Report.......................

    # ....For branch........
    path('daily-reports/', views.admin_daily_report),
    path('monthly-reports/', views.admin_monthly_report),
    path('yearly-reports/', views.admin_yearly_report),
    path('daily-report/', views.daily_report),
    path('monthly-report/', views.monthly_report),
    path('yearly-report/', views.yearly_report),
]
