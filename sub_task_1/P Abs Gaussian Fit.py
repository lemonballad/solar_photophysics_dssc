#import matplotlib.pyplot as plt
#import numpy as np

#A1 = 0.227554
#A2 = 0.290196
#A3 = 0.201763
#v1 = 877**2
#v2 = 692**2
#v3 = 4320**2
#c1 = 23200
#c2 = 21700
#c3 = 25000

#w = np.arange(0,3e4,20)
#g1 = A1 * np.exp(-(w - c1)**2 / 2 / v1)
#g2 = A2 * np.exp(-(w - c2)**2 / 2 / v2)
#g3 = A3 * np.exp(-(w - c3)**2 / 2 / v3)

#FIT_R = g1 + g2 + g3
#FIT_L = FIT_R[::-1]
#FIT = np.concatenate((FIT_L,FIT_R[1:]))
#w = np.concatenate((-w[::-1],w[1:]))

##plt.figure(0)
##plt.plot(w,FIT,'k-')
##plt.show()

#tFIT = np.abs(np.fft.ifft(np.fft.ifftshift(FIT),norm='ortho'))
#tFIT = tFIT / tFIT[0]

#c = 3e-5
#nw = np.size(w,0)
#dw = np.sum(np.diff(w))/(nw-1)
#dt = 1/dw/c
#nt = nw
#t = np.arange(0,dt*(nt-1/2),dt)

#plt.figure(1)
#plt.plot(t,tFIT,'k-')
#plt.plot((t[0],t[-1]),(np.exp(-1),np.exp(-1)),'b:')
#plt.plot(t,np.exp(-t/5000),'r--')
#plt.xlim([0,5e4])
#plt.show()