from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from accounts.models import SchoolUser
from accounts.api.serializers import RegistrationSerializer, UserSerializer

from school.models import Guardian

# Register
# Url: https://<your-domain>/api/account/register
@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):
    if request.method == 'POST':
        data = {}
        email = request.data.get('email', '0').lower()
        if validate_email(email) is not None:
            data['error_message'] = 'That email is already in use.'
            data['response'] = 'Error'
            return Response(data)

        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['email'] = account.email
            # data['first_name'] = account.first_name
            # data['last_name'] = account.last_name
            data['pk'] = account.pk
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


#TODO add password validation method to only allow stong passwords

def validate_email(email):
    account = None
    try:
        account = SchoolUser.objects.get(email=email)
    except SchoolUser.DoesNotExist:
        return None
    if account is not None:
        return email


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            # 'user_id': int(user.pk),
            # 'email': user.email,
            'is_staff': user.is_staff,
        })

@api_view(['GET'])
def current_user(request):
    user = request.user
    if user.is_staff:
        return Response({
        'user_id': user.id,
        'first_name': 'Staff First Name',
        'last_name': 'Last Name',
        'email': user.email,
        'is_staff': user.is_staff,
        })
    if not user.is_staff:
        guardian = Guardian.objects.get(user= user)
        return Response({
            'user_id': user.id,
            'first_name': guardian.first_name,
            'last_name': guardian.last_name,
            'email': user.email,
            'is_staff': user.is_staff,
    })