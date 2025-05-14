from .config import config
from PIL import Image
from typing import Optional
from utils.logging import logger
import models.zipline
import io
import requests

def uploadToZipline(url: str) -> Optional[str]:
    try:
        logger.debug(url)
        originalImageBytesIO = io.BytesIO(requests.get(url).content)
        originalImage = Image.open(originalImageBytesIO).convert("RGB")
        newImage = Image.new("RGB", originalImage.size)
        newImage.putdata(originalImage.getdata()) # pyright: ignore[reportArgumentType]
        newImageBytesIO = io.BytesIO()
        newImage.save(newImageBytesIO, subsampling = 0, quality = 90, format = "JPEG")
        response = requests.post(
			"https://share.caldeirag.xyz/api/upload",
			headers = { "Authorization": f"{config['display']['posters']['ziplineAuth']}", "Content-Type": "multipart/form-data" },
			files = { "file": newImageBytesIO.getvalue() }
		)
        logger.debug("HTTP %d, %s, %s", response.status_code, response.headers, response.text.strip())
        data: models.zipline.UploadResponse = response.json()
        if not data["success"]:
        	raise Exception(data["data"]["error"])
        return data["data"]["url"]
    except:
        logger.exception("An unexpected error occured while uploading an image to Zipline")
