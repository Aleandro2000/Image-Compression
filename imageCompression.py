#Realized by Alexandru-Andrei Carmici and Mihai Necula

import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import svd
from PIL import Image
from ipywidgets import interact, interactive, interact_manual
import ipywidgets as widgets
from IPython.display import display
import os
from os import path
import random

def compress_image(img_name, k):
    print("Processing...")
    global compressed_image
    img = images[img_name]

    r = img[:,:,0]
    g = img[:,:,1]
    b = img[:,:,2]

    print("Compressing...")
    ur,sr,vr = svd(r, full_matrices=False)
    ug,sg,vg = svd(g, full_matrices=False)
    ub,sb,vb = svd(b, full_matrices=False)
    rr = np.dot(ur[:,:k],np.dot(np.diag(sr[:k]), vr[:k,:]))
    rg = np.dot(ug[:,:k],np.dot(np.diag(sg[:k]), vg[:k,:]))
    rb = np.dot(ub[:,:k],np.dot(np.diag(sb[:k]), vb[:k,:]))

    print("Arranging...")
    rimg = np.zeros(img.shape)
    rimg[:,:,0] = rr
    rimg[:,:,1] = rg
    rimg[:,:,2] = rb

    for ind1, row in enumerate(rimg):
        for ind2, col in enumerate(row):
            for ind3, value in enumerate(col):
                if value < 0:
                    rimg[ind1,ind2,ind3] = abs(value)
                if value > 255:
                    rimg[ind1,ind2,ind3] = 255

    compressed_image = rimg.astype(np.uint8)
    plt.title("Image Name: "+img_name+"\n")
    plt.imshow(compressed_image)
    plt.axis('off')
    plt.show()
    compressed_image = Image.fromarray(compressed_image)

random.seed(0)

open=True

while open==True:

    name=input("Enter the image name with its extension: ")

    if name=="":
        exit(1)
    elif path.exists(name)==False:
        print("\nERROR! FILE DOES NOT EXIST OR IS ANOTHER FORMAT THAN PNG!\nDo you want to exit? Write EXIT if you want!\n")
        if input()=="EXIT":
            open=False
        else:
            os.system("@cls||clear")
        continue

    images = {
        "image": np.asarray(Image.open(name))
    }

    def show_images(img_name):
        'It will show image in widgets!'
        print("Loading...")
        plt.title("Close this plot to open compressed image...")
        plt.imshow(images[img_name])
        plt.axis('off')
        plt.show()

    show_images('image')
    compressed_image = None

    sigma = random.randrange(0,20)

    print("Sigma: ",sigma)

    compress_image("image", sigma)

    compressed_image.save("compressed_image.png")
    print("DONE!\n\nType EXIT to exit if you want!\n")
    
    if input()=="EXIT":
        open=False
    else:
        os.system("@cls||clear")