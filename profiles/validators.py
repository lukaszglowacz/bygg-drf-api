from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

def validate_image_file_size(value):
    max_size = 2 * 1024 * 1024  # 2MB
    if value.size > max_size:
        raise ValidationError(f'Plik graficzny jest za duży. Maksymalny rozmiar to {max_size/(1024*1024)}MB.')

def validate_image_dimensions(image):
    max_width = max_height = 4096  # maksymalna szerokość i wysokość
    width, height = get_image_dimensions(image)
    if width > max_width or height > max_height:
        raise ValidationError(f'Wymiary obrazu są za duże. Maksymalne wymiary to {max_width}x{max_height}px.')
