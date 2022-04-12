"""
Autogenerate viewsets file
"""
from rest_framework import viewsets
from .models import Proyect, Api 	# pylint: disable=relative-beyond-top-level
from .serializers import ProyectSerializer, ApiSerializer # pylint: disable=relative-beyond-top-level
from users.serializers import ApiUserSerializer
import requests
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from users.utils import Auth

class ProyectViewSet(viewsets.ModelViewSet):	# pylint: disable=too-many-ancestors
    """
    Proyect ViewSet
    """

    queryset = Proyect.objects.all()
    serializer_class = ProyectSerializer

class ApiViewSet(viewsets.ModelViewSet):	# pylint: disable=too-many-ancestors
    """
    Api ViewSet
    """

    queryset = Api.objects.all()
    serializer_class = ApiSerializer
    

class Gateway(APIView):
    authentication_classes = ()

    def check_plugin(self, api, request):

        if api.plugin == 0:
            return True, ''
        elif api.plugin == 1:
            is_valid, user  = Auth().valid_token(request.META.get('HTTP_AUTHORIZATION'))
            method = request.method.lower()
            
            if is_valid:
                method_map = {
                    'get': 1,
                    'list': 2,
                    'post': 3,
                    'put': 4,
                    'patch': 5,
                    'delete': 6,
                }
                permission = api.permission_set.get(type=method_map[method])
                user_permissions = user.get_permissions(type='query')
                if permission in user_permissions:
                    return True, 'Permisos validos'
                return False, 'Permisos no validos'
            return False, 'Se necesita un token valido'
        else:
            raise NotImplementedError("plugin %d no implementado" % api.plugin)

    def send_request(self, api, request):
        headers = {}
        if api.plugin != 0 and request.META.get('HTTP_AUTHORIZATION'):
            headers['authorization'] = request.META.get('HTTP_AUTHORIZATION')

        host = api.origin.host
        port = api.origin.port
        path = api.request_path
        
        url = "http://{}:{}/{}".format(host,port,path)
        method = request.method.lower()
        method_map = {
            'get': requests.get,
            'post': requests.post,
            'put': requests.put,
            'patch': requests.patch,
            'delete': requests.delete
        }

        for k,v in request.FILES.items():
            request.data.pop(k)
        
        if request.content_type and request.content_type.lower()=='application/json':
            data = json.dumps(request.data)
            headers['content-type'] = request.content_type
            
        else:
            data = request.data
        '''
        add extra headers loggin
        headers['user-test'] = "a@a.com"
        '''
        return method_map[method](url, headers=headers, data=data, files=request.FILES)

    def api_list(self, request):
        proyects = Proyect.objects.all()
        result = []
        for item in proyects:
            proyect = {
                'name':item.name,
                'host':item.host,
                'port':item.port,
                'urls':[],
            }

            urls = Api.objects.filter(origin=item)
            urls_list = {}
            for url in urls:
                urls_list["gateway/api/" + url.api_path] = "http://{}:{}/{}".format(proyect['host'],proyect['port'],url.request_path)
            proyect['urls'] = urls_list
            
            result.append(proyect)
        return result

    def operation(self, request):
        path = request.path_info.split('/')
        if len(path) < 3:
            return Response({'detail':'No url found'}, status=status.HTTP_400_BAD_REQUEST)


        if path[2] == 'api' and path[3] == '':
            is_valid, user  = Auth().valid_token(request.META.get('HTTP_AUTHORIZATION'))
            if is_valid:
                data = self.api_list(request)
                return Response({'result': data}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': "Sin permisos"}, status=status.HTTP_403_FORBIDDEN)


        apimodel = Api.objects.filter(api_path=path[3])
        if apimodel.count() != 1:
            return Response({'detail':'URL no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

        valid, msg = self.check_plugin(apimodel[0], request)

        if not valid:
            return Response({'detail':msg}, status=status.HTTP_403_FORBIDDEN)

        try:
            res = self.send_request(apimodel[0], request)
            if res.headers.get('Content-Type', '').lower() == 'application/json':
                data = res.json()
            else:
                data = res.content
            
            return Response({'result':data}, status=res.status_code)
        except Exception as e:
            return Response({'detail':'Error al establecer conexión, Servidor destino inaccesible'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        return self.operation(request)

    def post(self, request):
        return self.operation(request)

    def put(self, request):
        return self.operation(request)
    
    def patch(self, request):
        return self.operation(request)
    
    def delete(self, request):
        return self.operation(request)
