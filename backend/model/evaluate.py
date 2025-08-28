import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from mlp_mixer import MlpMixer


IMG_SIZE = 64
BATCH_SIZE = 100

# Data preprocessing
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor()
])

test_data = datasets.ImageFolder("dataset/test", transform=transform)
test_loader = DataLoader(test_data, batch_size=BATCH_SIZE, shuffle=False)

# Load model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MlpMixer(image_size=IMG_SIZE)
model.load_state_dict(torch.load("mlp_mixer.pth", map_location=device))
model.to(device)
model.eval()

# Evaluation
correct, total = 0, 0
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, preds = torch.max(outputs, 1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

accuracy = 100 * correct / total
print(f" Test Accuracy: {accuracy:.2f}%")
