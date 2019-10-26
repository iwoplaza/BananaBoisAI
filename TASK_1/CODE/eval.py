import os
import numpy as np
import cv2

import torch
from torch import nn, optim
from torch.autograd import Variable
from torchvision import models


from sklearn.metrics import confusion_matrix



def validation(file_path):
    """
    file_path = str(os.getcwd())[:-4] + '/DATASET/validation_small/0A8D1972C4C3830754B135FC956A5780FDF7D333.jpg'
    """

    # --------------------------------------------------------------
    ### PARAMETERS
    model_path = str(os.getcwd())[:-4] + '/MODEL/'
    device = torch.device('cpu')
    threshold = 0.8
    img_size = 200


    # --------------------------------------------------------------
    ### PREPARE AND CHECK DATA
    img = cv2.imread(file_path)
    img = cv2.resize(img, (200, 200)) / 255
    img = np.reshape(img, (1, 3, img_size, img_size)) 

    test_inputs = torch.from_numpy(img) 
    test_inputs = Variable(test_inputs.float()).to(device)
    test_inputs = test_inputs.view(test_inputs.size(0), 3, img_size, img_size)

    # --------------------------------------------------------------
    ### MODEL ARCHITECTURE
    def make_model():
        model = models.alexnet(pretrained=True)
        for param in model.parameters():
            param.requires_grad = False

        # Sequential to List
        alxlt = list(model.classifier)
        alxlt.append(nn.ReLU(inplace=True))
        alxlt.append(nn.Linear(in_features=1000, out_features=200, bias=True))
        alxlt.append(nn.ReLU(inplace=True))
        alxlt.append(nn.Linear(in_features=200, out_features=53, bias=True))
        alxlt.append((nn.Sigmoid()))

        # List to Sequential
        new_classifier = nn.Sequential(*(alxlt[x] for x in range(len(alxlt))))
                            
        model.classifier = new_classifier
        model = model.to(device)
        return model


    # --------------------------------------------------------------
    ### HELPER FUNCTION
    # probabilitites to binary values
    def prob_to_bin(outputs, threshold):
        # convert to np array
        if type(outputs) == torch.Tensor:
            outputs = (outputs.data).cpu().numpy()
        # convert probabilitites to 1 and 0
        outputs[outputs > threshold] = 1
        outputs[outputs <= threshold] = 0

        return outputs


    # --------------------------------------------------------------
    ### VALIDATION
    val_net = make_model().to(device)
    checkpoint = torch.load(f'{model_path}model_state_dict.pkl', map_location=device)
    val_net.load_state_dict(checkpoint, strict=True)

    test_outputs = val_net(test_inputs).to(device)
    test_outputs = prob_to_bin(test_outputs, threshold)

    # --------------------------------------------------------------
    ### RESULTS
    print(test_outputs)
    return test_outputs