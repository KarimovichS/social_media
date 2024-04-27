import tempfile
from fastapi import APIRouter, Depends, UploadFile, File
from minio import Minio

ACCESS_KEY = "huCosEyz2repf0fwEW3o"
SECRET_KEY = "lzM7ama2Pg3lSBlrGYhnsZwOpcvHKkCqvSeWwiFr"

router = APIRouter(prefix="/files", tags=["files"])

client = Minio(
    "127.0.0.1:9000",
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False
)


@router.post("/", tags=['upload'])
def file_upload(file: UploadFile = File(...)):
    handler, path = tempfile.mkstemp(suffix=f"{file.filename.split('.')[-1]}")
    with open(path, "wb") as f:
        f.write(file.file.read())
    client.fput_object(
        'images', file.filename, path
    )

    return {'file': file.filename}


