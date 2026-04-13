from flask import Blueprint, send_from_directory
from config import UPLOAD_FOLDER

files_bp = Blueprint("files", __name__, url_prefix="/files")


@files_bp.get("/<path:filename>")
def serve_uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=False)