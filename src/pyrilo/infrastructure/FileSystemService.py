import os
import io
import zipfile
import logging
from typing import List


class FileSystemService:
    """
    Encapsulates file system operations to isolate side effects (IO) from business logic.
    """

    @staticmethod
    def list_subdirectories(path: str) -> List[str]:
        """
        Returns a list of subdirectory names in the given path.
        """
        if not os.path.exists(path):
            logging.warning(f"Path does not exist: {path}")
            return []

        return [
            name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name))
        ]

    @staticmethod
    def create_zip_from_folder(folder_path: str) -> bytes:
        """
        Zips the contents of a folder into an in-memory bytes object.
        - Uses io.BytesIO instead of tempfile, avoiding disk IO entirely.
        - Fixes the Windows 'PermissionError' caused by reading a file while it is still open.
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        # In-memory buffer
        mem_zip = io.BytesIO()

        with zipfile.ZipFile(mem_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Calculate relative path for the zip archive to preserve structure
                    archive_name = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, archive_name)

        # Reset pointer to beginning of the stream so it can be read
        mem_zip.seek(0)
        return mem_zip.read()