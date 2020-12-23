from django.conf.urls import url
from purchase.views import BarChartAPI

urlpatterns = [
    url(r'^$', BarChartAPI.as_view(), name = 'chart'),
]