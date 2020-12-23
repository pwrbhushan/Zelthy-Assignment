import json
from datetime import datetime 

from django.views import View
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth

from purchase.models import Purchase, PurchaseStatus

class BarChartAPI(View):
    '''
    API to render a bar chart using purchase model data.
    '''

    def get(self, request):
        # Input paramters
        date = request.GET.get('date', None)

        purchase_data = PurchaseStatus.objects.all()

        if date:
            data = None
            latest_purchase = purchase_data.last()
            latest_status = latest_purchase.status
            if latest_status == 'Dispatched':
                data = purchase_data.filter(created_at=latest_purchase.created_at)
            elif latest_status == 'Delivered':
                dispatched_purchase = purchase_data.filter(purchase=latest_purchase.purchase,
                                                            status='Dispatched')
                if dispatched_purchase.exists():
                    data = purchase_data.filter(created_at=dispatched_purchase.first().created_at)
                else:
                    data = purchase_data.filter(created_at=latest_purchase.created_at)

            purchase_data = data if data else None

        if purchase_data:
            import pdb; pdb.set_trace()
            frequency_by_month = purchase_data.annotate(month=TruncMonth('created_at')).values(
                                    'month').annotate(c=Count('id')).order_by('month')

            for i in frequency_by_month:
                i['month'] = i['month'].strftime('%m-%Y')

            context_dict = {
                'month_year': json.dumps([x['month'] for x in frequency_by_month]),
                'count': json.dumps([x['c'] for x in frequency_by_month])
            }

            return render(request, "charts/base.html", context=context_dict)
        else:
            return render(request, "charts/base.html")