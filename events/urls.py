from django.urls import path
from events.views import dashboard_page, home_page, create_event, update_event, delete_event, create_category, deshboard_category, update_category, delete_category, create_participant, update_participant,  deshboard_participant,delete_participant

urlpatterns = [
    path('', home_page, name='home'),
    path('dashboard/', dashboard_page, name='dahsboard'),
    path('dashboard-category/', deshboard_category, name='dahsboard-category'),
    path('dashboard-participant/', deshboard_participant, name='dahsboard-participant'),
    path('create-event/', create_event, name='create-event'),
    path('create-category/', create_category, name='create-category'),
    path('create-participant/', create_participant, name='create-participant'),
    path('update-participant/<int:id>/', update_participant, name='update-participant'),
    path('delete-participant/<int:id>/', delete_participant, name='delete-participant'),
    path('update-category/<int:id>/', update_category, name='update-category'),
    path('delete-category/<int:id>/', delete_category, name='delete-category'),
    path('update-event/<int:id>/', update_event, name='update-event'),
    path('delete-event/<int:id>/', delete_event, name='delete-event'),
]