from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
import io

app = FastAPI()

@app.post("/remove-bg/")
async def remove_background(file: UploadFile = File(...)):
    try:
        if file is None or file.content_type is None:
            raise HTTPException(status_code=400, detail="Invalid file or content type")
        
        # Ensure the file is an image
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Read image data
        image_bytes = await file.read()
        input_image = Image.open(io.BytesIO(image_bytes))

        # Ensure the image is in RGBA format
        if input_image.mode != "RGBA":
            input_image = input_image.convert("RGBA")

        # Remove the background
        output_image = remove(image_bytes)

        # Convert back to a PIL image
        output_image = Image.open(io.BytesIO(output_image))

        # Save the processed image to a buffer
        buffer = io.BytesIO()
        output_image.save(buffer, format="PNG")
        buffer.seek(0)

        return StreamingResponse(buffer, media_type="image/png")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
