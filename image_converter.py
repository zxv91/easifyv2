import os
from PIL import Image

def convert_images(input_path, format_file):
	try:
		base_name=os.path.splitext(input_path)[0]
		with Image.open(input_path) as img:
			if img.mode in ("RGBA", "LA") and format_file.upper() == "JPEG" or format_file.upper() == "JPG":
				img.convert("RGB")

			output_path=f"{base_name}.{format_file.lower()}"
			img.save(output_path, format_file.upper())

	except Exception as e:
		print("Error:", e)