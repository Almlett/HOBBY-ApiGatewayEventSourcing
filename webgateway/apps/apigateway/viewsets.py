"""
Autogenerate viewsets file
"""
import datetime
from rest_framework import viewsets
from .models import EndPoint, Api 	# pylint: disable=relative-beyond-top-level
from .serializers import EndPointSerializer, ApiSerializer  # pylint: disable=relative-beyond-top-level
from users.serializers import ApiUserSerializer
import requests
import json
import boto3
import os
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from users.utils import Auth
from pymongo import MongoClient
import uuid


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
            return True, 'Remote validation', "External Validation"
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
                    return True, 'Valid permission', user
                return False, 'Invalid permission', None
            return False, 'Valid token is needed', None
        else:
            raise NotImplementedError("Not plugin implemented")

    def send_request(self, api, request, user, protocol='http'):
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
        #payload, timestamp, ID, type, author

        result = {
            'payload': {
                'url': url,
                'headers': headers,
                'data': json.loads(data) if data else None,
                'files': request.FILES
            },
            'timestamp': str(datetime.datetime.now()),
            '_id': str(uuid.uuid4()),
            'type': method,
            'author': user
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

    def get_db_handle(self):
        """Method to create a connection to a database

        Returns:
            db_handle: Database handle
        """
        host = os.environ.get('MONGO_INITDB_HOST')
        port = os.environ.get('MONGO_INITDB_PORT')
        username = os.environ.get('MONGO_INITDB_ROOT_USERNAME')
        password = os.environ.get('MONGO_INITDB_ROOT_PASSWORD')
        db_name = os.environ.get('MONGO_INITDB_NAME')
        try:
            client = MongoClient(host=host,
                                 port=int(port),
                                 username=username,
                                 password=password
                                 )
            db_handle = client[db_name]
            return db_handle, client
        except Exception:
            return None

    def insert_mongo(self, message):
        """Method to insert a message into a database
        """
        db_handle, client = self.get_db_handle()
        try:
            collection_name = db_handle["events_c"]
            print("\n\n\n\n")
            print(message)
            print("\n\n\n\n")
            collection_name.insert_one(message)
            client.close()
            return True
        except Exception:
            return False

    def operation(self, request):
        """URLS Manager, get and redirect urls from gateway/api
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

        valid, msg, user = self.check_plugin(apimodel[0], request)

        if not valid:
            return Response({'detail': msg}, status=status.HTTP_403_FORBIDDEN)

        try:
            message = self.send_request(apimodel[0], request, user)
            insert_mongo = self.insert_mongo(message)
            if not insert_mongo:
                return Response({'detail': 'Failed to establish connection, mongo server unreachable'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # It was sent directly to the remote server, now it will be sent to a message stack
            # if res.headers.get('Content-Type', '').lower() == 'application/json':
            #    data = res.json()
            # else:
            #    data = res.content

            AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", None)
            AWS_SECRET_ACCESS_KEY = os.environ.get(
                "AWS_SECRET_ACCESS_KEY", None)
            AWS_SNS_ARN = os.environ.get("AWS_SNS_ARN", None)

            # Get the service resource

            sns = boto3.client('sns',
                               aws_access_key_id=AWS_ACCESS_KEY_ID,
                               aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                               region_name='us-west-2')

            response = sns.publish(
                TargetArn=AWS_SNS_ARN,
                Message=json.dumps(json.dumps(message))
            )

            return Response({'result': response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'Failed to establish connection, destination server unreachable'}, status=status.HTTP_400_BAD_REQUEST)

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
