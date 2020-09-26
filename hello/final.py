#the images generated are sent with this file please go through them as well


#conversion to halftone

import sys

from PIL import Image
from random import randint 
# Open an Image
def open_image(path):
  newImage = Image.open(path)
  return newImage

# Save Image
def save_image(image, path):
  image.save(path, 'png')


# Create a new image with the given size
def create_image(i, j):
  image = Image.new("RGB", (i, j), "white")
  return image


# Get the pixel from the given image
def get_pixel(image, i, j):
  # Inside image bounds?
  width, height = image.size
  if i > width or j > height:
    return None

  # Get Pixel
  pixel = image.getpixel((i, j))
  return pixel


def get_saturation(value, quadrant):
  if value > 223:
    return 255
  elif value > 159:
    if quadrant != 1:
      return 255

    return 0
  elif value > 95:
    if quadrant == 0 or quadrant == 3:
      return 255

    return 0
  elif value > 32:
    if quadrant == 1:
      return 255

    return 0
  else:
    return 0


# Create a dithered version of the image
def convert_dithering(image):
  # Get size
  width, height = image.size
  print(width,height)

  # Create new Image and a Pixel Map
  new = create_image(width, height)
  pixels = new.load()

  # Transform to half tones
  for i in range(0, width, 2):
    for j in range(0, height, 2):
      # Get Pixels
      p1 = get_pixel(image, i, j)
      try:
        p2 = get_pixel(image, i, j + 1)
        p3 = get_pixel(image, i + 1, j)
        p4 = get_pixel(image, i + 1, j + 1)
      except:
        p2= get_pixel(image, i,j)
        p3= get_pixel(image, i,j)
        p4= get_pixel(image, i,j)

      # Color Saturation by RGB channel
      red   = (p1[0] + p2[0] + p3[0] + p4[0]) / 4
      green = (p1[1] + p2[1] + p3[1] + p4[1]) / 4
      blue  = (p1[2] + p2[2] + p3[2] + p4[2]) / 4

      # Results by channel
      r = [0, 0, 0, 0]
      g = [0, 0, 0, 0]
      b = [0, 0, 0, 0]

      # Get Quadrant Color
      for x in range(0, 4):
        r[x] = get_saturation(red, x)
        g[x] = get_saturation(green, x)
        b[x] = get_saturation(blue, x)

      # Set Dithered Colors
      pixels[i, j] = (r[0], g[0], b[0])
      try:
        pixels[i, j + 1] = (r[1], g[1], b[1])
      except:
        pass
      try:
        pixels[i + 1, j] = (r[2], g[2], b[2])
      except:
        pass
      try:
        pixels[i + 1, j + 1] = (r[3], g[3], b[3])
      except:
        pass

  # Return new image
  return new



  # Load Image (JPEG/JPG needs libjpeg to load)
filename=str(sys.argv[1])
print(filename)
original = open_image(filename)
print("generating half tone")
# Convert to Dithering and save
new = convert_dithering(original)
halftonefilename="halftone"+filename
save_image(new, halftonefilename)



# updated dither
from PIL import Image

img1 = Image.open(halftonefilename)
data = img1.getdata()

img2 = Image.open(halftonefilename)

img3 = Image.open(halftonefilename)




r = [(d[0], 0, 0) for d in data]
g = [(0, d[1], 0) for d in data]
b = [(0, 0, d[2]) for d in data]

print("spliting")
img1.putdata(r)


redfilename="red"+filename
bluefilename="blue"+filename
greenfilename="green"+filename
img1.save(redfilename)


img2.putdata(g)
img2.save(greenfilename)


img3.putdata(b)
img3.save(bluefilename)





#generation of mask even lines 1 odd lines 0

width,height=img1.size


