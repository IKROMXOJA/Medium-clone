from pathlib import Path
from fastapi import UploadFile
import uuid

MEDIA_DIR = Path(__file__).resolve().parents[1] / "media"
MEDIA_DIR.mkdir(exist_ok=True)

async def save_upload(file: UploadFile) -> str:
    ext = Path(file.filename).suffix or ".bin"
    name = f"{uuid.uuid4().hex}{ext}"
    path = MEDIA_DIR / name
    with path.open("wb") as f:
        f.write(await file.read())
    return f"/media/{name}"
