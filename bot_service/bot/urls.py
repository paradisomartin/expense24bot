from django.urls import path
from .views import ProcessMessageView

urlpatterns = [
    path('process_message/', ProcessMessageView.as_view(), name='process_message'),
]