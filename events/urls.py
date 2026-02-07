from django.urls import path
from .views import (
    EventListView, EventDetailView, 
    AdminEventCreateView, AdminEventUpdateView, 
    AdminEventDeleteView, AdminEventListView
)

urlpatterns = [
    # Public endpoints
    path('', EventListView.as_view(), name='event-list'),
    path('<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    
    # Admin endpoints
    path('admin/', AdminEventListView.as_view(), name='admin-event-list'),
    path('admin/create/', AdminEventCreateView.as_view(), name='admin-event-create'),
    path('admin/<int:pk>/update/', AdminEventUpdateView.as_view(), name='admin-event-update'),
    path('admin/<int:pk>/delete/', AdminEventDeleteView.as_view(), name='admin-event-delete'),
]