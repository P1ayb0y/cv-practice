import numpy as np
from pylab import *
from PIL import Image
import cv2 as cv

def AddNoise(src, dst, probility = 0.01, method = "salt_pepper"):
    img=Image.open(src)
    img=img.convert('L')
    imarray = np.array(img)
    height, width = imarray.shape
    for i in range(height):
        for j in range(width):
            if np.random.random(1) < probility:
                if np.random.random(1) < 0.5:
                    imarray[i, j] = 0
                else:
                    imarray[i, j] = 255
    new_im = Image.fromarray(imarray)
    new_im.save(dst)



def medfilt(x1,h,w):
    x=x1.copy()
    row=x.shape[0]
    col=x.shape[1]
    new_row = int(floor(h/2))
    new_col = int(floor(w/2))
    for i in range(row):
        if i+h>=row+1:
            break
        for j in range(col):
            if j+w>=col+1:
                break
            y=x1[i:(i+h),j:(j+w)]
            med=np.median(y,axis=None)
            x[new_row,new_col]=med
            new_col+=1
            j=j+1
        j=0
        i=i+1
        new_row += 1
        new_col = int(floor(w / 2))
    return x


def meanfilt(x,h,w):
    y=x.copy()
    row = y.shape[0]
    col = y.shape[1]
    new_row = int(floor(h / 2))
    new_col = int(floor(w / 2))
    for i in range(row):
        if i+h>=row+1:
            break
        for j in range(col):
            if j+w>=col+1:
                break
            x1=x[i:(i+h),j:(j+w)]
            mean=round(sum(x1)/(w*h))
            y[new_row,new_col]=mean
            new_col += 1
            j=j+1
        j=0
        i=i+1
        new_row += 1
        new_col = int(floor(w / 2))
    return y

def sharpening(img,model):
    y = img.copy()
    row = y.shape[0]
    col = y.shape[1]
    grad_array=np.zeros((row,col))
    new_row = int(floor(3 / 2))
    new_col = int(floor(3 / 2))
    if model=="laplace":
        mask=np.array([[0,-1,0],[-1,4,-1],[0,-1,0]])
        for i in range(row):
            if i + 3 >= row + 1:
                break
            for j in range(col):
                if j + 3 >= col + 1:
                    break
                x1 = img[i:(i + 3), j:(j + 3)]
                grad=sum((x1*mask))
                grad_array[new_row, new_col] = grad
                new_col += 1
                j = j + 1
            j = 0
            i = i + 1
            new_row += 1
            new_col = int(floor(3 / 2))
        final_array=grad_array+y
        final_array[final_array>255]=255
        final_array[final_array<0]=0
        return final_array
    if model=="prewitt":
        mask_x=np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
        mask_y=np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
        for i in range(row):
            if i + 3 >= row + 1:
                break
            for j in range(col):
                if j + 3 >= col + 1:
                    break
                x1 =img[i:(i + 3), j:(j + 3)]
                grad=sum(x1*mask_x+x1*mask_y)
                grad_array[new_row, new_col] = grad
                new_col += 1
                j = j + 1
            j = 0
            i = i + 1
            new_row += 1
            new_col = int(floor(3 / 2))
        final_array = grad_array + y
        final_array[final_array > 255] = 255
        final_array[final_array < 0] = 0
        return final_array



# AddNoise('C:\\Users\\31495\\Desktop\\vn.jpg','C:\\Users\\31495\\Desktop\\vn2.jpg')
im_or = Image.open('C:\\Users\\31495\\Desktop\\vn2.jpg')
im_or.show()
im_array=array(im_or)
im_array_medfilt=meanfilt(im_array,3,3)
im0=Image.fromarray(uint8(im_array_medfilt))
im0.show()
im_array_sharpening=sharpening(im_array,model='laplace')
im=Image.fromarray(float64(im_array_sharpening))
im.show()

