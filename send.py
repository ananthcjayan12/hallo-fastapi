import requests

url = "https://5ipynsrw52o6us-8000.proxy.runpod.net/run_hallo2/"
files = {
    "source_image": open("/Users/ananthu/Desktop/new_repos/hallo-fastapi/1.jpg", "rb"),
    "driving_audio": open("/Users/ananthu/Desktop/new_repos/hallo-fastapi/audio.mp3", "rb")
}

response = requests.post(url, files=files)

if response.status_code == 200:
    # Save the received video
    with open("output.mp4", "wb") as f:
        f.write(response.content)
    print("Conversion successful! Video saved as output.mp4")
else:
    print("Error:", response.json())