#mask
li=[]
lic=[]
for i in range(0,height,2):
    l1=[]
    l2=[]
    l1c=[]
    l2c=[]
    for j in range(width):
        v1=randint(0,1)
        if(v1==0):
            l1.append([0,0,0])
            l2.append([255,255,255])
            
            l1c.append([0,0,0])
            l2c.append([255,255,255])
        else:
            l1.append([255,255,255])
            l2.append([0,0,0])
            l2c.append([0,0,0])
            l1c.append([255,255,255])
    li.append(l1)
    lic.append(l1c)
    lic.append(l2c)
    li.append(l2)

#generating mask image
print("generating mask")
new2 = create_image(width, height)
for i in range(height):
    for j in range(width):
        if li[i][j]==1:
            new2.putpixel((j,i),(255,255,255))
        else:
            new2.putpixel((j,i),(0,0,0))


maskfilename="mask"+filename
save_image(new2,maskfilename)


#creating array of RGB channel images where 1 means pixel is red and 0 -> black 

colourr=[] 	# 2D list of colour pixels of red channel image 
colourg=[]
colourb=[]
co=0
for i in range(height):
    lir=[]
    lib=[]
    lig=[]
    for j in range(width):
        r1,_,_=get_pixel(img1, j, i)
        _,g1,_=get_pixel(img2, j, i)
        _,_,b1=get_pixel(img3, j, i)
        lir.append(r1)
        lig.append(g1)
        lib.append(b1)

    colourr.append(lir)
    
    colourg.append(lig)
    colourb.append(lib)
    
print(co)
def bin(a,b):
    for i in range(8):
        a[7-i]=b%2
        b=b//2
def dec(a):
    x=a[7]+a[6]*2**1+a[5]*2**2+a[4]*2**3+a[3]*2**4+a[2]*2**5+a[1]*2**6+a[0]*2**7
    return x


#encryption
mask=li
maskc=lic
print("encrypting image");
encryptr = create_image(width, height)
encryptg = create_image(width, height)
encryptb = create_image(width, height)
height2=0
if height%2==0:
    height2=height
else:
    height2=height-1

def createencryptr(encryptr,v,colourr):
    mask2 = open_image(maskfilename)
    co=0
    for i in range(width):
        for j in range(int(height2/2)):
            temp=j
            j=j*2
            imgb0=colourr[j][i]
            imgb1=colourr[j+1][i]
            maskv1=mask[j][i][0]
            maskv2=mask[j+1][i][0]
            aimgb0=[0]*8
            aimgb1=[0]*8
            amaskv1=[0]*8
            amaskv2=[0]*8
            bin(aimgb0,imgb0)
            bin(aimgb1,imgb1)
            bin(amaskv1,maskv1)
            bin(amaskv2,maskv2)
            aenc1=[0]*8
            aenc2=[0]*8
            cou=0
            for ik in range(8):
                if aimgb0[ik] ==0 and aimgb0[ik]==0:
                    if amaskv1[ik]==0:
                        aenc1[ik]=1
                        aenc2[ik]=0
                    else:
                        aenc2[ik]=1
                        aenc1[ik]=0
                elif aimgb1[ik] ==1 and aimgb1[ik]==1:
                    aenc1[ik]=amaskv1[ik]
                    aenc2[ik]=amaskv2[ik]
                else:
                    amaskv1[ik]=aimgb0[ik]
                    amaskv2[ik]=aimgb1[ik]
                    aenc1[ik]=amaskv1[ik]
                    aenc2[ik]=amaskv2[ik]
                    cou+=1
            if cou>0:
                maskc[j][i][0]=dec(amaskv1)
                maskc[j+1][i][0]=dec(amaskv2)
            encryptr.putpixel((i,j),(dec(aenc1),0,0))
            encryptr.putpixel((i,j+1),(dec(aenc2),0,0))
            mask2.putpixel((i,j+1),(dec(amaskv2),dec(amaskv2),dec(amaskv2)))
            mask2.putpixel((i,j),(dec(amaskv1),dec(amaskv1),dec(amaskv1)))

