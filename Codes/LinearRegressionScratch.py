# -*- coding: utf-8 -*-
"""Linear Regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bdg7FRVcYn4AolwKk-ei4WBg5UWnLvyt
"""

import torch
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn import metrics

class CustomDataset:
  def __init__(self,data,targets):
    self.data=data
    self.targets=targets

  def __len__(self):
    return self.data.shape[0]

  def __getitem__(self,idx):
    current_sample=self.data[idx, :]
    current_target=self.targets[idx]
    return {
        "x":torch.tensor(current_sample,dtype=torch.float),
        "y":torch.tensor(current_target,dtype=torch.long)
    }

data,targets=make_classification(n_samples=1000)
train_data,test_data,train_targets,test_targets=train_test_split(data,
                                                                 targets,
                                                                 stratify=targets)

train_dataset=CustomDataset(train_data,train_targets)
test_dataset=CustomDataset(test_data,test_targets)

train_loader=torch.utils.data.DataLoader(
    train_dataset,batch_size=4,num_workers=2
)
test_loader=torch.utils.data.DataLoader(
    test_dataset,batch_size=4,num_workers=2
)

model=lambda x,w,b: torch.matmul(x,w)+b

train_data.shape

W=torch.randn(20,1,requires_grad=True)
b=torch.randn(1,requires_grad=True)
learning_rate=0.001

for epoch in range(10):
  epoch_loss=0
  counter=0
  for data in train_loader:
    xtrain=data['x']
    ytrain=data['y']

    # 1. prediction
    output=model(xtrain,W,b)

    # 2. loss
    loss=torch.mean((ytrain.view(-1)-output.view(-1))**2)
    epoch_loss=epoch_loss+loss.item()

    # 3. backprop
    loss.backward()

    # 4. update params
    with torch.no_grad():
      W=W-(learning_rate*W.grad)
      b=b-(learning_rate*b.grad)
    W.requires_grad_(True)
    b.requires_grad_(True)
    counter+=1
  print(epoch, epoch_loss/counter)

outputs=[]
labels=[]
with torch.no_grad():
  for data in test_loader:
    xtest=data['x']
    ytest=data['y']
    output=model(xtest,W,b)
    labels.append(ytest)
    outputs.append(output)

metrics.roc_auc_score(torch.cat(labels).view(-1), torch.cat(outputs).view(-1))
