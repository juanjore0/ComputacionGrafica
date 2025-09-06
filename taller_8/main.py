import numpy as np
import matplotlib.pyplot as plt
matriz=np.zeros((3,3,3))

print(matriz)
matriz[0,0,1]=matriz[0,0,2]=1 #cyan
matriz[0,1,0]=matriz[0,1,1]=matriz[0,1,2]=1 #blanco
matriz[0,2,0]=1 #rojo

matriz[1,0,0]=matriz[1,0,2]=1 #magenta
matriz[1,1,0]=matriz[1,1,1]=matriz[1,1,2]=0.5 #gris
matriz[1,2,1]=1 #verde

matriz[2,0,0]=matriz[2,0,1]=1 #amarillo
#negro
matriz[2,2,2]=1 #azul






plt.imshow(matriz)
plt.show()