def createencryptg(encryptr,v,colourr):
    mask2 = open_image(maskfilename)
    co=0
    for i in range(width):
        for j in range(int(height2/2)):
            temp=j
            j=j*2
            imgb0=colourr[j][i]
            imgb1=colourr[j+1][i]
            maskv1=mask[j][i][1]
            maskv2=mask[j+1][i][1]
            aimgb0=[0]*8
            aimgb1=[0]*8
            amaskv1=[0]*8
            amaskv2=[0]*8
            bin(aimgb0,imgb0)
            bin(aimgb1,imgb1)
            bin(amaskv1,maskv1)
            bin(amaskv2,maskv2)
            aenc1=[0]*8
            aenc2=[0]*8
            cou=0
            for ik in range(8):
                if aimgb0[ik] ==0 and aimgb0[ik]==0:
                    if amaskv1[ik]==0:
                        aenc1[ik]=1
                        aenc2[ik]=0
                    else:
                        aenc2[ik]=1
                        aenc1[ik]=0
                elif aimgb1[ik] ==1 and aimgb1[ik]==1:
                    aenc1[ik]=amaskv1[ik]
                    aenc2[ik]=amaskv2[ik]
                else:
                    amaskv1[ik]=aimgb0[ik]
                    amaskv2[ik]=aimgb1[ik]
                    aenc1[ik]=amaskv1[ik]
                    aenc2[ik]=amaskv2[ik]
                    cou+=1
            if cou>0:
                maskc[j][i][1]=dec(amaskv1)
                maskc[j+1][i][1]=dec(amaskv2)
            encryptr.putpixel((i,j),(0,dec(aenc1),0))
            encryptr.putpixel((i,j+1),(0,dec(aenc2),0))
            mask2.putpixel((i,j+1),(dec(amaskv2),dec(amaskv2),dec(amaskv2)))
            mask2.putpixel((i,j),(dec(amaskv1),dec(amaskv1),dec(amaskv1)))
                              

def createencryptb(encryptr,v,colourr):
    mask2 = open_image(maskfilename)
    co=0
    for i in range(width):
        for j in range(int(height2/2)):
            temp=j
            j=j*2
            imgb0=colourr[j][i]
            imgb1=colourr[j+1][i]
            maskv1=mask[j][i][2]
            maskv2=mask[j+1][i][2]
            aimgb0=[0]*8
            aimgb1=[0]*8
            amaskv1=[0]*8
            amaskv2=[0]*8
            bin(aimgb0,imgb0)
            bin(aimgb1,imgb1)
            bin(amaskv1,maskv1)
            bin(amaskv2,maskv2)
            aenc1=[0]*8
            aenc2=[0]*8
            cou=0
            for ik in range(8):
                if aimgb0[ik] ==0 and aimgb0[ik]==0:
                    if amaskv1[ik]==0:
                        aenc1[ik]=1
                        aenc2[ik]=0
                    else:
                        aenc2[ik]=1
                        aenc1[ik]=0
                elif aimgb1[ik] ==1 and aimgb1[ik]==1:
                    aenc1[ik]=amaskv1[ik]
                    aenc2[ik]=amaskv2[ik]
                else:
                    amaskv1[ik]=aimgb0[ik]
                    amaskv2[ik]=aimgb1[ik]
                    aenc1[ik]=amaskv1[ik]
                    aenc2[ik]=amaskv2[ik]
                    cou+=1
            if cou>0:
                maskc[j][i][2]=dec(amaskv1)
                maskc[j+1][i][2]=dec(amaskv2)
            encryptr.putpixel((i,j),(0,0,dec(aenc1)))
            encryptr.putpixel((i,j+1),(0,0,dec(aenc2)))
            mask2.putpixel((i,j+1),(dec(amaskv2),dec(amaskv2),dec(amaskv2)))
            mask2.putpixel((i,j),(dec(amaskv1),dec(amaskv1),dec(amaskv1)))
            

            j=temp
    maskcfilename="maskc"+filename


    save_image(mask2, maskcfilename)


