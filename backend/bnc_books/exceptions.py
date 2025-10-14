from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        error_data = {
            'error': str(exc),
            'code': getattr(exc, 'code', 'ERROR'),
            'details': {},
            'timestamp': timezone.now().isoformat()
        }
        
        # Handle validation errors more safely
        if hasattr(exc, 'detail'):
            detail = exc.detail
            if isinstance(detail, dict):
                error_data['details'] = detail
            elif isinstance(detail, list):
                error_data['details'] = {'non_field_errors': detail}
            else:
                error_data['details'] = {'non_field_errors': [str(detail)]}
        
        response.data = error_data
    
    return response