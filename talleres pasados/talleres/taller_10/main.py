import numpy as np 
import matplotlib
import matplotlib.pyplot as plt

imagenTiff = np.array(plt.imread("FLIR_00088.tiff"))
D = np.double(imagenTiff)
temMin = -40
temMax = 160
nBits = 14
matrizCentrigrados = np.array((temMax - temMin)*D/2**nBits+temMin)

fig = plt.figure("Imagen Termografica")
plt.imshow(matrizCentrigrados, cmap=plt.cm.hot_r)

plt.colorbar(shrink=.92)
plt.figure("Histograma")
hist, bins = np.histogram(matrizCentrigrados, np.arange(0, temMax), density=True)

histogramaTemperaturaBar = np.int32(matrizCentrigrados.round())
plt.hist(histogramaTemperaturaBar, 5, facecolor='red', alpha=0.5)
plt.show()