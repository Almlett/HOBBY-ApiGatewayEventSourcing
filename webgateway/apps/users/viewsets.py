"""
Autogenerate viewsets file
"""
import json
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ApiUser, UserProfile, UserPermission, Turn, Department, UserDepartment 	# pylint: disable=relative-beyond-top-level
from .serializers import ApiUserSerializer, ChangePasswordSerializer, UserProfileSerializer # pylint: disable=relative-beyond-top-level
from .serializers import UserPermissionSerializer, UserLoginSerializer, UserLogoutSerializer  # pylint: disable=relative-beyond-top-level
from .serializers import ResetPasswordSerializer, PasswordTokenSerializer # pylint: disable=relative-beyond-top-level
from .serializers import UserDataSerializer # pylint: disable=relative-beyond-top-level
from .serializers import DepartmentSerializer, TurnSerializer, UserDepartmentSerializer 
from .utils import Auth # pylint: disable=relative-beyond-top-level


class AuthViewSet(viewsets.GenericViewSet):	# pylint: disable=too-many-ancestors
    """
    Auth
    """

    permission_classes = [AllowAny, ]
    queryset = ApiUser.objects.all()


    def get_serializer_class(self):
        serializer_classes = {
            '/gateway/users/auth/login/': UserLoginSerializer,
            '/gateway/users/auth/logout/': UserLogoutSerializer,
            '/gateway/users/auth/changepass/': ChangePasswordSerializer,
            '/gateway/users/auth/resetpass/': ResetPasswordSerializer,
            '/gateway/users/auth/passtoken/': PasswordTokenSerializer,
            '/gateway/users/auth/userdata/': UserDataSerializer,
        }
        
        return serializer_classes[self.request.path]


    @action(methods=['POST', ], detail=False)
    def login(self, request):   #pylint: disable=no-self-use
        """
        login
        """
        
        email = request.data.get("email")
        password = request.data.get("password")
        result, status = Auth().login(ApiUserSerializer, email, password)
        return Response(result,status)


    @action(methods=['POST', ], detail=False)
    def logout(self, request):  #pylint: disable=no-self-use
        """
        logout
        """
        token = request.data.get("token")
        result, status = Auth().logout(token)
        return Response(result,status)


    @action(methods=['POST', ], detail=False)
    def changepass(self, request):
        """
        change password
        """
        serializer = self.get_serializer(data=request.data)
        token = request.data['token']
        new_password = request.data['new_password']
        result, status = Auth().change_password(serializer, token, new_password)
        return Response(result,status)


    @action(methods=['POST', ], detail=False)
    def resetpass(self, request):
        """
        reset password
        """
        serializer = self.get_serializer(data=request.data)
        token = request.data['token']
        new_password = request.data['new_password']
        result, status = Auth().reset_password(serializer, token, new_password)
        return Response(result,status)


    @action(methods=['POST', ], detail=False)
    def passtoken(self, request):  #pylint: disable=no-self-use
        """
        password token
        """
        email = request.data['user_email']
        result, status = Auth().token_password(email)
        return Response(result,status)

    @action(methods=['POST', ], detail=False)
    def userdata(self, request):   #pylint: disable=no-self-use
        """
        userdata
        """
        serializer = self.get_serializer(data=request.data)
        token = request.data['token']
        result, status = Auth().user_data(ApiUserSerializer,token)
        return Response(result,status)


class ApiUserViewSet(viewsets.ModelViewSet):	# pylint: disable=too-many-ancestors
    """
    ApiUser ViewSet
    """
    queryset = ApiUser.objects.all()
    serializer_class = ApiUserSerializer

class UserProfileViewSet(viewsets.ModelViewSet):	# pylint: disable=too-many-ancestors
    """
    UserProfile ViewSet
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserPermissionViewSet(viewsets.ModelViewSet):	# pylint: disable=too-many-ancestors
    """
    UserPermission ViewSet
    """

    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer


class TurnViewSet(viewsets.ModelViewSet):	# pylint: disable=too-many-ancestors
    """
    Turn ViewSet
    """

    queryset = Turn.objects.all()
    serializer_class = TurnSerializer


class DepartmentViewSet(viewsets.ModelViewSet):	# pylint: disable=too-many-ancestors
    """
    Department ViewSet
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class UserDepartmentViewSet(viewsets.ModelViewSet):	# pylint: disable=too-many-ancestors
    """
    UserDepartment ViewSet
    """

    queryset = UserDepartment.objects.all()
    serializer_class = UserDepartmentSerializer
