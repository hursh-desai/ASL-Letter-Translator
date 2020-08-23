from io import BytesIO
from PIL import Image
import torchvision
import base64
import torch
import re

classes = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'I', 9:'J', 10:'K', 11:'L', 12:'M', 13:'N', 14:'O', 15:'P', 16:'Q', 17:'R',
           18:'S', 19:'T', 20:'U', 21:'V', 22:'W', 23:'X', 24:'Y',25:'Z', 26:'DELETE', 27:'NOTHING', 28:'SPACE'}

class ConvNet(torch.nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()
        self.conv1 = torch.nn.Conv2d(3, 96, 11, stride=4)
        self.conv2 = torch.nn.Conv2d(96, 256, 5, stride=2)
        #pooling
        self.pool1 = torch.nn.MaxPool2d(kernel_size=3, stride=2, padding=0)
        self.pool2 = torch.nn.MaxPool2d(kernel_size=3, stride=2, padding=0)
        # an affine operation: y = Wx + b
        self.fc1 = torch.nn.Linear(256 * 4 * 4, 256)
        self.fc2 = torch.nn.Linear(256, 128)
        self.fc3 = torch.nn.Linear(128, 29)
    def forward(self, x):
        x = torch.nn.functional.relu(self.conv1(x))
        x = self.pool1(x)
        x = torch.nn.functional.relu(self.conv2(x))
        x = self.pool2(x)
        x = x.view(-1, 256 * 4 * 4)
        x = torch.nn.functional.relu(self.fc1(x))
        x = torch.nn.functional.relu(self.fc2(x))
        # last layer doesn't have activation since we use pytorch's binary cross entropy loss
        x = self.fc3(x)
        return x
    
model = ConvNet()
model.load_state_dict(torch.load('model.pth'))
model.eval()
def predict(image):
    imgstr = re.search(r'base64,(.*)', image).group(1)
    image_bytes = BytesIO(base64.b64decode(imgstr))
    img = Image.open(image_bytes)
    img.save('image.jpg', 'JPEG')
    trans = torchvision.transforms.ToTensor()
    t = (trans(img))
    tensor = torch.unsqueeze(t, 0)
    y_pred = model(tensor)
    value, index = torch.max(y_pred, 1)
    prediction = classes[int(index.numpy())]
    return prediction