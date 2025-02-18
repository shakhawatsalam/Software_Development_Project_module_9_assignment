from django.urls import path
from events.views import dashboard_page, create_event, update_event, delete_event, create_category, deshboard_category, update_category, delete_category, event_details,rsvp_event, CreateEventView, UpdateEventView, DeleteEventView, EventDetailsView, CreateCategoryView, UpdateCategoryView, DeleteCategoryView

urlpatterns = [
    path('dashboard/', dashboard_page, name='dahsboard'),
    path('dashboard-category/', deshboard_category, name='dahsboard-category'),
    # path('create-event/', create_event, name='create-event'),
    # path('update-event/<int:id>/', update_event, name='update-event'),
    # path('delete-event/<int:id>/', delete_event, name='delete-event'),
    # path('event-details/<int:event_id>', event_details, name='event-details'),
    # path('update-category/<int:id>/', update_category, name='update-category'),
    # path('delete-category/<int:id>/', delete_category, name='delete-category'),
    path('create-event/', CreateEventView.as_view(), name='create-event'),
    path('update-event/<int:id>/', UpdateEventView.as_view(), name='update-event'),
    path('delete-event/<int:id>/', DeleteEventView.as_view(), name='delete-event'),
    path('event-details/<int:event_id>', EventDetailsView.as_view(), name='event-details'),
    path('create-category/', CreateCategoryView.as_view(), name='create-category'),
    path('update-category/<int:id>/', UpdateCategoryView.as_view(), name='update-category'),
    path('delete-category/<int:id>/', DeleteCategoryView.as_view(), name='delete-category'),
    path('rsvp-event/<int:event_id>/<int:user_id>/', rsvp_event, name='rsvp-event'),
]