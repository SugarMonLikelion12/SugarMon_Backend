from django.urls import include, path
from .views import *

urlpatterns = [
    path('items/', ChecklistListCreateView.as_view(), name='checklist-list-create'),
    path('items/<int:pk>/', ChecklistDetailView.as_view(), name='checklist-detail'),
    path('daily/', DailyChecklistView.as_view(), name='daily-checklist'),
    path('getContinuousDay/', countContinuousChecklist.as_view())
]

