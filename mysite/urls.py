# mysite/urls.py-------------------------------------------------------------------------------------
from django.contrib import admin
from django.urls import path
from .views import home_view
from projects.views import *
from products.views import *
from suppliers.views import input_supplier_view, update_supplier_by_keyword_view
from supplier_products.views import input_supplier_product_view, update_supplier_product
from receivings.views import input_receiving_view
from receiving_suppliers.views import input_receiving_supplier_view
from myemails.views import send_email_with_attachment, send_email_form
from django.contrib.auth import views as auth_views
from account.views import registration_view, logout_view, login_view, account_view
from uploadfiles.views import *
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', home),
    path('homepage', home_view,name='homepage'), # home add page for debug
    path('input_project/', input_project_view, name='input_project'),
    path('input_project_initial/', input_project_initial_view, name='input_project_initial'),

    path('input_product/', input_product_view, name='input_product'),
    path('update_product/<str:part_number_formal>/', update_product_by_part_number_view, name='update_product'),
    path('export_products/', export_products_to_excel, name='export_products_to_excel'),
    path('import_products/', import_products_excel, name='import_products_excel'),


    path('input_supplier/', input_supplier_view, name='input_supplier'),
    path('update_supplier/<str:supplier_keyword>/', update_supplier_by_keyword_view, name='update_supplier'),

    path('input_supplier_product/', input_supplier_product_view, name='input_supplier_product'),
    path('update_supplier_product/<str:supplier_keyword>/<str:part_number_formal>/', update_supplier_product, name='update_supplier_product'),
    path('input_receiving/', input_receiving_view, name='input_receiving'),
    path('input_receiving_supplier/', input_receiving_supplier_view, name='input_receiving_supplier'),

    # path('project_list/', project_list, name='project_list'),
    path('input_new_project_by_lot_num/', input_new_project_by_lot_num_view, name='input_new_project_by_lot_num'),

    path('project/', project_list, name='project_list'),
    # path('', project_list, name='home'), # also as home page for debug
    path('ongoing_project_list/', ongoing_project_list, name='ongoing_project_list'),
    path('', ongoing_project_list, name='home'), # as home page for run


    path('project/<int:project_id>/', single_project_view, name='single_project_view'),
    path('project/<int:project_id>/update/', update_project_view, name='update_project'),

    path('delete_project/<str:pk>', delete_project, name='delete_project'),

    path('send_email/', send_email, name='send_email'),
    path('send_custom_email/', send_custom_email, name='send_custom_email'),
    path('send_doc_check_email/', send_doc_check_email_view, name='send_doc_check_email'),

    path('send_mail_web/', send_email_with_attachment, name='send_mail_web'),
    path('send_email_form/', send_email_form, name='send_email_form'),

    path('update_project_view_send_mail/<int:project_id>/', update_project_view_send_mail, name='update_project_view_send_mail'), # doc checking result
    path('update_project_view_send_mail_trf_pac/<int:project_id>/', update_project_view_send_mail_trf_pac, name='update_project_view_send_mail_trf_pac'), # ask TRF to PAC
    path('update_project_view_send_mail_trf_pro/<int:project_id>/', update_project_view_send_mail_trf_pro, name='update_project_view_send_mail_trf_pro'), # ask TRF to PRO
    path('update_project_view_send_mail_trf_nc/<int:project_id>/', update_project_view_send_mail_trf_nc, name='update_project_view_send_mail_trf_nc'), # ask TRF to STKNC
    path('update_project_view_send_mail_ncr_notice/<int:project_id>/', update_project_view_send_mail_ncr_notice, name='update_project_view_send_mail_ncr_notice'), # NCR notice

    path('project/<int:project_id>/ip', update_project_to_ip_pdf_view, name='update_project_to_ip_pdf_view'),
    path('project/<int:project_id>/dhr', update_project_to_dhr_review_annex_1_view, name='update_project_to_dhr_review_annex_1_view'),

    path('upload/', upload, name='upload'),

    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('account/', account_view, name='account'),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)