from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'CodeAlpha Event Registration System API',
        'endpoints': {
            'events': '/api/events/',
            'event-detail': '/api/events/<id>/',
            'register': '/api/register/',
            'registrations': '/api/registrations/',
            'cancel-registration': '/api/registrations/<id>/',
        },
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', api_root),
]
