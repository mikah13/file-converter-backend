from typing import Union
from PIL import Image
from fastapi import FastAPI, File, HTTPException, Response, UploadFile
from io import BytesIO
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
import zipfile
import os

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


@app.get("/uuid")
async def get_uuid():
    str_uuid = str(uuid.uuid4())
    process[str_uuid] = []
    return {"uuid": str_uuid}


@app.get("/download/{uuid}")
async def download(uuid: str):
    if uuid not in process:
        raise HTTPException(status_code=404, detail="UUID not found")

    # return process[uuid]
    # Create a BytesIO object to store the zipped files
    zip_buffer = BytesIO()

    # Create a ZIP file
    with zipfile.ZipFile("./image.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        for image, format, filename in process[uuid]:
            try:
                image_data = Image.open(BytesIO(image))
                # image_buffer = get_image_buffer(image_data)
                zipf.writestr(
                    f"{filename}.{format}",
                    image_data,
                    compress_type=zipfile.ZIP_DEFLATED,
                )
            except Exception as e:
                print(f"Error processing file {filename}: {str(e)}")
    zip_buffer.seek(0)
    response = StreamingResponse(
        content=zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=download.zip"},
    )
    # return response


@app.post("/convert")
async def upload_file(file: UploadFile, format: str, quality: int):
    if not file:
        return {"message": "No upload file sent"}

    if not quality:
        quality = 50
    if quality > 100:
        quality = 100
    if quality < 0:
        quality = 0
    image_quality = 50 + int(quality / 2)

    # return message
    if not format:
        format = "png"
    original_image = Image.open(file.file)
    converted_image = BytesIO()
    original_image.save(
        converted_image, image_formats[format], optimize=True, quality=image_quality
    )

    response = StreamingResponse(converted_image, media_type="image/" + format)

    converted_image.seek(0)

    return response
