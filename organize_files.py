import os
import shutil

def organize_folder(folder):
	categories = {
		"multimedia": {
			"images" : [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
			"videos" : [".mp4", ".avi", ".mkv",  ".mov", ".flv", ".webm"],
			"audio"  : [".mp3", ".wav", ".ogg",  ".flac"]
		},
		"modeling": {
			"blender" : [".blend"],
			"maya"    : [".ma", ".mb"],
			"zbrush"  : [".zbr", ".ztl"],
			"fbx"     : [".fbx"],
			"obj"     : [".obj"]
		},
		"documents": {
			"textos"   : [".pdf", ".docx", ".doc", ".txt",  ".pptx", ".ppt"],
			"datasets" : [".csv", ".json", ".xml", ".xlsx", ".xls",  ".sav", ".arff"]
		},
		"executables": {
			"executables" : [".exe"],
			"scripts"     : [".py", ".cs", ".cpp", ".java", ".js", ".html", ".css", ".sql", ".bat", ".sh"]
		},
		"compressed": {
			"compressed" : [".zip", ".rar", ".7z"],
			"archives"   : [".tar", ".tar.gz", ".tar.bz2"]
		}
	}

	for filename in os.listdir(folder):
		file_path = os.path.join(folder, filename)
		if os.path.isfile(file_path):
			extension = os.path.splitext(filename)[1].lower()
			for category, subcategories in categories.items():
				for subcategory, extensions in subcategories.items():
					if extension in extensions:
						category_folder = os.path.join(folder, category)
						subcategory_folder = os.path.join(category_folder, subcategory)
						os.makedirs(subcategory_folder, exist_ok=True)
						shutil.move(file_path, os.path.join(subcategory_folder, filename))