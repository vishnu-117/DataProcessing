import pandas as pd
from pathlib import Path
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
import os

BASE_DIR = Path(__file__).resolve().parent.parent
today = datetime.datetime.now()


class GetProductData(APIView):

    def get(self, request, transaction_id):
        print(os.path.join(BASE_DIR, 'static'))
        csv_file_path = os.path.join(BASE_DIR, 'static')

        data = pd.read_csv(csv_file_path+'/Transaction_20180101101010.csv')
        product_ref_data = pd.read_csv(csv_file_path+'/ProductReference.csv')
        merged_csv = pd.merge(data, product_ref_data, left_on='productId', right_on='productId', how='left')
        result = merged_csv[merged_csv['transactionId']==int(transaction_id)]
        result.drop(columns=['productId','productManufacturingCity'], axis=1, inplace=True)
        return Response(result.to_json(orient='records', lines=True))


class GetTransactionSummaryByProducts(APIView):

    def get(self, request, last_n_days):
        final_result = []
        csv_file_path = os.path.join(BASE_DIR, 'static')

        d = datetime.timedelta(days = int(last_n_days))
        before_n_day_date = today - d

        data = pd.read_csv(csv_file_path+'/Transaction_20180101101010.csv')
        product_ref_data = pd.read_csv(csv_file_path+'/ProductReference.csv')
        merged_csv = pd.merge(data, product_ref_data, left_on='productId', right_on='productId', how='left')
        merged_csv['transactionDatetime']=pd.to_datetime(merged_csv["transactionDatetime"], dayfirst=True)
        merged_csv = merged_csv[merged_csv['transactionDatetime']>before_n_day_date]
        print(merged_csv)
        final_output = merged_csv.groupby('productName', as_index=True).agg({"transactionAmount": "sum"})
        for i, j in final_output.items():
            for key, value in j.items():
                final_result.append({"productName":key, "totalAmount":value})
        print(final_result)
        return Response(final_result)


class GetTransactionSummaryByManufacturingCity(APIView):

    def get(self, request, last_n_days):
        final_result = []
        csv_file_path = os.path.join(BASE_DIR, 'static')

        d = datetime.timedelta(days = int(last_n_days))
        before_n_day_date = today - d

        data = pd.read_csv(csv_file_path+'/Transaction_20180101101010.csv')
        product_ref_data = pd.read_csv(csv_file_path+'/ProductReference.csv')
        merged_csv = pd.merge(data, product_ref_data, left_on='productId', right_on='productId', how='left')
        merged_csv['transactionDatetime']=pd.to_datetime(merged_csv["transactionDatetime"], dayfirst=True)
        merged_csv = merged_csv[merged_csv['transactionDatetime']>before_n_day_date]
        print(merged_csv)
        final_output = merged_csv.groupby('productManufacturingCity', as_index=True).agg({"transactionAmount": "sum"})
        for i, j in final_output.items():
            for key, value in j.items():
                final_result.append({"cityName":key, "totalAmount":value})
        return Response(final_result)
