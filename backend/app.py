from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from PIL import Image
import io
import torch
from backend.model.mlp_mixer import MlpMixer
import torchvision.transforms as transforms
import torch.nn.functional as F

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Model configuration (must match training)
IMG_SIZE = 64
PATCH_SIZE = 16
NUM_CLASSES = 2
CLASS_NAMES = ["class0", "class1"]  # replace with your dataset class names

# Load model
model = MlpMixer(image_size=IMG_SIZE, patch_size=PATCH_SIZE, num_classes=NUM_CLASSES)
model.load_state_dict(torch.load("mlp_mixer.pth", map_location=device))
model.to(device)
model.eval()

# Preprocessing 
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
])

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Read image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        img_tensor = transform(image).unsqueeze(0).to(device)  # add batch dimension

        # Forward pass
        with torch.no_grad():
            outputs = model(img_tensor)
            probs = F.softmax(outputs, dim=1)
            confidence, predicted_idx = torch.max(probs, 1)
            predicted_class = CLASS_NAMES[predicted_idx.item()]

        return {
            "predictedClass": predicted_class,
            "confidence": confidence.item()
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
