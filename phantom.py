from phantominator import shepp_logan
from matplotlib import pyplot as plt
import numpy as np
import pynufft as pnft



#create the shepp_logan phantom
ph = shepp_logan(16)

for i in range(8):
	ph[:,i]= [1]*16

for i in range(8,16):
	ph[:,i]= [0.5]*16	

plt.title('phantom'), plt.xticks([]), plt.yticks([])
plt.imshow(ph, cmap = 'gray')
plt.show()


#function that draws the k-space under the effect of the non-uniform B0
def non_uniform_kspace(phantom):
    NufftObj = pnft.NUFFT()
    Nd = (phantom.shape[0], phantom.shape[1])
    Kd = (2 * phantom.shape[0], 2 * phantom.shape[1])
    Jd = (6, 6)
    om = np.random.randn(15120, 3)
    NufftObj.plan(om, Nd, Kd, Jd)
    x = NufftObj.forward(phantom)
    Data = NufftObj.solve(x, solver='cg', maxiter=50)
    k = np.fft.fft2(Data)
    k_space = (np.fft.fftshift(k)) / np.sqrt(k)
    plt.title('Non-uniform K-Space of The phantom'), plt.xticks([]), plt.yticks([])
    plt.imshow(20 * np.log(np.abs(k_space)), cmap='gray')
    plt.show()


#function that draws the k-space under the effect of the uniform B0

def uniform_kspace(img):
	img = np.fft.ifftshift(img)
	FFT = np.fft.fft2(img)
	FFT_shift = np.fft.fftshift(FFT)
	FFT_shift=np.fft.fftshift(FFT)
	FFT_abs=(np.abs(FFT_shift))
	plt.imshow(FFT_abs,cmap = 'gray')
	plt.title('uniform K-Space of The phantom'), plt.xticks([]), plt.yticks([])
	plt.show()
	return FFT_shift



def inverse_kspace(k):
	
	print(k)
	k = np.fft.ifft2(k)
	plt.imshow(np.abs(k),cmap = 'gray')
	plt.title('2 The phantom'), plt.xticks([]), plt.yticks([])
	plt.show()
    
non_uniform_kspace(ph)
k=uniform_kspace(ph)
inverse_kspace(k)