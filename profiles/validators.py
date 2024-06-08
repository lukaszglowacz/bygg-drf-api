from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

def validate_image_file_size(value):
    """
    Validates that the image file size does not exceed a specified limit.
    
    Args:
    value (UploadedFile): The image file uploaded by the user.

    Raises:
    ValidationError: If the file size exceeds 2 megabytes.
    """
    max_size = 2 * 1024 * 1024  # Set the maximum file size to 2MB.
    if value.size > max_size:
        # If the file size is greater than the maximum size, raise a ValidationError.
        raise ValidationError(f'Image too large. Max size is {max_size/(1024*1024)}MB.')

def validate_image_dimensions(image):
    """
    Validates that the dimensions of the uploaded image do not exceed a specified width and height.
    
    Args:
    image (ImageFile): The image file uploaded by the user.

    Raises:
    ValidationError: If either dimension of the image exceeds 4096 pixels.
    """
    max_width = max_height = 4096  # Set the maximum width and height to 4096 pixels.
    width, height = get_image_dimensions(image)
    if width > max_width or height > max_height:
        # If either the width or the height exceeds their respective maxima, raise a ValidationError.
        raise ValidationError(f'Image dimensions too large. Max size is {max_width}x{max_height}px.')
