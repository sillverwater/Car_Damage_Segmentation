import random

import torch
import cv2
import os
from src.Models import Unet
import numpy as np

os.environ['KMP_DUPLICATE_LIB_OK']='True'

def main(user_img):
    labels = ['Breakage_3', 'Crushed_2', 'Seperated_1', 'Scratch_0']
    models = []

    n_classes = 2
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    for label in labels:
        model_path = f'models/[DAMAGE][{label}]Unet.pt'

        model = Unet(encoder='resnet34', pre_weight='imagenet', num_classes=n_classes).to(device)
        model.model.load_state_dict(torch.load(model_path, map_location=torch.device(device)))
        model.eval()

        models.append(model)

    img_path = './static/images/' + user_img

    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (256, 256))

    img_input = img / 255.
    img_input = img_input.transpose([2, 0, 1])
    img_input = torch.tensor(img_input).float().to(device)
    img_input = img_input.unsqueeze(0)

    outputs = []
    output_path = []
    img_output_list =[]

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    for i, model in enumerate(models):
        output = model(img_input)

        img_output = torch.argmax(output, dim=1).detach().cpu().numpy()
        img_output = img_output.transpose([1, 2, 0])

        outputs.append(img_output)

    for i, label in enumerate(labels):
        area = outputs[i].sum()
        print(f'{label}: {area}')

        if (area!=0):
            img_output_ = ((outputs[i] - outputs[i].min()) * (1 / (outputs[i].max() - outputs[i].min()) * 255)).astype(
                'uint8')

            cv2.imwrite('./static/result/' + label + '.jpg', img_output_)

            h, w = img.shape[:2]
            dst = np.zeros((h, w, 3), np.uint8)

            contours, hierachy = cv2.findContours(img_output_, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                hull = cv2.convexHull(cnt)  # convex hull 추출
                line_img = cv2.drawContours(dst, [hull], -1, (0, 0, 255), 2)

            final_img = cv2.add(img, line_img)
            output_path.append('./result/' + label + '_' + user_img)
            cv2.imwrite('./static' + output_path[i], final_img)


        else:
            cv2.imwrite('./static/result/' + label + '.jpg', img_output)

            img_final = img
            output_path.append('./result/' + label + '_' + user_img)
            cv2.imwrite('./static' + output_path[i], img_final)

    return output_path

if __name__ == "__main__":
    main()
