from typing import TypedDict

class Response(TypedDict):
	success: bool
	status: int

class UploadResponseData(TypedDict):
	error: str
	url: str

class UploadResponse(Response):
	data: UploadResponseData
