from django.urls import path
from users.views import sign_up, sign_in, sign_out, activate_user, admin_dashboard, admin_view_userlist, assign_role, create_group,delete_group, group_list, admin_view_participantlist, delete_participants, update_participants, dashboard, organizer_dashboard, categories_list, participants_dashboard

urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'), # Register User
    path('sign-in/', sign_in, name='sign-in'), # Login User
    path('sign-out/', sign_out, name='sign-out'), # Login Out User
    path('activate/<int:user_id>/<str:token>/' , activate_user), # Activate Email By Sending Email
    # ADMIN ROUTES
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/dashboard/user-list/', admin_view_userlist, name='admin-view-userlist'),
    path('admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('admin/dashboard/create-group/', create_group, name='create-group'),
    path('admin/dashboard/group-list/', group_list, name='group-list'),
    path('admin/dashboard/group-list/<int:group_id>/', delete_group, name='delete-group'),
    path('admin/dashboard/participant-list/', admin_view_participantlist, name='participant-list'),
    path('admin/dashboard/delete-participant/<int:user_id>/', delete_participants, name='delete-participant'),
    path('admin/dashboard/update-user/<int:user_id>/', update_participants, name='update-user'),
    # ORGANIZER DESHBOARD
    path('organizer/dashboard/', organizer_dashboard, name='organizer-dashboard'),
    path('organizer/dashboard/categories-list', categories_list, name='categories-list'),
    # ORGANIZER DESHBOARD
    path('participants/dashboard/', participants_dashboard, name='participants-dashboard'),
    # path('organizer/dashboard/categories-list', categories_list, name='categories-list'),
    #COMMON ROUTE
    path('dashboard/', dashboard, name='dashboard')
]

