
from django.urls import path
from .views import ProcessImageView , index

urlpatterns = [
   path( 'api' ,index , name='index' ),
   path('api/process-image/', ProcessImageView.as_view(), name='process_image'),
]
