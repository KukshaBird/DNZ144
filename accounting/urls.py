from django.urls import path, include
from . import views

app_name = 'accounting'

urlpatterns = [
	path('kassas/', views.KassaListView.as_view(), name='kassas_list'),
	path('closed_kassas/', views.KassaClosedListView.as_view(), name='kassas_closed_list'),
	path('charity_kassas/', views.KassaCharityListView.as_view(), name='kassas_charity_list'),
	path('kassas/details/<pk>', views.KassaDetailView.as_view(), name='kassas_details'),
	path('kassas/admin', views.create_operation, name='create_operation'),
	path('kassas/operation_submit', views.operation_submit, name='operation_submit'),
	path('kassas/transfer_submit', views.transfer_submit, name='transfer_submit'),
	path('kassas/withdraw_submit', views.withdraw_submit, name='withdraw_submit'),
	path('kassas/withdraw', views.create_withdraw, name='create_withdraw'),
	path('kassas/transfer', views.create_transfer, name='create_transfer'),
	path('kassas/update_tables', views.refresh_table, name='refresh_table'),
]
