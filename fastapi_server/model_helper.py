import torch
from torchvision import models, transforms
from PIL import Image
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "saved_model.pth")

CLASS_NAMES = ["Dent", "Scratch", "Broken Light", "Glass Damage"]

REPAIR_COST = {
    "Dent": "₹4,000 – ₹12,000",
    "Scratch": "₹1,000 – ₹5,000",
    "Broken Light": "₹2,000 – ₹8,000",
    "Glass Damage": "₹6,000 – ₹18,000"
}

# Load model
model = models.resnet18(weights=None)
model.fc = torch.nn.Linear(model.fc.in_features, len(CLASS_NAMES))
state_dict = torch.load(MODEL_PATH, map_location="cpu")
model.load_state_dict(state_dict)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def predict(image_path):
    image = Image.open(image_path).convert("RGB")
    img_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(img_tensor)
        probabilities = torch.softmax(outputs, dim=1)[0]
        confidence, predicted_idx = torch.max(probabilities, dim=0)

    predicted_class = CLASS_NAMES[predicted_idx.item()]
    conf_percent = round(confidence.item() * 100, 2)
    cost = REPAIR_COST[predicted_class]

    return {
        "damage": predicted_class,
        "confidence": f"{conf_percent}%",
        "estimated_cost": cost
    }
