from PIL import Image
import os

def batch_resize(folder_input, folder_output, width, height):
	for filename in os.listdir(folder_input):
		if filename.endswith(('.png', '.jpg', '.jpeg')):
			img=Image.open(os.path.join(folder_input, filename))
			img=img.resize((width, height))
			img.save(os.path.join(folder_output, f"resized_{filename}"))