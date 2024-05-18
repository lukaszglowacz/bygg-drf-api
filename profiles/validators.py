from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

def validate_image_file_size(value):
    max_size = 2 * 1024 * 1024  # 2MB
    if value.size > max_size:
        raise ValidationError(f'The image file is too large. The maximum size is {max_size/(1024*1024)}MB.')

def validate_image_dimensions(image):
    max_width = max_height = 4096  # maksymalna szerokość i wysokość
    width, height = get_image_dimensions(image)
    if width > max_width or height > max_height:
        raise ValidationError(f'The image dimensions are too large. The maximum dimensions are {max_width}x{max_height}px.')
