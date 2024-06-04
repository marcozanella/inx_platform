from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("forecast/", views.forecast, name="forecast"),
    path("forecast/<int:customer_id>/", views.forecast, name="forecast-customer"),
    path("forecast/<int:customer_id>/<int:brand_colorgroup_id>/", views.forecast, name="forecast-c-bcg"),

    path("loader/", views.loader, name="loader"),
    path("loading", views.loading, name="loading"),
    path('log_stream_import_files/<int:file_id>/', views.start_file_processing, name='log_stream_import_files'),

    path("import_data/", views.import_data, name='import_data'),
    path("import_single_table/", views.import_single_table, name='import-single-table'),
    
    path("clean_db/", views.clean_db, name='clean_db'),
    path("clean_single/", views.clean_single, name='clean_single'),
    
    path("imported_files/", views.imported_files, name='imported-files'),
    path("imported_file_log/<int:pk>", views.imported_file_log, name='imported-file-log'),
    path("files_to_import/", views.files_to_import, name='files-to-import'),
    path("push_file_to_file_processor", views.push_file_to_file_processor, name="push-file-to-file-processor"),
   

    path('start_processing/<int:file_id>/', views.start_processing, name='start-processing'),
    path('start_file_processing/<int:file_id>', views.start_file_processing, name='start-file-processing'),
    path('delete_this_file_to_import/<int:file_id>/', views.delete_this_file_to_import, name='delete-this-file-to-import'),
    
    path("customers/", views.customers, name="customers"),
    path("customer_view/<int:pk>", views.customer_view, name="customer-view"),
    path("customer_edit/<int:pk>", views.customer_edit, name="customer-edit"),

    path("get_contact_details/<int:id>", views.get_contact_details, name="get-contact-details"),

    path("products/", views.products, name="products"),
    path("products_list/", views.products_list, name="products-list"),
    path("product_view/<int:pk>", views.product_view, name="product-view"),
    path("product_edit/<int:pk>", views.product_edit, name="product-edit"),

    path("brands_list/", views.brands_list, name="brands-list"),
    path("brand_view/<int:pk>", views.brand_view, name="brand-view"),
    path("brand_edit/<int:pk>", views.brand_edit, name="brand-edit"),
    

    # Authentication
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/login-illustration/', views.LoginViewIllustrator.as_view(), name='login_illustration'),
    path('accounts/login-cover/', views.LoginViewCover.as_view(), name='login_cover'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/login-link/', views.login_link, name='login_link'),
    path('accounts/register/', views.RegistrationView.as_view(), name='register'),

    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='change_password'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='app_pages/password-change-done.html'
    ), name="password_change_done" ),

    path('accounts/forgot-password/', views.PasswordReset.as_view(), name='forgot_password'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', 
        views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='pages/password-reset-done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='pages/password-reset-complete.html'
    ), name='password_reset_complete'),

]

