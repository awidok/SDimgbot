from io import BytesIO

def image_to_bytes(image):
    bio = BytesIO()
    bio.name = 'image.png'
    image.save(bio, 'png')
    bio.seek(0)
    return bio