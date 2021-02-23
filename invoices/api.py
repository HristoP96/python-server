from django.http import JsonResponse
from common.models import Invoice
from . import Session, Base, db_engine
from common import CrudAPI
from django.views.decorators.csrf import csrf_exempt
import datetime
from k_means.sklearn import RFM
from sqlalchemy import between
import pandas as pd
from common.models import Customer
class Cache:
    data = []

Base.metadata.create_all(db_engine)
session = Session()

customer_cache_data = Cache()

class InvoicesAPI(CrudAPI):
    cache = {}

    def index(self, request):
        invoices = session.query(Invoice)
        res = []
        for i in invoices:
            res = i.to_json()
            res.append(res)

        return JsonResponse(res, safe=False)

    @csrf_exempt
    def get(self, request, record_id):
        if len(self.cache) > 0 and self.cache['date'] == record_id:
            print("from cache")
            return JsonResponse(self.cache['data'], safe=False)

        invoices = session.query(Invoice).filter(
            Invoice.date.between(record_id, datetime.datetime.now().strftime("%Y-%m-%d")))

        res = []
        rfm_res = []
        for i in invoices:
            rfm_obj = i.to_rfm_json()
            obj = i.to_json()
            rfm_res.append(rfm_obj)
            res.append(obj)
        cluster_data = RFM(rfm_res, res)

        customer_cache_data.data = cluster_data['customer_data']
        self.cache['data'] = cluster_data['cluster_data'].to_json()
        self.cache['date'] = record_id

        return JsonResponse(self.cache['data'], safe=False)

def get_customers(request, cluster_id):
    filtered_data = customer_cache_data.data[customer_cache_data.data["Cluster ID"] == cluster_id]['Customer ID'].values.tolist()
    pd.set_option('display.expand_frame_repr', False)
    invoices = session.query(Invoice).filter(Invoice.customer_id.in_(filtered_data))
    c_data = {}
    r_res = []
    for d in invoices:
        res = d.to_json()
        c_id = res['customer']['id']

        if not c_id in c_data.keys():

            c_data[c_id] = {"ID": c_id}
            c_data[c_id][f"Location"] = res['customer']['location']
            c_data[c_id][f"Email"] = res['customer']['email']
            c_data[c_id][f"FirstName"] = res['customer']['first_name']
            c_data[c_id][f"LastName"] = res['customer']['last_name']
            c_data[c_id]['Invoice'] = []

        c_data[c_id]['Invoice'].append({'Date': res['date'], 'Value': res['value'], 'Product': res['product']['name']})

    for k in c_data.keys():
       r_res.append(c_data[k])

    return JsonResponse(r_res, safe=False)

