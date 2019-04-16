#!/usr/bin/python 
# -*- coding: utf-8 -*- 
"""
File : tr_SFF.py 
code author : DoranLyong 
email : cheeryun@gmail.com 
"""

import numpy as np 
import scipy.io as sio     # Load MATLAB files 
from scipy import ndimage, misc
from skimage.viewer import ImageViewer
import matplotlib.pyplot as plt 
from mpl_toolkits import mplot3d  
import cv2


def load_matdata():
    mat_contents = sio.loadmat('./images/xsin.mat')
    print(type(mat_contents))
    print(mat_contents)
    img_stack = mat_contents['x']

    return img_stack

def imshow(img_stack):
    print("stack_length = ", len(img_stack[1,1,:]))
    viewer = ImageViewer(img_stack[:,:,50])
    viewer.show()

def ML(img):
    row, col = img.shape
    ml = np.zeros((row, col), dtype=float)

    for i in range(4, row-3,1 ):
        for j in range(4, col-3, 1):
            ml[i,j] =  abs(2*img[i,j] - img[i-1,j] - img[i+1, j]) + abs(2*img[i,j] - img[i, j-1] - img[i,j+1])   
           
    return ml
    
def SML(ML):
    row, col = ML.shape 
    SML = np.zeros((row, col), dtype=float )

    for i in range(4, row-3,1 ):
        for j in range(4, col-3, 1):
            for m in range(-1,1,1):
                for n in range(-1,1,1):
                    SML[i,j] = SML[i,j] + ML[i+m, j+n]                  
    return SML



def meshgrid(mesh):
    x, y = mesh.shape 

    x = np.linspace(0, x, x)
    y = np.linspace(0, y, y)

    X, Y = np.meshgrid(x, y)
    
    fig = plt.figure()
    ax   = plt.axes( projection = '3d')
    ax.plot_surface(X, Y, mesh, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    plt.show()



def main():
    img_stack = load_matdata()
    row, col, h = img_stack.shape 
    
    #imshow(img_stack)
  
    focus_stack = np.zeros((row, col,h), dtype=float )
    for k in range(h):
        #focus_stack[:,:,k] = cv2.Laplacian(img_stack[:,:,k],cv2.CV_64F) 
        focus_stack[:,:,k] = ML(img_stack[:,:,k]) 
        focus_stack[:,:,k] = SML(focus_stack[:,:,k]) 
        print("count: ", k)   
  
    print("Focus_stack= ",focus_stack )

    shape = focus_stack.argmax(axis=2)
    print(shape.shape)
    #print(focus_stack.shape)

    meshgrid(shape)
    
    print("Done!")
    print(shape)


if __name__ == "__main__":
    main()