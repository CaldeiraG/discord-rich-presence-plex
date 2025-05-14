from .config import config
from typing import Optional
from utils.logging import logger
import requests

def uploadToZipline(url: str) -> Optional[str]:
    try:
        originalImage = requests.get(url).content
        filename = url.split("/")[-1] 
        #originalImageBytesIO = io.BytesIO(requests.get(url).content)
        #originalImage = Image.open(originalImageBytesIO).convert("RGB")
        #newImage = Image.new("RGB", originalImage.size)
        #newImage.putdata(originalImage.getdata()) # pyright: ignore[reportArgumentType]
        #newImageBytesIO = io.BytesIO()
        #newImage.save(newImageBytesIO, subsampling = 0, quality = 90, format = "JPEG")
        response = requests.post(
            "https://share.caldeirag.xyz/api/upload",
            headers = { "Authorization": f"{config['display']['posters']['ziplineAuth']}"},
            files = {"file" : (filename,originalImage, "image/jpeg") })
        logger.debug("HTTP %d, %s, %s", response.status_code, response.headers, response.text.strip())
        data = response.json()
        if not response.status_code == 200:
            raise Exception(data["files"]["error"])
        return data["files"][0]["url"]
    except:
        logger.exception("An unexpected error occured while uploading an image to Zipline")
