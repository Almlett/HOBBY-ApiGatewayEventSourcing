"""
Autogenerate viewsets file
"""
from rest_framework import viewsets
from .models import EndPoint, Api 	# pylint: disable=relative-beyond-top-level
from .serializers import EndPointSerializer, ApiSerializer  # pylint: disable=relative-beyond-top-level
from users.serializers import ApiUserSerializer
import requests
import json
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from users.utils import Auth
from .tasks import send_to_rabbitmq


class EndPointViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    EndPoint ViewSet
    """

    queryset = EndPoint.objects.all()
    serializer_class = EndPointSerializer


class ApiViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
    Api to save api paths

    Api Path: local path example /api/users/
    Request Path: remote path example http://server:16000/api/v1/users/
    Plugin: Type of validation
    Origin: Host name of the api
    """

    queryset = Api.objects.all()
    serializer_class = ApiSerializer


class Gateway(APIView):
    authentication_classes = ()

    def check_plugin(self, api, request):
        """Check if plugin is enabled

        Args:
            api (API Model): Instance of API model

        Raises:
            NotImplementedError: Error when plugin is not implemented

        Returns:
            Boolean, Message: Validation result and message
        """

        if api.plugin == 0:
            return True, 'Remote validation'
        elif api.plugin == 1:
            is_valid, user = Auth().valid_token(request.META.get('HTTP_AUTHORIZATION'))
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
                    return True, 'Valid permission'
                return False, 'Invalid permission'
            return False, 'Valid token is needed'
        else:
            raise NotImplementedError("Not plugin implemented")

    def send_request(self, api, request, protocol='http'):
        """Send request to remote server

        Args:
            api (API): Instance of API model

        Returns:
            request.method: Request method
        """
        headers = {}
        if api.plugin != 0 and request.META.get('HTTP_AUTHORIZATION'):
            headers['authorization'] = request.META.get('HTTP_AUTHORIZATION')

        host = api.origin.host
        port = api.origin.port
        path = api.request_path

        url = "{}://{}:{}/{}".format(protocol, host, port, path)
        method = request.method.lower()
        ''' method_map = {
            'get': requests.get,
            'post': requests.post,
            'put': requests.put,
            'patch': requests.patch,
            'delete': requests.delete
        } '''

        for k, v in request.FILES.items():
            request.data.pop(k)

        if request.content_type and request.content_type.lower() == 'application/json':
            data = json.dumps(request.data)
            headers['content-type'] = request.content_type

        else:
            data = request.data
        # It was sent directly to the remote server, now it will be sent to a message stack
        # return method_map[method](url, headers=headers, data=data, files=request.FILES)
        result = {
            'method': method,
            'url': url,
            'headers': headers,
            'data': data,
            'files': request.FILES
        }
        return result

    def api_list(self, request, protocol='http'):
        """Get endpoints list

        Returns:
            dict: Dict with endpoints list
        """
        endpoints = EndPoint.objects.all()
        result = []
        for item in endpoints:
            endpoint = {
                'name': item.name,
                'host': item.host,
                'port': item.port,
                'urls': [],
            }

            urls = Api.objects.filter(origin=item)
            urls_list = {}
            for url in urls:
                urls_list["gateway/api/" + url.api_path] = "{}://{}:{}/{}".format(
                    protocol, endpoint['host'], endpoint['port'], url.request_path)
            endpoint['urls'] = urls_list

            result.append(endpoint)
        return result

    def operation(self, request):
        """URLS Manager, get and redirect urls from gateway/api to rabbitMQ
        """
        path = request.path_info.split('/')
        if len(path) < 3:
            return Response({'detail': 'No URL found'}, status=status.HTTP_400_BAD_REQUEST)
        if path[2] == 'api' and path[3] == '':
            is_valid, user = Auth().valid_token(request.META.get('HTTP_AUTHORIZATION'))
            if is_valid:
                data = self.api_list(request)
                return Response({'result': data}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': "Without Permissions"}, status=status.HTTP_403_FORBIDDEN)

        apimodel = Api.objects.filter(api_path=path[3])
        if apimodel.count() != 1:
            return Response({'detail': 'URL not found'}, status=status.HTTP_400_BAD_REQUEST)

        valid, msg = self.check_plugin(apimodel[0], request)

        if not valid:
            return Response({'detail': msg}, status=status.HTTP_403_FORBIDDEN)

        response = self.send_request(apimodel[0], request)
        send_to_rabbitmq.delay(response)
        return Response({'result': response}, status=status.HTTP_200_OK)
        # try:
        # It was sent directly to the remote server, now it will be sent to a message stack
        # if res.headers.get('Content-Type', '').lower() == 'application/json':
        #    data = res.json()
        # else:
        #    data = res.content
        # return Response({'result': response}, status=status.HTTP_200_OK)
        # except Exception as e:
        #    return Response({'detail': 'Failed to establish connection, destination server unreachable'}, status=status.HTTP_400_BAD_REQUEST)

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
