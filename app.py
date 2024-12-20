import flet as ft
from delete_duplicates import find_duplicates, delete_file
from organize_files    import organize_folder
from resize            import batch_resize
from image_converter   import convert_images

def main(page: ft.Page):
	page.title="Easify"
	page.window.width=1000
	page.window.height=900
	page.window.min_width=1000
	page.window.min_height=900
	page.padding=0
	page.bgcolor="#232323"
	page.theme_mode=ft.ThemeMode.DARK

	# --- Custom theme ---
	page.theme = ft.Theme(
		color_scheme_seed="#232323",
		visual_density=ft.VisualDensity.COMFORTABLE,
		color_scheme=ft.ColorScheme(
			primary=ft.Colors.WHITE30,
			secondary="#232323",
			background="#232323",
			surface="#111214",
		)
	)

	# --- State var ---
	state = {
		"current_duplicates": [],
		"current_view": "duplicates",
		"resize_input_folder": "",
		"resize_output_folder": "",
		"selecting_resize_output": False,
		"convert_input_file": "",
	}

	selected_dir_text=ft.Text(
		value="No directory selected",
		size=15,
		color=ft.Colors.WHITE30,
	)

	# --- Utils ---
	# --- Delete duplicates ---
	result_text=ft.Text(
		size=15,
		weight=ft.FontWeight.BOLD,
	)

	loading_bar=ft.ProgressBar(
		visible=False,
		width=400
	)

	duplicates_list=ft.ListView(
		expand=1,
		spacing=10,
		height=200
	)

	delete_all_buttons=ft.ElevatedButton(
		text="Delete all duplicates ",
		icon=ft.Icons.DELETE_SWEEP,
		color=ft.Colors.WHITE30,
		bgcolor="#111214",
		visible=False,
		on_click=lambda e: delete_all_duplicates()
	)

	# --- Organize directory ---
	organize_directory_text=ft.Text(
		value="No directory selected",
		size=15,
		color=ft.Colors.WHITE30,
	)

	organize_result_text=ft.Text(
		size=15,
		weight=ft.FontWeight.BOLD,
	)

	# --- Resize images ---
	resize_input_text=ft.Text(
		value="Input folder: not selected yet.",
		size=15,
		color=ft.Colors.WHITE30,
	)

	resize_output_text=ft.Text(
		value="Output folder: not selected yet.",
		size=15,
		color=ft.Colors.WHITE30,
	)

	resize_result_text=ft.Text(
		size=15,
		weight=ft.FontWeight.BOLD,
	)

	width_field=ft.TextField(
		label="Width",
		value="800",
		width=100,
		text_align=ft.TextAlign.RIGHT,
		keyboard_type=ft.KeyboardType.NUMBER,
	)

	height_field=ft.TextField(
		label="Height",
		value="600",
		width=100,
		text_align=ft.TextAlign.RIGHT,
		keyboard_type=ft.KeyboardType.NUMBER,
	)

	# --- Convert controls ---
	convert_input_text=ft.Text(
		value="No file selected yet",
		size=15,
		color=ft.Colors.WHITE30,
	)

	convert_result_text=ft.Text(
		size=15,
		weight=ft.FontWeight.BOLD,
	)

	format_dropdown=ft.Dropdown(
		label="Output format",
		width=200,
		options=[
			ft.dropdown.Option("PNG"),
			ft.dropdown.Option("JPG"),
			ft.dropdown.Option("BMP"),
			ft.dropdown.Option("WEBP"),
			ft.dropdown.Option("GIF"),
		],
		value="PNG"
	)

	# --- Sidebar picker ---
	def change_view(e):
		selected=e.control.selected_index
		if selected==0:
			content_area.content=duplicate_files_view
			state["current_view"]="duplicates"
		elif selected==1:
			content_area.content=organize_files_view
			state["current_view"]="organize"
		elif selected==2:
			content_area.content=resize_files_view
			state["current_view"]="resize"
		elif selected==3:
			content_area.content=convert_images_view
			state["current_view"]="convert"
		elif selected==4:
			state["current_view"]="coming soon"
			content_area.content=ft.Text(
				value="Coming soon...",
				size=30,
			)
		content_area.update()

	# --- Folder picker handler ---
	def handle_file_picker(e: ft.FilePickerResultEvent):
		if e.files and len(e.files)>0:
			file_path=e.files[0].path
			state["convert_input_file"]=file_path
			convert_input_text.value=f"Selected file: {file_path}"
			convert_input_text.update()

	def handle_folder_picker(e: ft.FilePickerResultEvent):
		if e.path:
			if state["current_view"]=="duplicates":
				selected_dir_text.value=f"Selected directory: {e.path}"
				selected_dir_text.update()
				scan_directory(e.path)
			elif state["current_view"]=="organize":
				organize_directory_text.value=f"Selected directory: {e.path}"
				organize_directory_text.update()
				organize_directory(e.path)
			elif state["current_view"]=="resize":
				if state["selecting_resize_output"]:
					state["resize_output_folder"]=e.path
					resize_output_text.value=f"Selected output folder: {e.path}"
					resize_output_text.update()
				else:
					state["resize_input_folder"]=e.path
					resize_input_text.value=f"Selected input folder: {e.path}"
					resize_input_text.update()

	def select_input_folder():
		state["selecting_resize_output"]=False
		folder_picker.get_directory_path()

	def select_output_folder():
		state["selecting_resize_output"]=True
		folder_picker.get_directory_path()

	def convert_image():
		try:
			if not state["convert_input_file"]:
				convert_result_text.value="Select a file before converting"
				convert_result_text.color=ft.Colors.RED_300
				convert_result_text.update()
				return
			if not format_dropdown.value:
				convert_result_text.value="Select output format before converting"
				convert_result_text.color=ft.Colors.RED_300
				convert_result_text.update()
				return

			convert_images(state["convert_input_file"], format_dropdown.value)
			convert_result_text.value="Converted image successfully"
			convert_result_text.color=ft.Colors.GREEN_300
			convert_result_text.update()

		except Exception as e:
			convert_result_text.value=f"Failed to convert image: {str(e)}"
			convert_result_text.color=ft.Colors.RED_300
			convert_result_text.update()

	def resize_images():
		try:
			if not state["resize_input_folder"] and not state["resize_output_folder"]:
				resize_result_text.value="Select input and output folders before resizing"
				resize_result_text.color=ft.Colors.RED_300
				resize_result_text.update()
				return

			width=int(width_field.value)
			height=int(height_field.value)

			if width<=0 or height<=0:
				resize_result_text.value="Width and height must be positive numbers"
				resize_result_text.color=ft.Colors.RED_300
				resize_result_text.update()
				return

			batch_resize(state["resize_input_folder"], state["resize_output_folder"], width, height)
			resize_result_text.value=f"Resized images successfully"
			resize_result_text.color=ft.Colors.GREEN_300
			resize_result_text.update()

		except ValueError:
			resize_result_text.value = "Width and height must be positive numbers"
			resize_result_text.color = ft.Colors.RED_300
			resize_result_text.update()
		except Exception as e:
			resize_result_text.value = f"Failed to resize images: {str(e)}"
			resize_result_text.color = ft.Colors.RED_300
			resize_result_text.update()

	def organize_directory(directory):
		try:
			organize_folder(directory)
			organize_result_text.value=f"Organized {directory}"
			organize_result_text.color=ft.Colors.GREEN_300
		except Exception as e:
			organize_result_text.value=f"Failed to organize {directory}: {e}"
			organize_result_text.color=ft.Colors.RED_300

		organize_result_text.update()

	def scan_directory(directory):
		duplicates_list.controls.clear()
		state["current_duplicates"]=find_duplicates(directory)
		loading_bar.visible=True
		loading_bar.update()

		try:
			state["current_duplicates"]=find_duplicates(directory)
		finally:
			loading_bar.visible=False
			loading_bar.update()

		if not state["current_duplicates"]:
			delete_all_buttons.visible=False
			result_text.value="No duplicates found"
			result_text.color=ft.Colors.WHITE30
		else:
			result_text.value=f"Found {len(state['current_duplicates'])} duplicates"
			result_text.color=ft.Colors.RED_300

			delete_all_buttons.visible=True

			for duplicate_file, original in state["current_duplicates"]:
				duplicate_row=ft.Row([
					ft.Text(
						value=f"Duplicate: {duplicate_file}\nOriginal: {original}",
						size=15,
						expand=True,
						color=ft.Colors.WHITE30
					),
					ft.ElevatedButton(
						text="Delete ",
						icon=ft.Icons.DELETE_FOREVER,
						color=ft.Colors.WHITE30,
						bgcolor="#232323",
						on_click=lambda e, filepath=duplicate_file: delete_duplicate(filepath)
					)
				])
				duplicates_list.controls.append(duplicate_row)

		duplicates_list.update()
		result_text.update()
		delete_all_buttons.update()

	def delete_duplicate(filepath):
		if delete_file(filepath):
			result_text.value=f"Deleted {filepath}"
			result_text.color=ft.Colors.GREEN_300
			for control in duplicates_list.controls[:]:
				if filepath in control.controls[0].value:
					duplicates_list.controls.remove(control)
			state["current_duplicates"]=[(dup, orig) for dup, orig in state["current_duplicates"] if dup != filepath]
			if not state["current_duplicates"]:
				delete_all_buttons.visible=False
		else:
			result_text.value=f"Failed to delete {filepath}"
			result_text.color=ft.Colors.RED_300

		duplicates_list.update()
		result_text.update()
		delete_all_buttons.update()

	def delete_all_duplicates():
		deleted_count=0
		failed_count=0

		for duplicate_file, _ in state["current_duplicates"][:]:
			if delete_file(duplicate_file):
				deleted_count+=1
			else:
				failed_count+=1

		duplicates_list.controls.clear()
		state["current_duplicates"]=[]
		delete_all_buttons.visible=False

		if failed_count==0:
			result_text.value=f"Deleted {deleted_count} duplicates successfully"
			result_text.color=ft.Colors.GREEN_300
		else:
			result_text.value=f"Deleted {deleted_count} duplicates succesfully. Failed to delete {failed_count} duplicates"
			result_text.color=ft.Colors.RED_300

		duplicates_list.update()
		result_text.update()
		delete_all_buttons.update()

	file_picker=ft.FilePicker(
		on_result=handle_file_picker
	)
	page.overlay.append(file_picker)

	file_picker.file_type=ft.FilePickerFileType.IMAGE
	file_picker.allowed_extensions=["jpg", "jpeg", "png", "bmp", "webp", "gif"]

	folder_picker=ft.FilePicker(
		on_result=handle_folder_picker
	)
	page.overlay.append(folder_picker)

	# --- Duplicate files view ---
	duplicate_files_view=ft.Container(
		content=ft.Column([
			ft.Container(
				content=ft.Text(
					value="Duplicate files",
					size=30,
					weight=ft.FontWeight.BOLD,
					color=ft.Colors.WHITE30,
				),
				margin=ft.margin.only(bottom=20),
			),
			ft.Row([
				ft.ElevatedButton(
					text="Select directory ",
					icon=ft.Icons.FOLDER_OPEN,
					color=ft.Colors.WHITE30,
					bgcolor="#111214",
					on_click=lambda _: folder_picker.get_directory_path()
				),
				delete_all_buttons,
			]),
			ft.Container(
				content=selected_dir_text,
				margin=ft.margin.only(top=10, bottom=10),
			),
			loading_bar,
			result_text,
			ft.Container(
				content=duplicates_list,
				border=ft.border.all(
					width=1,
					color=ft.Colors.WHITE30
				),
				border_radius=10,
				padding=20,
				margin=ft.margin.only(
					top=10
				),
				bgcolor="#111214",
				expand=True,
			)
		]),
		padding=30,
		expand=True,
	)

	# --- Organize files view ---
	organize_files_view=ft.Container(
		content=ft.Column([
			ft.Container(
				content=ft.Text(
					value="Organize files",
					size=30,
					weight=ft.FontWeight.BOLD,
					color=ft.Colors.WHITE30,
				),
				margin=ft.margin.only(bottom=20),
			),
			ft.ElevatedButton(
				text="Select directory ",
				icon=ft.Icons.FOLDER_OPEN,
				color=ft.Colors.WHITE30,
				bgcolor="#111214",
				on_click=lambda _: folder_picker.get_directory_path()
			),
			ft.Container(
				content=organize_directory_text,
				margin=ft.margin.only(top=10, bottom=10),
			),
			organize_result_text,
			ft.Container(
				content=ft.Column([
					ft.Text(
						value="Files will be organized the following way:",
						size=15,
						weight=ft.FontWeight.BOLD,
						color=ft.Colors.WHITE30,
					),
					ft.Text(
						value="· multimedia\n - images\n - videos\n - audio",
						color=ft.Colors.WHITE30,
						size=15,
					),
					ft.Text(
						value="· modeling\n - blender\n - maya\n - zbrush\n - fbx\n - obj",
						color=ft.Colors.WHITE30,
						size=15,
					),
					ft.Text(
						value="· documents\n - docs\n - datasets",
						color=ft.Colors.WHITE30,
						size=15,
					),
					ft.Text(
						value="· executables\n - executables\n - scripts",
						color=ft.Colors.WHITE30,
						size=15,
					),
					ft.Text(
						value="· compressed\n - compressed\n - archives",
						color=ft.Colors.WHITE30,
						size=15,
					),
				]),
				border=ft.border.all(width=1, color=ft.Colors.WHITE30),
				border_radius=10,
				padding=20,
				margin=ft.margin.only(top=10),
				bgcolor="#111214",
			)
		]),
		padding=30,
		expand=True,
	)

	resize_files_view=ft.Container(
		content=ft.Column([
			ft.Container(
				content=ft.Text(
					value="Resize images",
					size=30,
					weight=ft.FontWeight.BOLD,
					color=ft.Colors.WHITE30,
				),
				margin=ft.margin.only(bottom=20),
			),
			ft.Row([
				ft.ElevatedButton(
					text="Select input folder ",
					icon=ft.Icons.FOLDER_OPEN,
					color=ft.Colors.WHITE30,
					bgcolor="#111214",
					on_click=lambda _: select_input_folder()
				),
				ft.ElevatedButton(
					text="Select output folder ",
					icon=ft.Icons.FOLDER_OPEN,
					color=ft.Colors.WHITE30,
					bgcolor="#111214",
					on_click=lambda _: select_output_folder()
				)
			]),
			ft.Container(
				content=ft.Column([
					resize_input_text,
					resize_output_text,
				]),
				margin=ft.margin.only(top=10, bottom=10),
			),
			ft.Container(
				content=ft.Column([
					ft.Text(
						value="Image dimensions",
						size=15,
						weight=ft.FontWeight.BOLD,
						color=ft.Colors.WHITE30,
					),
					ft.Row([
						width_field,
						ft.Text(
							value="x",
							size=15,
						),
						height_field,
						ft.Text(
							value="px",
							size=15,
						)
					])
				]),
				margin=ft.margin.only(bottom=10),
			),
			ft.ElevatedButton(
				text="Resize images ",
				icon=ft.Icons.PHOTO_SIZE_SELECT_LARGE,
				color=ft.Colors.WHITE30,
				bgcolor="#111214",
				on_click=lambda _: resize_images()
			),
			resize_result_text,
			ft.Container(
				content=ft.Column([
					ft.Text(
						value="Note: Images will be resized in-place. Original files will not be modified or deleted.",
						size=15,
						weight=ft.FontWeight.BOLD,
						color=ft.Colors.WHITE30,
					),
				]),
				border=ft.border.all(width=1, color=ft.Colors.WHITE30),
				border_radius=10,
				padding=20,
				margin=ft.margin.only(top=10),
				bgcolor="#111214",
			)
		]),
		padding=30,
		expand=True,
	)

	convert_images_view=ft.Container(
		content=ft.Column([
			ft.Container(
				content=ft.Text(
					value="Convert images",
					size=30,
					weight=ft.FontWeight.BOLD,
					color=ft.Colors.WHITE30,
				),
				margin=ft.margin.only(bottom=20),
			),
			ft.ElevatedButton(
				text="Select image ",
				icon=ft.Icons.IMAGE,
				color=ft.Colors.WHITE30,
				bgcolor="#111214",
				on_click=lambda _: file_picker.pick_files()
			),
			ft.Container(
				content=convert_input_text,
				margin=ft.margin.only(top=10, bottom=10),
			),
			format_dropdown,
			ft.Container(
				margin=ft.margin.only(top=10),
				content=ft.ElevatedButton(
					text="Convert image ",
					icon=ft.Icons.TRANSFORM,
					color=ft.Colors.WHITE30,
					bgcolor="#111214",
					on_click=lambda _: convert_image()
				)
			),
			convert_result_text,
			ft.Container(
				content=ft.Column([
					ft.Text(
						value="Information:",
						size=15,
						weight=ft.FontWeight.BOLD,
						color=ft.Colors.WHITE30,
					),
					ft.Text(
						value="· Supported formats : PNG, JPEG, BMP, GIF, WEBP",
						color=ft.Colors.WHITE30,
						size=15,
					),
					ft.Text(
						value="· Original image will not be affected.",
						color=ft.Colors.WHITE30,
						size=15,
					),
					ft.Text(
						value="· Converted image will be saved in the same folder as the original image.",
						color=ft.Colors.WHITE30,
						size=15,
					),
					ft.Text(
						value="· Turning into a JPEG or JPG, images with no background will be turned into white background.",
						color=ft.Colors.WHITE30,
						size=15,
					)
				]),
				border=ft.border.all(width=1, color=ft.Colors.WHITE30),
				border_radius=10,
				padding=20,
				margin=ft.margin.only(top=10),
				bgcolor="#111214",
			)
		]),
		padding=30,
		expand=True,
	)

	content_area=ft.Container(
		content=duplicate_files_view,
		expand=True,
	)

	# --- Sidebar ---
	rail = ft.NavigationRail(
		selected_index=0,
		label_type=ft.NavigationRailLabelType.ALL,
		min_width=100,
		min_extended_width=200,
		group_alignment=-0.9,
		destinations=[
			ft.NavigationRailDestination(
				icon=ft.Icons.DELETE_FOREVER,
				label="_duplicates"
			),
			ft.NavigationRailDestination(
				icon=ft.Icons.FOLDER_COPY,
				label="_organize"
			),
			ft.NavigationRailDestination(
				icon=ft.Icons.PHOTO_SIZE_SELECT_LARGE,
				label="_resize"
			),
			ft.NavigationRailDestination(
				icon=ft.Icons.TRANSFORM,
				label="_convert"
			),
			ft.NavigationRailDestination(
				icon=ft.Icons.ADD_BOX,
				label="_coming soon"
			)
		],
		on_change=change_view,
		bgcolor="#111214",
	)

	page.add(
		ft.Row(
			controls=[
				rail,
				content_area
			],
		expand=True,
		)
	)

ft.app(target=main)