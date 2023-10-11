from typing import Union
from PIL import Image
from fastapi import FastAPI, File, Response, UploadFile
from io import BytesIO
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid

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
async def upload_metadata(format: str):
    if format not in image_formats:
        return {"message": "Invalid format"}
    str_uuid = str(uuid.uuid4())
    message = {"uuid": str_uuid, "format": format}
    process[str_uuid] = {"uuid": str_uuid, "format": format}
    return message


@app.post("/upload")
async def upload_file(file: UploadFile, format):
    if not file:
        return {"message": "No upload file sent"}

    # str_uuid = str(uuid.uuid4())
    # message = {"uuid": str_uuid, "format": format}
    # process[str_uuid] = {"uuid": str_uuid, "format": format}
    # return message
    if not format:
        format = "png"
    original_image = Image.open(file.file)
    converted_image = BytesIO()
    original_image.save(
        converted_image, image_formats[format], optimize=True, quality=95
    )
    converted_image.seek(0)

    return StreamingResponse(converted_image, media_type="image/" + format)
