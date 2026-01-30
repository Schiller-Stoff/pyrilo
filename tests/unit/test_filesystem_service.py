import io
import zipfile

from pyrilo.infrastructure.FileSystemService import FileSystemService


def test_list_subdirectories_filters_files(tmp_path):
    """
    Verifies that list_subdirectories returns ONLY folders, not files.
    """
    service = FileSystemService()

    # Setup: Create 2 folders and 1 file
    (tmp_path / "folder_a").mkdir()
    (tmp_path / "folder_b").mkdir()
    (tmp_path / "random_file.txt").touch()

    # Act
    result = service.list_subdirectories(str(tmp_path))

    # Assert
    assert len(result) == 2
    assert "folder_a" in result
    assert "folder_b" in result
    assert "random_file.txt" not in result


def test_create_zip_structure(tmp_path):
    """
    Verifies that the zip created in memory actually contains the file structure.
    """
    service = FileSystemService()

    # Setup: Create a nested structure
    # root/
    #   - data.txt
    #   - sub/
    #       - config.json
    bag_root = tmp_path / "my_bag"
    bag_root.mkdir()
    (bag_root / "data.txt").write_text("hello world")

    sub_folder = bag_root / "sub"
    sub_folder.mkdir()
    (sub_folder / "config.json").write_text("{}")

    # Act: Create Zip
    zip_bytes = service.create_zip_from_folder(str(bag_root))

    # Assert: We unzip the bytes in memory to verify contents
    assert isinstance(zip_bytes, bytes)

    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        file_list = zf.namelist()

        # Check files exist in the zip with correct relative paths
        # Note: Zip paths are usually forward slashes
        assert "data.txt" in file_list
        # Normalize path separators for cross-platform test safety
        assert any("sub/config.json" in f.replace("\\", "/") for f in file_list)