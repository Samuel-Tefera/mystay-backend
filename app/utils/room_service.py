from pathlib import Path
import uuid
import shutil
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = Path('app/uploads/rooms')
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/webp'}

def save_room_image(image: UploadFile) -> str:
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail='Invalid image format'
        )

    image.file.seek(0, 2)
    size = image.file.tell()
    image.file.seek(0)

    if size > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=400,
            detail='Image must be <= 5MB'
        )

    ext = image.filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    file_path = UPLOAD_DIR / filename

    with file_path.open('wb') as buffer:
        shutil.copyfileobj(image.file, buffer)

    return f'/uploads/rooms/{filename}'
