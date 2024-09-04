from django.urls import path
from .views import signup, signin, resetpassword, inviteMember, invitesignup, deleteMember, updateMember, getRolewiseCount, getOrgwiseCount, getOrgwiseRoleWiseCount


urlpatterns = [
    path('users/signup/', signup, name='signup'),
    path('users/signin/', signin, name='signin'),
    path('users/resetpass/', resetpassword, name='resetpassword'),
    path('users/invitemember/', inviteMember, name='inviteMember'),
    path('users/invitesignup/', invitesignup, name='invitesignup'),
    path('users/deletemember/', deleteMember, name='deleteMember'),
    path('users/updatemember/', updateMember, name='updateMember'),
    path('users/rolewisedata/', getRolewiseCount, name='getRolewiseCount'),
    path('users/orgwisedata/', getOrgwiseCount, name='getOrgwiseCount'),
    path('users/orgwiserolewisedata/', getOrgwiseRoleWiseCount, name='getOrgwiseRoleWiseCount'),


]