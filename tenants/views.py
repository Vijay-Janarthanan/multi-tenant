from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Organization, Role, Member
from .utils import sendEmail, createTempassword
from rest_framework_simplejwt.tokens import RefreshToken
import time, datetime
from cryptography.fernet import Fernet
from django.conf import settings
from django.db.models import Count

print("settings.SECRET_KEY", type(settings.SECRET_KEY))
fernet = Fernet(settings.SECRET_KEY)

# Create your views here.
@api_view(['POST'])
def signup(request):
    email = request.data.get('email')
    password = request.data.get('password')
    org_name = request.data.get('org_name')
    role_name = request.data.get('role_name')
    role_desc = request.data.get('role_desc')
    time_now = time.time()

    # Encrypt Password
    password_encrypted = fernet.encrypt(password.encode())

    if User.objects.filter(email=email).exists():
        return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(email=email, password=password_encrypted, status =1,created_at=time_now, updated_at=time_now)
    org = Organization.objects.create(name=org_name,created_at=time_now, status=1, updated_at=time_now)
    role = Role.objects.create(org=org, name = role_name,description= role_desc)
    Member.objects.create(user=user, org=org, role=role,created_at=time_now, updated_at=time_now, status=1)

    return Response({
        "stat":"Ok",
        "msg":"User Signed up successfully"
    })


@api_view(['POST'])
def signin(request):
    email = request.data.get('email')
    password = request.data.get('password')
    time_now = time.time()
    if not User.objects.filter(email=email).exists():
        return Response({'error': 'User doesnot exists, Please signup first'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        user = User.objects.filter(email=email).values().first()
        # Decode Password
        password_decrypted = fernet.decrypt(eval(user['password'])).decode()
        if password != password_decrypted:
            return Response({'error': 'Wrong Password, Enter a correct password'}, status=status.HTTP_400_BAD_REQUEST)

    # Generate tokens
    refresh = RefreshToken.for_user(User(user))
    mail_str = f'''<html><head><body><h1>you have successfully logged in to Multi-Tenant</h1>
        <h2>If you think you have not logged in. Kindly Contact us.</h2>
        </body></html>'''
        # Send invite email
    sendEmail(email,mail_str)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })

