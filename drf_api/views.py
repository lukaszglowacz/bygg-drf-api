from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.generic import TemplateView

@api_view()
def root_route(request):
    return Response({
        "message": "Welcome to my WorkTime App API"
    })
    
class IndexView(TemplateView):
    template_name = 'index.html'