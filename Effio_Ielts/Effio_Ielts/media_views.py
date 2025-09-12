"""
Media file serving utilities for production deployment.
"""
import os
from django.http import HttpResponse, Http404
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_control
import mimetypes


@require_http_methods(["GET", "HEAD"])
@cache_control(max_age=3600)  # Cache for 1 hour
def serve_media(request, path):
    """
    Serve media files in production when DEBUG=False.
    This is a simple solution for small-scale applications.
    For larger applications, consider using a CDN or dedicated media server.
    """
    # Security: Prevent directory traversal
    if '..' in path or path.startswith('/'):
        raise Http404("Invalid path")
    
    # Construct full file path
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    # Check if file exists
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise Http404("Media file not found")
    
    # Security: Ensure file is within MEDIA_ROOT
    if not os.path.abspath(file_path).startswith(os.path.abspath(settings.MEDIA_ROOT)):
        raise Http404("Access denied")
    
    # Determine content type
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = 'application/octet-stream'
    
    # Read and serve file
    try:
        # For HEAD requests, don't read the file content
        if request.method == 'HEAD':
            response = HttpResponse(content_type=content_type)
        else:
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type=content_type)
            
        # Add appropriate headers
        response['Content-Length'] = os.path.getsize(file_path)
        if content_type.startswith('image/'):
            response['Cache-Control'] = 'public, max-age=86400'  # Cache images for 24 hours
            
        return response
        
    except IOError:
        raise Http404("Cannot read media file")