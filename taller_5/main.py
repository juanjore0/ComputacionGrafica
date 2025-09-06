import numpy as np

#1. Cree el siguiente vector A= [2, 3,5, 1, 4 ,7 9, 8, 6, 10] 
A = np.array([2, 3, 5, 1, 4, 7, 9, 8, 6, 10])
print("Vector A:", A)

#2. Cree un vector B que contenga los elementos desde el 11 hasta el 20
B = np.arange(11, 21)
print("Vector B:", B)

#3. Componer un vector C formado por los vectores A y B en la misma fila respectivamente 
C = np.concatenate((A, B))
print("Vector C (A concatenado con B):", C)

#4. valor mínimo en el vector C 
min_value = np.min(C)
print("Valor mínimo en el vector C:", min_value)

#5. valor máximo en el vector C
max_value = np.max(C)
print("Valor máximo en el vector C:", max_value)

#6. Longitud del vector C
length_C = np.size(C)
print("Longitud del vector C:", length_C)

#7. Promedio del vector C usando sumas y divisiones
sum_C = np.sum(C)
average_C = sum_C / length_C
print("Promedio del vector C:", average_C)

#8. Promedio del vector C
average_C_np = np.mean(C)
print("Promedio del vector C (usando np.mean):", average_C_np)

#9. Mediana del vector C
median_C = np.median(C)
print("Mediana del vector C:", median_C)

#10. Suma del vector C
sum_C_np = np.sum(C)
print("Suma del vector C:", sum_C_np)

#11. Vector D (elementos > 5)
D = C[C > 5]

#12. Vector E (elementos >5 y <15)
E = C[(C > 5) & (C < 15)]

#13. Cambiar 5 y 15 por 7
print("Vector C original:", C)
C_modified = np.where((C == 5) | (C == 15), 7, C)
print("Vector C modificado (5 y 15 cambiados por 7):", C_modified)

#14. Moda del vector C
valores, conteos = np.unique(C, return_counts=True)
indice_moda = np.argmax(conteos)   # posición del valor más repetido
moda = valores[indice_moda]
print("Moda:", moda, "Frecuencia:", conteos[indice_moda])

#15. Ordenar el vector C de forma ascendente
C_sorted = np.sort(C)
print("Vector C ordenado de forma ascendente:", C_sorted)

#16. Multiplicar el vector C por 10
C_multiplied = C * 10
print("Vector C multiplicado por 10:", C_multiplied)

#17. Cambiar elementos del 6 al 8 (índices 5:8)
C_multiplied[5:8] = [60, 70, 80]
print("Vector C:", C_multiplied)

#18. Cambiar elementos del 14 al 16 (índices 13:16)
C_multiplied[13:16] = [140, 150, 160]
print("Vector C:", C_multiplied)