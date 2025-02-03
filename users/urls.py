from django.urls import path
from users.views import sign_up, sign_in, sign_out, activate_user

urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'), # Register User
    path('sign-in/', sign_in, name='sign-in'), # Login User
    path('sign-out/', sign_out, name='sign-out'), # Login Out User
    path('activate/<int:user_id>/<str:token>/' , activate_user), # Activate Email By Sending Email
]
