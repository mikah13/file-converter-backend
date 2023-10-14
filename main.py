from typing import Union
from PIL import Image
from fastapi import FastAPI, File, HTTPException, Response, UploadFile
from io import BytesIO
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
import zipfile
import os
import numpy as np

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


@app.post("/compress")
async def compress(file: UploadFile, format: str):
    if not file:
        return {"message": "No upload file sent"}
    original_image = Image.open(file.file)
    image = np.asarray(original_image) / 255
    w, h, d = image.shape
    # Get the feature matrix X
    X = image.reshape((w * h, d))
    K = 40  # the number of colors in the image
    colors, _ = find_k_means(X, K, max_iters=20)
    idx = find_closest_centroids(X, colors)
    idx = np.array(idx, dtype=np.uint8)
    X_reconstructed = np.array(colors[idx, :] * 255, dtype=np.uint8).reshape((w, h, d))
    compressed_image = Image.fromarray(X_reconstructed)
    processed_image = BytesIO()
    compressed_image.save(processed_image, optimize=True)

    response = StreamingResponse(processed_image, media_type="image/" + format)

    processed_image.seek(0)
    return response


# Compression algorithm


def initialize_K_centroids(X, K):
    """Choose K points from X at random"""
    m = len(X)
    return X[np.random.choice(m, K, replace=False), :]


def find_closest_centroids(X, centroids):
    return c


def compute_means(X, idx, K):
    return centroids


def find_k_means(X, K, max_iters=10):
    return centroids, idx
