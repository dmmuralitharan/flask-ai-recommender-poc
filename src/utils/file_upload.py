import os
from flask import current_app
from werkzeug.utils import secure_filename


def save__file(file, content, file_type, id, index_number, image_size=1, video_size=5):
    if not file:
        return None
    
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0)

    if file_type == "image":
        max_size = image_size * 1024 * 1024  # 1 MB
    elif file_type == "video":
        max_size = video_size * 1024 * 1024  # 5 MB
    else:
        raise ValueError("Invalid file_type. Must be 'image' or 'video'.")

    if not (0 < file_length <= max_size):
        raise ValueError(f"{file_type.capitalize()} file must be between 0 and {max_size // (1024 * 1024)} MB.")


    _, file_extension = os.path.splitext(file.filename)
    new_filename = f"{content}_{file_type}_{id}_{index_number}{file_extension}"
    secure_name = secure_filename(file.filename)

    dynamic_folder = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        f"{content}_resourses/{content}_id_{id}/",
    )

    os.makedirs(dynamic_folder, exist_ok=True)

    file_path = os.path.join(dynamic_folder, new_filename)

    file.save(file_path)

    return file_path
