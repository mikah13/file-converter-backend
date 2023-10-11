from typing import Union
from PIL import Image
from fastapi import FastAPI, File, Response, UploadFile
from io import BytesIO
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
import zipfile

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

image_formats = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "bmp": "BMP",
    "tiff": "TIFF",
    "tif": "TIFF",
    "webp": "WebP",
    # "sgi": "SGI",
    # "ppm": "PPM",
    # "msp": "MSP",
    # "im": "IM",
    "ico": "ICO",
    # "eps": "EPS",
    # "dds": "DDS",
    # "dib": "DIB",
    # "bpm": "BPM",
    # "blp": "BLP",
    # "spi": "SPIDER",
}

process = {}


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/extensions")
async def get_supported_extensions():
    return {"extensions": image_formats}


@app.get("/metadata")
async def upload_metadata():
    if format not in image_formats:
        return {"message": "Invalid format"}
    str_uuid = str(uuid.uuid4())
    message = {"uuid": str_uuid, "format": format}
    process[str_uuid] = {"uuid": str_uuid, "format": format}
    return message


@app.get("/uuid")
async def get_uuid():
    str_uuid = str(uuid.uuid4())
    process[str_uuid] = []
    return {"uuid": str_uuid}


@app.get("/download/{uuid}")
async def download(uuid: str):
    if uuid not in process:
        return {"message": "UUID not found"}
    return process.get(uuid)


@app.post("/upload")
async def upload_file(file: UploadFile, format: str, uuid: str):
    if not file:
        return {"message": "No upload file sent"}

    # return message
    if not format:
        format = "png"
    original_image = Image.open(file.file)
    converted_image = BytesIO()
    original_image.save(
        converted_image, image_formats[format], optimize=True, quality=95
    )
    if uuid in process:
        process[uuid].append(converted_image)
    else:
        process[uuid] = [converted_image]
    converted_image.seek(0)

    return StreamingResponse(converted_image, media_type="image/" + format)
