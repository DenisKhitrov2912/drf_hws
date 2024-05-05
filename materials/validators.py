from rest_framework.exceptions import ValidationError

key = "youtube.com"
key_mobile = "youtu.be"


def validate_youtube_url(value):
    if key not in value.lower() and key_mobile not in value.lower():
        raise ValidationError("Incorrect YouTube URL")
