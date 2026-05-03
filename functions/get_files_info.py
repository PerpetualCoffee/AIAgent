import os

def get_files_info(working_directory, directory="."):
	try:
		# code that might raise an exception
		working_dir_abs = os.path.abspath(working_directory)
		target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
		
		# Will be True or False
		valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
		
		if not valid_target_dir:
			return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

		if not os.path.isdir(target_dir):
			return f'Error: "{directory}" is not a directory'

		contents = os.listdir(target_dir)
		lines = []
		for name in contents:
			# Once have this item, create:
			# 	its full path (so other os.functions can find it)
			# 	ts size in bytes (os.path.getsize())
			# 	whether its a directory (os.path.isdir())
			# then build a single line of output to display as required by task
			path = os.path.join(target_dir, name)
			size = os.path.getsize(path)
			is_dir = os.path.isdir(path)
			lines.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")
		return "\n".join(lines)
	except Exception as e:
		# runs ONLY if something inside the try block raised
		return f"Error: {e}"