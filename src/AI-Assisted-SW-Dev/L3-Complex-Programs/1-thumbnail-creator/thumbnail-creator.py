from pathlib import Path
from PIL import Image, ImageOps

def create_thumbnails(
    source_dir: str, 
    output_dir: str = None, 
    size: tuple = (50, 50), 
    square_crop: bool = True
):
    """
    Creates thumbnail versions of all images in a source directory.

    :param source_dir: Directory containing the original images.
    :param output_dir: Directory to save thumbnails. Defaults to a 'thumbnails' subfolder.
    :param size: Target dimensions (width, height).
    :param square_crop: If True, crops the image to fill a square without stretching.
                        If False, fits inside 50x50 while preserving original aspect ratio.
    """
    src_path = Path(source_dir)
    out_path = Path(output_dir) if output_dir else src_path / "thumbnails"
    out_path.mkdir(parents=True, exist_ok=True)

    # Common image file extensions to check
    valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff", ".gif"}

    for file_path in src_path.iterdir():
        # Skip subdirectories (including the output folder) and non-images
        if not file_path.is_file() or file_path.suffix.lower() not in valid_extensions:
            continue

        try:
            with Image.open(file_path) as img:
                # Optional: convert palettes/CMYK to RGB/RGBA for format compatibility
                if img.mode in ("CMYK", "P"):
                    img = img.convert("RGBA" if "transparency" in img.info else "RGB")

                if square_crop:
                    # Crops from the center and scales to exactly 50x50
                    thumb = ImageOps.fit(img, size, Image.Resampling.LANCZOS)
                else:
                    # Preserves aspect ratio, fits *within* 50x50 (e.g., might be 50x33)
                    thumb = img.copy()
                    thumb.thumbnail(size, Image.Resampling.LANCZOS)

                # Save with a prefix into the destination directory
                dest_file = out_path / f"thumb_{file_path.name}"
                
                # If saving as JPEG, ensure RGBA is converted to RGB
                if dest_file.suffix.lower() in (".jpg", ".jpeg") and thumb.mode == "RGBA":
                    thumb = thumb.convert("RGB")

                thumb.save(dest_file)
                print(f"Created: {dest_file.name}")

        except Exception as e:
            print(f"Skipping {file_path.name} (Error: {e})")


if __name__ == "__main__":
    # Replace '.' with your target folder path if running from elsewhere
    create_thumbnails(source_dir="./images")