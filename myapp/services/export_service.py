import os
import zipfile
from django.conf import settings
from datetime import datetime


def save_code(code, filename):
    """
    Save generated code to file
    """
    # Create media directory if not exists
    media_root = settings.MEDIA_ROOT
    if not os.path.exists(media_root):
        os.makedirs(media_root)

    # Create timestamp subdirectory
    timestamp = datetime.now().strftime("%Y%m%d")
    save_dir = os.path.join(media_root, 'generated', timestamp)
    os.makedirs(save_dir, exist_ok=True)

    # Save file
    file_path = os.path.join(save_dir, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)

    return file_path


def export_zip(file_path):
    """
    Create zip file with generated code
    """
    # Get directory and filename
    file_dir = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    name_without_ext = os.path.splitext(filename)[0]

    # Create zip file
    zip_path = os.path.join(file_dir, f"{name_without_ext}.zip")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, filename)

    return zip_path