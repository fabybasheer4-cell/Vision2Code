"""
URL configuration for visiontocode project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login_get/', views.login_get),
    path('login_post/', views.login_post),
    path('landing_index/', views.landing_index),

    path('change_password_get/', views.change_password_get),
    path('change_password_post/', views.change_password_post),

    path('and_forget_password/', views.and_forget_password),
    path('and_forget_password_post/', views.and_forget_password_post),

    path('logout_get/', views.logout_get),

    ###ADMIN
    path('admin_home_get/', views.admin_home_get),
    path('home_new_index/', views.home_new_index),

    path('admin_view_customer_get/',views.admin_view_customer_get),
    path('admin_view_customer_post/',views.admin_view_customer_post),

    path('admin_view_review_get/',views.admin_view_review_get),
    path('admin_view_review_post/',views.admin_view_review_post),

    path('admin_view_history_get/',views.admin_view_history_get),
    path('admin_view_history_post/',views.admin_view_history_post),


    #####3 Android

    path('android_login_post/',views.android_login_post),
    path('android_forget_password_post/',views.android_forget_password_post),
    path('parent_changepassword_post/',views.user_changepassword_post),

    path('android_user_register/',views.android_user_register),
    path('android_user_view_profile_post/',views.android_user_view_profile_post),
    path('android_user_edit_profile_get/',views.android_user_edit_profile_get),
    path('android_user_edit_profile/',views.android_user_edit_profile),
    path('android_upload_image/',views.android_upload_image),
    path('android_user_send_feedback/',views.android_user_send_feedback),
    path('android_user_view_history_post/',views.android_user_view_history_post),
    path('android_upload_image/',views.android_upload_image),
    # path('/',views.),

]
