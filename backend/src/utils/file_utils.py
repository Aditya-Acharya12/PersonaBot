import os
import uuid
from typing import List
from fastapi import UploadFile

UPLOAD_BASE_DIR = "uploads"


def save_uploads_to_disk(
    files: List[UploadFile],
    persona_id: str,
) -> List[str]:
    """
    Saves uploaded files to disk and returns their file paths.
    """

    persona_dir = os.path.join(UPLOAD_BASE_DIR, persona_id)
    os.makedirs(persona_dir, exist_ok=True)

    saved_paths = []

    for file in files:
        ext = os.path.splitext(file.filename)[1]
        unique_name = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(persona_dir, unique_name)

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        saved_paths.append(file_path)

    return saved_paths
