from django.urls import path, re_path
from .views import GetProductData, GetTransactionSummaryByProducts, GetTransactionSummaryByManufacturingCity

urlpatterns = [
    re_path(r'^GetProductData/(?P<transaction_id>[0-9]+)/$', GetProductData.as_view()),
    re_path(r'^transactionSummaryByProducts/(?P<last_n_days>[0-9]+)/$', GetTransactionSummaryByProducts.as_view()),
    re_path(r'^transactionSummaryByManufacturingCity/(?P<last_n_days>[0-9]+)/$', GetTransactionSummaryByManufacturingCity.as_view()),
]