v=(255,0,0)
createencryptr(encryptr,v,colourr)

encryptrfilename="encryptr"+filename
save_image(encryptr, encryptrfilename)
v=(0,255,0)
encryptgfilename="encryptg"+filename
createencryptg(encryptg,v,colourg)
save_image(encryptg, encryptgfilename)
v=(0,0,255)
encryptbfilename="encryptb"+filename
createencryptb(encryptb,v,colourb)
save_image(encryptb, encryptbfilename)



encryptf = create_image(width, height)
for i in range(width):
    for j in range(height):
        r1,_,_=get_pixel(encryptr, i, j)
        _,g1,_=get_pixel(encryptg, i, j)
        _,_,b1=get_pixel(encryptb, i, j)
        encryptf.putpixel((i,j),(r1,g1,b1))


encryptffilename="encryptf"+filename
save_image(encryptf, encryptffilename)



imger=Image.open(encryptrfilename)
imgeg=Image.open(encryptgfilename)
imgeb=Image.open(encryptbfilename)


decryptr = create_image(width, height)
decryptg = create_image(width, height)
decryptb = create_image(width, height)
dcr=[]
dcg=[]
dcb=[]

for i in range(height):
    lir=[]
    lib=[]
    lig=[]
    for j in range(width):
        r1,_,_=get_pixel(imger, j, i)
       
        _,g1,_=get_pixel(imgeg, j, i)
        _,_,b1=get_pixel(imgeb, j, i)
        
        if(r1==255):
            lir.append(255)
        else:
            lir.append(0)
        if(g1==255):
            lig.append(255)
        else:
            lig.append(0)
        if(b1==255):
            lib.append(255)
        else:
            lib.append(0)
    dcr.append(lir)
    
    dcg.append(lig)
    dcb.append(lib)

#writing the decrypter function 




height2=0
if height%2==0:
    height2=height
else:
    height2=height-1

lo=55
hi=255


def createdecryptnr(decrypt,dcr,v,mi):
    for i in range(width):
        for j in range(int(height2/2)):
            temp=j
            j=j*2
            mb0=dcr[j][i]
            mb1=dcr[j+1][i]
            maska1=mask[j][i][mi]
            maska2=mask[j+1][i][mi]
            maskc1=maskc[j][i][mi]
            maskc2=maskc[j+1][i][mi]
            if maska1==maskc1:
                if maska1==mb0:
                    decrypt.putpixel((i,j),v)
                    decrypt.putpixel((i,j+1),v)
                else:
                    decrypt.putpixel((i,j),(0,0,0))
                    decrypt.putpixel((i,j+1),(0,0,0))
            else:
                if maska1>0:
                    decrypt.putpixel((i,j),v)
                    decrypt.putpixel((i,j+1),(0,0,0))
                else:
                    
                    decrypt.putpixel((i,j),(0,0,0))
                    decrypt.putpixel((i,j+1),v)



v=(255,0,0)
print("generating decrypted image")
createdecryptnr(decryptr,dcr,v,0)

decryptrfilename="decryptr"+filename

decryptgfilename="decryptg"+filename

decryptbfilename="decryptb"+filename

save_image(decryptr, decryptrfilename)
v=(0,255,0)
createdecryptnr(decryptg,dcg,v,1)
save_image(decryptg, decryptgfilename)
v=(0,0,255)
createdecryptnr(decryptb,dcb,v,2)
save_image(decryptb, decryptbfilename)

#again mering/ overlaping these images with the same method 


decryptf = create_image(width, height)
for i in range(width):
    for j in range(height):
        r1,_,_=get_pixel(decryptr, i, j)
        _,g1,_=get_pixel(decryptg, i, j)
        _,_,b1=get_pixel(decryptb, i, j)
        decryptf.putpixel((i,j),(r1,g1,b1))
print("merging decrypted image")
decrfilename="decrypt"+filename
save_image(decryptf, decrfilename)