@api_view(['POST'])
def resetpassword(request):
    email = request.data.get('email')
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    password_encrypted = fernet.encrypt(new_password.encode())

    time_now = time.time()
    if not User.objects.filter(email=email).exists():
        return Response({'error': 'User doesnot exists, Please signup first'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        user = User.objects.filter(email=email).values().first()
        # Decode Password
        password_decrypted = fernet.decrypt(eval(user['password'])).decode()
        if old_password != password_decrypted:
            return Response({'error': 'Old Password is Wrong, Enter a correct password'}, status=status.HTTP_400_BAD_REQUEST)
        User.objects.filter(email=email).update(password=password_encrypted, updated_at=time_now)
        mail_str = f'''<html><head><body><h1>Your Password have been changed</h1>
        <h2>There is a recent update in your Password</h2>
        <h2>If the Password is not changed by you. Kindly revert back as soon as Possible.</h2>
        </body></html>'''
        # Send invite email
        sendEmail(email,mail_str)
        return Response({
        "stat":"Ok",
        "msg":"Password updated Successfully"
    })


@api_view(['POST'])
def inviteMember(request):
    org_id = request.data.get('org_id')
    user_email = request.data.get('email')
    role_id = request.data.get('role_id')
    try:
        time_now = time.time()
        org = Organization.objects.get(id=org_id)
        role = Role.objects.get(id=role_id)
        temp = createTempassword()
        # Check if user exists, otherwise create a new user
        user, created = User.objects.get_or_create(email=user_email, defaults={
            'password': temp,  # Normally, you would set a temporary password or send an invitation link
            'status': 0,
            'profile': {},
            'created_at':time_now,
            'updated_at':time_now
        })
        if not created:
            temp = User.objects.filter(email=user_email).values().first()['password']
        print(user,org)
        # Create a member entry
        Member.objects.create(
            org=org,
            user=user,
            role=role,
            status=0,  # Assuming 0 means 'invited' or 'pending'
            created_at=time_now
        )
        mail_str = f'''<html><head><body><h1>You are invited by {org.name} </h1>
        <h2>Use the Temporary Password given below to signup</h2>
        <h2>Temporary Password = {temp}</h2>
        <h2>Open this Url: http://127.0.0.1:8000/tenants/users/invitesignup</h2>
        </body></html>'''
        # Send invite email
        sendEmail(user_email,mail_str)

        return Response({'message': 'Invitation sent successfully'}, status=status.HTTP_200_OK)
    except Organization.DoesNotExist:
        return Response({'error': 'Organisation not found'}, status=status.HTTP_404_NOT_FOUND)
    except Role.DoesNotExist:
        return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def invitesignup(request):
    email = request.data.get('email')
    old_password = request.data.get('temp_password')
    new_password = request.data.get('new_password')
    password_encrypted = fernet.encrypt(new_password.encode())
    time_now = time.time()
    if not User.objects.filter(email=email).exists():
        return Response({'error': 'User doesnot exists, Please signup first'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        user = User.objects.filter(email=email).values().first()
        # Decode Password
        password_decrypted = user['password']
        if old_password != password_decrypted:
            return Response({'error': 'Old Password is Wrong, Enter a correct password'}, status=status.HTTP_400_BAD_REQUEST)
        User.objects.filter(email=email).update(password=password_encrypted,status=1,updated_at=time_now)
        Member.objects.filter(user_id=user['id']).update(status=1,updated_at=time_now)
        return Response({
        "stat":"Ok",
        "msg":"Password updated Successfully"
    })

@api_view(['POST'])
def deleteMember(request):
    mem_id = request.data.get('mem_id')
    try:
        Member.objects.filter(id=mem_id).delete()
        return Response({
        "stat":"Ok",
        "msg":"Member deleted  Successfully"
        })
    except Exception as e:
        return Response({
        "stat":"Not Ok",
        "msg":f"{e}"
        })
    

@api_view(['POST'])
def updateMember(request):
    mem_id = request.data.get('mem_id')
    role_id =  request.data.get('role_id')
    try:
        time_now = time.time()
        Member.objects.filter(id=mem_id).update(role_id=role_id,updated_at=time_now)
        return Response({
        "stat":"Ok",
        "msg":"Member Role Updated Successfully"
        })
    except Exception as e:
        return Response({
        "stat":"Not Ok",
        "msg":f"{e}"
        })
    

@api_view(["GET"])
def getRolewiseCount(request):
    try:
        # Query to get the role-wise number of users
        role_user_count = Member.objects.values('role__name').order_by('role__name').annotate(user_count=Count('user_id'))
        # Prepare response data
        data = [{'role': role['role__name'], 'user_count': role['user_count']} for role in role_user_count]
        return Response({"stat":"Ok", "Data":data})
    except Exception as e:
        print(e)
        return Response({
        "stat":"Not Ok",
        "msg":f"{e}"
        })
    

@api_view(["GET"])
def getOrgwiseCount(request):
    try:
        # Fetch the organization-wise member count
        org_member_count = Member.objects.values('org__name').annotate(member_count=Count('user')).order_by('org__name')

        # Prepare response data
        data = [{'organization': org['org__name'], 'member_count': org['member_count']} for org in org_member_count]

        return Response({"stat":"Ok", "Data":data})
    except Exception as e:
        print(e)
        return Response({
        "stat":"Not Ok",
        "msg":f"{e}"
        })
    
@api_view(["POST"])
def getOrgwiseRoleWiseCount(request):
    try:
        from_date_epoch = request.data.get('from_date')
        to_date_epoch = request.data.get('to_date')
        status = request.data.get('status')

        # Convert epoch to datetime objects
        from_date = datetime.datetime.fromtimestamp(int(from_date_epoch)) if from_date_epoch else None
        to_date = datetime.datetime.fromtimestamp(int(to_date_epoch)) if to_date_epoch else None
        # Fetch the organization-wise role-wise user count
        # Query to get organization wise, role wise user count with optional filters
        queryset = Member.objects.select_related('org', 'role', 'user').values('org__name', 'role__name')

        # Apply date filters
        if from_date and to_date:
            queryset = queryset.filter(created_at__range=(from_date_epoch, to_date_epoch))
            print(queryset)

        # Apply status filter
        if status is not None:
            queryset = queryset.filter(status=status)

        # Annotate count of users per organization and role
        queryset = queryset.annotate(user_count=Count('user_id')).order_by('org__name', 'role__name')

        # Prepare response data
        data = [
            {
                'organization': entry['org__name'],
                'role': entry['role__name'],
                'user_count': entry['user_count']
            }
            for entry in queryset
        ]
        return Response({"stat":"Ok", "Data":data})
    except Exception as e:
        print(e)
        return Response({
        "stat":"Not Ok",
        "msg":f"{e}"
        })

