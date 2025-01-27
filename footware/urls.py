"""
URL configuration for shoesproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from website import views
# from admins import views as adminss


urlpatterns = [
    path('',views.login_view),
    path('dashbord/',views.dashbord),
    path('Profile/',views.Profile),
    path('forgot_password/', views.forgot_password_view),
    path('custmore_model/',views.custmore_model),
    path('save_Customer/',views.save_Customer),
    path('custmore_list/',views.custmore_list),
    path('delete_custmore/',views.delete_custmore),
    path('edit_custmore/',views.edit_custmore),
    path('update_file/',views.update_file),

    path('add_brand/',views.add_brand),
    path('save_brand/',views.save_brand),
    path('add_brand_list/',views.add_brand_list),
    path('delete_brand/',views.delete_brand),
    path('edit_brand/',views.edit_brand),
    path('update_brand/',views.update_brand),
    path('available_stock/',views.available_stock),
    path('customer_visits/',views.customer_visits),
    path('add_bill/',views.add_bill),
    path('save_bill/',views.save_bill),
    path('bill_print/<int:customer_id>/', views.bill_print),



    path('Notifaction/',views.Notifaction),
    path('Purchase_list/',views.Purchase_list),
    path('delete_Purchase/',views.delete_Purchase),
    path('purchase_list/', views.Purchase_list),


    path('Profile_info/',views.Profile_info),
    path('save_bill_info/',views.save_bill_info),
    path('edit_Info/',views.edit_Info),
    # path('update_info/',views.update_info),

    path('Return/',views.Return),
    path("process_return/", views.process_return),
    path("total_sum/",views.total_sum),


    path("Calendar/",views.Calendar),
    
    path("Pyment/",views.Pyment),
    path("verify_payment/",views.verify_payment),

]
