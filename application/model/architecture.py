from torchvision import models
from torch import nn
from torchvision import transforms
import torch

transformer = transforms.Compose([
    transforms.Resize(225),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225])
])

try:
    model = models.resnet101(pretrained=True)
    fc = nn.Sequential(nn.Linear(2048, 2), nn.Sigmoid())
    model.fc = fc
except Exception as e:
    print("Unable to download model")
    print(e.with_traceback())
    print({'error': "Unable to download model"})

try :
    model.load_state_dict(torch.load('./data/model_transfer.brain'))
    model.eval()
except Exception as e:
    print("Unable to load trained model")
    print(e)
