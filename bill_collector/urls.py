from django.urls import path
from . import views


app_name = 'bill_collector'
urlpatterns = [
    path('', views.render_month_selector, name='select_bill_month'),
    path('selected_month/', views.month_selector_bill_middleware),
    path('selected_month/<int:year>/<int:month>/', views.render_monthly_bill, name='monthly_bill'),
    path('selected_month/<int:year>/<int:month>/add_invoice/', views.add_invoice),
    path('selected_month/<int:year>/<int:month>/delete_invoice/', views.delete_invoice),
    path('selected_month/<int:year>/<int:month>/update_invoice/', views.update_invoice),
]
