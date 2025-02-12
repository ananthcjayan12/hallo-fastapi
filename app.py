import os
import shutil
import subprocess
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

app = FastAPI()

@app.post("/run_hallo2/")
async def run_hallo2_api(
    source_image: UploadFile = File(...),
    driving_audio: UploadFile = File(...)
):
    # Create a temporary directory for processing
    temp_dir = "hallo2_temp"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)
    
    # Save the uploaded source image
    image_path = os.path.join(temp_dir, "source.jpg")
    with open(image_path, "wb") as img_file:
        img_file.write(await source_image.read())
    
    # Save the uploaded driving audio
    audio_path = os.path.join(temp_dir, "driving.wav")
    with open(audio_path, "wb") as audio_file:
        audio_file.write(await driving_audio.read())
    
    # Build the command to run the hallo2 inference script.
    # Adjust the command parameters if your config file or output paths differ.
    command = [
        "python", "scripts/inference_long.py",
        "--config", "configs/inference/long.yaml",
        "--source_image", image_path,
        "--driving_audio", audio_path
    ]
    
    # Execute the inference command
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        return {"error": f"Inference failed: {e}"}
    
    # Define the expected output video path
    output_video = os.path.join(temp_dir, "output.mp4")
    
    # Check if the output file was generated
    if os.path.exists(output_video):
        return FileResponse(
            output_video,
            media_type="video/mp4",
            filename="output.mp4"
        )
    else:
        return {"error": "Output video not found."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
