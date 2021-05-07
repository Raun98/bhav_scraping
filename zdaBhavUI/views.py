from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .logic import Logic
from zda.settings import ZIP_FILE
from django.views.static import serve
import os, redis


def download(request):
    bhav_obj = Logic()
    bhav_data = bhav_obj.create_file_name()
    path_to_zip = ZIP_FILE + bhav_data
    if os.path.exists(path_to_zip):
        return serve(request, os.path.basename(path_to_zip), os.path.dirname(path_to_zip))

class Search(APIView):
    def get(self,request, format='None'):
        search = request.query_params.get('name')
        client = redis.Redis(host="127.0.0.1", port=6379, db=0)
        result = list()
        #print(type(search))
        if search is not None:
            for key in client.keys():
                #print(search," ",key)
                if search.strip().lower() == key.decode('UTF-8').strip().lower():
                    d={}
                    d['code'] = client.hget(key, 'code')
                    d['name'] = client.hget(key, 'name')
                    d['open'] = client.hget(key, 'open')
                    d['high'] = client.hget(key, 'high')
                    d['low'] = client.hget(key, 'low')
                    d['close'] = client.hget(key, 'close')
                    result.append(d)
                    print(str(search), " ", client.hget(key, 'code'))
                    break
        else:
            #print(client.keys())
            i=0

            for key in client.keys():
                try:
                    d = {}
                    if i < 15:
                        d['code'] = client.hget(key, 'code')
                        d['name'] = client.hget(key, 'name')
                        d['open'] = client.hget(key, 'open')
                        d['high'] = client.hget(key, 'high')
                        d['low'] = client.hget(key, 'low')
                        d['close'] = client.hget(key, 'close')
                        i += 1
                        result.append(d)
                except Exception as e:
                    pass
        #print(result)
        return Response(result)




