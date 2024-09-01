import os
import io
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image

app = FastAPI()

@app.post("/remove-bg/")
async def remove_background(file: UploadFile = File(...)):
    # Ensure file is an image
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image.")
    
    try:
        # Read image data
        image_bytes = await file.read()
        input_image = Image.open(io.BytesIO(image_bytes))

        # Ensure image is in a valid format
        if input_image.mode != "RGBA":
            input_image = input_image.convert("RGBA")

        # Remove background using rembg
        output_image = remove(image_bytes)

        # Convert processed image back to PIL format
        output_image = Image.open(io.BytesIO(output_image))

        # Save processed image to buffer
        buffer = io.BytesIO()
        output_image.save(buffer, format="PNG")
        buffer.seek(0)

        # Return the processed image as a response
        return StreamingResponse(buffer, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to the Background Removal API!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 0))  # Default to a random port if not provided
    uvicorn.run(app, host="0.0.0.0", port=port)
