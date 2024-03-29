# -*- coding: utf-8 -*-
"""CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1q5Jzob-vPcg5WApLLIGIzIZ5CvEAwpzR
"""

# Imports
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader
import  torchvision.datasets as datasets
import torchvision.transforms as transforms

# CNN architecture
class CNN(nn.Module):
  def __init__(self, in_channels=1, num_classes=10):
    super(CNN,self).__init__()
    self.conv1 = nn.Conv2d(1, 8, kernel_size=(3,3), stride=(1,1), padding=(1,1))
    self.pool = nn.MaxPool2d(kernel_size=(2,2), stride=(2,2))
    self.conv2 = nn.Conv2d(8, 16, kernel_size=(3,3), stride=(1,1), padding=(1,1))
    self.fc1 = nn.Linear(16*7*7, num_classes)

  def forward(self,x):
    x=self.pool(F.relu(self.conv1(x)))
    x=self.pool(F.relu(self.conv2(x)))
    x=x.reshape(x.shape[0],-1)
    x=self.fc1(x)
    return x

# Hyperparameters
in_channels = 1
num_classes = 10
learning_rate = 0.001
batch_size = 64
num_epochs = 1

# Load Data
train_dataset = datasets.MNIST(root='dataset/',train=True, transform=transforms.ToTensor(),download=True)
train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
test_dataset = datasets.MNIST(root='dataset/',train=False, transform=transforms.ToTensor(),download=True)
test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=True)

# Initialize Network
model = CNN()

# Loss & Optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Train network
for epoch in range(num_epochs):
  for batch_ix, (data, targets) in enumerate(train_loader):
    data = data
    targets = targets

    # forward
    scores=model(data)
    loss=criterion(scores,targets)

    # backward
    optimizer.zero_grad()
    loss.backward()

    # gradient descent
    optimizer.step()

# Check accuracy
def check_accuracy(loader,model):
  num_correct=0
  num_samples=0
  model.eval()
  with torch.no_grad():
    for x, y in loader:
      scores = model(x)
      _, predictions = scores.max(1)
      num_correct += (predictions==y).sum()
      num_samples += predictions.size(0)
    print(f'Got {num_correct}/{num_samples} with accuracy {float(num_correct)/float(num_samples)*100:.2f}')
  model.train()

check_accuracy(train_loader, model)
check_accuracy(test_loader, model)

