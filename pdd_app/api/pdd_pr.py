import io
from pathlib import Path
import torch
import torch.nn as nn
from fastapi import APIRouter, File, UploadFile, HTTPException
from torchvision import transforms
from PIL import Image

# ================= PATH =================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "melis_model.pth"

model_router = APIRouter(prefix='/model', tags=['Model'])

# ================= CLASSES =================
class_names = [
    'Ограничение скорости (20 км/ч)',
    'Ограничение скорости (30 км/ч)',
    'Ограничение скорости (50 км/ч)',
    'Ограничение скорости (60 км/ч)',
    'Ограничение скорости (70 км/ч)',
    'Ограничение скорости (80 км/ч)',
    'Конец ограничения скорости (80 км/ч)',
    'Ограничение скорости (100 км/ч)',
    'Ограничение скорости (120 км/ч)',
    'Обгон запрещён',
    'Обгон запрещён для ТС более 3,5 тонн',
    'Главная дорога на следующем перекрёстке',
    'Главная дорога',
    'Уступите дорогу',
    'Стоп',
    'Движение запрещено',
    'Движение ТС более 3,5 тонн запрещено',
    'Въезд запрещён',
    'Общее предупреждение',
    'Опасный поворот налево',
    'Опасный поворот направо',
    'Двойной поворот',
    'Неровная дорога',
    'Скользкая дорога',
    'Сужение дороги справа',
    'Дорожные работы',
    'Светофорное регулирование',
    'Пешеходы',
    'Дети',
    'Велосипедисты',
    'Осторожно: лёд / снег',
    'Дикие животные',
    'Конец всех ограничений скорости и обгона',
    'Поворот направо',
    'Поворот налево',
    'Движение прямо',
    'Движение прямо или направо',
    'Движение прямо или налево',
    'Держаться правой стороны',
    'Держаться левой стороны',
    'Круговое движение',
    'Конец запрета обгона',
    'Конец запрета обгона для ТС более 3,5 тонн'
]

# ================= TRANSFORM =================
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor()
])

# ================= MODEL =================
class CheckImage(nn.Module):
    def __init__(self):
        super().__init__()

        # 🔴 ИМЕНА СЛОЁВ ОСТАВЛЕНЫ КАК В .pth
        self.first = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout2d(0.25),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout2d(0.25),

            nn.AdaptiveAvgPool2d((1, 1))  # ✅ ИСПРАВЛЕНИЕ
        )

        self.second = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, 43)
        )

    def forward(self, x):
        x = self.first(x)
        x = self.second(x)
        return x


# ================= DEVICE =================
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# ================= LOAD MODEL =================
model = CheckImage()
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.to(device)
model.eval()

# ================= API =================
@model_router.post('/predict')
async def check_image(file: UploadFile = File(...)):
    try:
        data = await file.read()
        if not data:
            raise HTTPException(status_code=400, detail='Изображение не получено')

        image = Image.open(io.BytesIO(data)).convert("RGB")
        img_tensor = transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            outputs = model(img_tensor)
            probs = torch.softmax(outputs, dim=1)
            confidence, class_id = torch.max(probs, dim=1)

        return {
            "name": class_names[class_id.item()],
            "confidence": f"{round(confidence.item() * 100, 2)}%"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
