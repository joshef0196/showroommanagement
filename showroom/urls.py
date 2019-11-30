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
    path('add-area/', views.add_area),
    path('area-list/', views.area_list),
    path('edit-area/<int:id>/', views.edit_area),
    path('customer-registration/', views.customer_reg),
    path('edit-customer/<int:id>/', views.edit_customer),
    path('customer-list/', views.customer_list),
    path('profile/<int:id>', views.customer_details),
    path('cash-sales-product/',views.cash_selling_product),
    path('installment-sales-product/',views.installment_selling_product),
    path('sold-product-list/',views.sold_product_list),
    path('customer-product-list/',views.customer_product_list),
    path('installment-collection/',views.installment_collection),
    path('installment-list/',views.installment_list),
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
    path('details/<int:id>/', views.product_details),
    path('unpaid-list/', views.unpaid_list),
    path('dateover-due-list/', views.dateover_due_list),
    # ................Report.......................

    # ....For Admin........
    path('daily-reports/', views.admin_daily_report),
    path('monthly-reports/', views.admin_monthly_report),
    path('yearly-reports/', views.admin_yearly_report),

    # ....For branch........
    path('daily-report/', views.daily_report),
    path('monthly-report/', views.monthly_report),
    path('yearly-report/', views.yearly_report),
    path('date-wise-report/', views.date_to_date_report),
    path('unpaid-report/', views.unpaid_report),
    path('dateover-due-report/', views.dateover_due_report),
]
