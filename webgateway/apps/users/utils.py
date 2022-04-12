"""
Utils
"""
import binascii
import os
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from .models import ApiUser,PasswordToken #pylint: disable=relative-beyond-top-level

class Auth:
    """
    Auth
    """

    def __init__(self):
        """
        Init
        """

    @staticmethod
    def _expires_in(token):
        """
        Time to expire token
        """
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time


    def _is_token_expired(self, token):
        """
        Boolean token is expired
        """
        return self._expires_in(token) < timedelta(seconds = 0)


    def _token_expire_handler(self, token):
        """
        Init
        """
        is_expired = self._is_token_expired(token)
        if is_expired:
            token.delete()
            token = Token.objects.create(user = token.user)
        return is_expired, token


    @staticmethod
    def valid_token(token):
        """
        Valid token
        """
        try:
            result = Token.objects.get(key=token)
            return True, result.user
        except Exception as error: #pylint: disable=unused-variable, broad-except
            return False, None

    @staticmethod
    def valid_email_token(token):
        """
        Emai Token
        """
        try:
            result = PasswordToken.objects.get(key=token)
            return True, ApiUser.objects.get(email=result.user_email)
        except Exception as error: #pylint: disable=unused-variable, broad-except
            return False, None


    def login(self, serializer, email, password):
        """
        login
        """
        if not email or not password:
            message = {'detail': 'Por favor proporcione el correo electrónico y la contraseña'}
            return message, HTTP_400_BAD_REQUEST

        try:
            user = ApiUser.objects.get(email=email)
            # Revisar intengos fallidos
        except Exception as error: #pylint: disable=unused-variable, broad-except
            return {'detail': 'Correo electronico no encontrado'}, HTTP_404_NOT_FOUND

        user = authenticate(username=email, password=password)
        if not user:
            #Intentos fallidos + 1
            return {'detail': 'Credenciales no válidas o cuenta inactiva'}, HTTP_404_NOT_FOUND

        #add last ip login
        token, _ = Token.objects.get_or_create(user=user)
        is_expired, token = self._token_expire_handler(token)
        serializer_data = serializer(user, many=False).data
        return {'result':{'token': token.key}}, HTTP_200_OK


    def logout(self, token): #pylint: disable=no-self-use
        """
        Logout
        """
        try:
            result = Token.objects.get(key=token)
            result.delete()
        except Exception as error: #pylint: disable=unused-variable, broad-except
            return {'detail': 'Sesión no encontrada'}, HTTP_404_NOT_FOUND
        return {'detail':'Cierre de sesión exitoso'}, HTTP_200_OK


    def change_password(self, serializer,  token, new_password):
        """
        Change password
        """
        valid, self.object = self.valid_token(token)
        if serializer.is_valid() and valid:
            if not self.object.check_password(serializer.data.get("old_password")):
                return {"detail": "Contraseña incorrecta"}, HTTP_400_BAD_REQUEST
            # validate new password format
            self.object.set_password(new_password)
            self.object.save()
            return {'detail':'Contraseña actualizada exitosamente'}, HTTP_200_OK
        return {"detail": "Token no válido"}, HTTP_404_NOT_FOUND


    def reset_password(self, serializer, token, new_password):
        """
        Reset Password
        """
        valid, self.object = self.valid_email_token(token)
        if valid and serializer.is_valid():
            # validate new password
            self.object.set_password(new_password)
            self.object.save()
            return {'detail':'Contraseña actualizada exitosamente'}, HTTP_200_OK
        return {"detail": "Token no válido"}, HTTP_404_NOT_FOUND


    def token_password(self, email): #pylint: disable=no-self-use
        """
        Token password
        """
        if email:
            try:
                user = ApiUser.Objects.get(email=email)
            except Exception as error: #pylint: disable=unused-variable, broad-except
                return {"detail": "No hay ningún usuario registrado con ese correo electrónico"}, HTTP_404_NOT_FOUND
            try:
                instance = PasswordToken.objects.get(user_email=user.email)
            except Exception as error: #pylint: disable=unused-variable, broad-except
                instance = PasswordToken()
            instance.user_email = email
            instance.key = binascii.hexlify(os.urandom(20)).decode()
            instance.save()
            #Enviar correo
            return {'detail':'Token enviado con éxito'}, HTTP_200_OK

        return {"detail": "Por favor proporcione un correo electrónico"}, HTTP_400_BAD_REQUEST

    def user_data(self, serializer, token):
        """
        user_data
        """
        if not token:
            message = {'detail': 'Token incorrecto'}
            return message, HTTP_400_BAD_REQUEST

        valid, user = self.valid_token(token)

        if not valid:
            return {'detail': 'Token caducado'}, HTTP_404_NOT_FOUND
        serializer_data = serializer(user, many=False).data
        permission = serializer_data.get('permissions')
        user = "{} {}".format(serializer_data.get('first_name'), serializer_data.get('last_name'))
        department = serializer_data.get('department')
            
        return {'result':{'permissions': permission, 'user':user, 'department':department}}, HTTP_200_OK
