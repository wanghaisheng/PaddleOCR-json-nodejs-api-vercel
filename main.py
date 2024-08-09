from fastapi import FastAPI, File, UploadFile
from PPOCR_api import GetOcrApi
import os

# Initialize the OCR API (replace with the correct path to your PaddleOCR-json executable)
ocr_api_path = "Your Path/PaddleOCR-json.exe"
ocr = GetOcrApi(ocr_api_path)

app = FastAPI()

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "running"}

# OCR image file upload endpoint
@app.post("/ocr")
def ocr_image(file: UploadFile = File(...)):
    try:
        # Save the uploaded file to a temporary location
        with open("test.jpg", "wb") as f:
            f.write(file.file.read())
        
        # Run OCR on the image
        res = ocr.run("test.jpg")
        return {"status": "success", "data": res}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# OCR image byte stream endpoint
@app.post("/ocr-byte-stream")
def ocr_byte_stream(image_bytes: bytes = File(...)):
    try:
        # Run OCR on the image byte stream
        res = ocr.runBytes(image_bytes)
        return {"status": "success", "data": res}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# OCR PIL Image object endpoint
@app.post("/ocr-pil-image/")
def ocr_pil_image(image: UploadFile = File(...)):
    try:
        # Save the uploaded file to a temporary location
        with open("temp_image.jpg", "wb") as f:
            f.write(image.file.read())

        from PIL import Image
        from io import BytesIO

        # Open the image file
        image = Image.open("temp_image.jpg")
        # Convert Image object to byte stream
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        image_bytes = buffered.getvalue()

        # Run OCR on the image byte stream
        res = ocr.runBytes(image_bytes)
        return {"status": "success", "data": res}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Run the FastAPI server with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
