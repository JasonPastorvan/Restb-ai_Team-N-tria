# -*- coding: utf-8 -*-
"""Bueno.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bk9xcYgj8v-Nu1JTXZTPAZ76g1bdu2GV
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import csv

#                          ENTRENAMIENTO TRAIN.CSV
# Leer el archivo CSV
df = pd.read_csv('train.csv', header=None)  # Usa header=None si no hay encabezados

# Convertir a matriz NumPy
matriz = df.to_numpy()

f = len(matriz)
c = len(matriz[0])

#Eliminar columnas con poca información
# Recorrer la matriz y limpiar valores
for i in range(f):  # Recorrer las filas
    for j in range(c):  # Recorrer las columnas
        try:
            # Intentar convertir el elemento a float
            valor = float(matriz[i, j])
            # Si el valor es NaN, no hacer nada
            if np.isnan(valor):
                continue
        except ValueError:
            # Si ocurre un ValueError (no es un número), se convierte a 0
            matriz[i, j] = 0
#Mirar que columnas tienen más del 70% de nan
eliminar_7 = np.array([])
for i in range(c):
  contador_nan = 0
  for j in range(f):
    if isinstance(matriz[j][i], (int, float)) and np.isnan(matriz[j][i]):
    #if np.isnan(matriz[j][i]):
      contador_nan = contador_nan + 1
  contador_nan = contador_nan / f
  #print("Contador relativo nan columna", i, ":", contador_nan, "\n")
  if contador_nan >= 0.7:
    eliminar_7 = np.append(eliminar_7, i)

#Definir vector con las columnas con datos del 1 al 6
vector_punt = np.array([2,3,4,5,6,8,9,10,11], dtype = int)

#Calculamos el promedio de los valores no nan de una característica
matriz = matriz.astype(float)
promedio = np.zeros(9)
h = 0
for i in vector_punt:
    for j in range(f):
      cont = 1
      if not np.isnan(matriz[j][i]) and matriz[j, i] != 0:
            promedio[h] = promedio[h] + matriz[j, i]
            cont = cont + 1
      promedio[h] = promedio[h] / cont
    h = h + 1
promedio_suma = np.zeros(12, dtype = float)
k = 0
for i in vector_punt:
  promedio_suma[i] = promedio[k]
  k = k + 1

#Recuperamos la matriz original
# Leer el archivo CSV
dg = pd.read_csv('train.csv', header=None)  # Usa header=None si no hay encabezados

# Convertir a matriz NumPy
matriz2 = dg.to_numpy()

fil = len(matriz2)
col = len(matriz2[0])

#ImageData.features_reso.results
utiles = np.zeros(fil, dtype = int)
for i in range(1,fil):
  #print(type(matriz2[i][7]))
  if type(matriz2[i][7]) == str:
    utiles[i] = len(matriz2[i][7])
  else:
    utiles[i] = 0
n = np.max(utiles)  # Valor máximo del rango origina
map = np.zeros(fil, dtype = float)
k = 0
for i in utiles:
  map[k] = 6 - 5 * (i / n)
  k = k + 1

#ImageData.room_type_reso.results
utiles2 = np.zeros(fil, dtype = int)
for i in range(1,fil):
  #print(type(matriz2[i][13]))
  if type(matriz2[i][13]) == str:
    utiles2[i] = len(matriz2[i][13])
  else:
    utiles2[i] = 0
n2 = np.max(utiles)  # Valor máximo del rango origina
map2 = np.zeros(fil, dtype = float)
k2 = 0
for i in utiles:
  map[k2] = 6 - 5 * (i / n2)
  k2 = k2 + 1

#Structure.YearBuilt
media3 = 0
cont3 = 0
año = np.zeros([], dtype = int)
for i in range(fil):
  if not np.isnan(matriz[i,52]) and matriz[i][52] > 1900:
    media3 = media3 + matriz[i,52]
    cont3 = cont3 + 1
    año = np.append(año, matriz[i,52])
media3 = media3 / cont3
min3 = 2024
for i in range(len(año)):
  if año[i] < min3 and año[i] > 1900:
    min3 = año[i]
map3 = np.zeros(fil, dtype = float)
for i in range(fil):
  if np.isnan(matriz[i,52]):
    matriz[i,52] = media3
    map3[i] = 6 - ((matriz[i,52] - 1900) / 124) * (6 - 1)
  elif matriz[i,52] <= 1900:
    map3[i] = 6
  else:
    map3[i] = 6 - ((matriz[i,52] - 1900) / 124) * (6 - 1)

#Listado de precios
precios = np.array([])
for i in range(1,fil):
  valor2 = float(matriz[i,18])
  if not np.isnan(valor2):
    precios = np.append(precios, valor2)
media_precios = np.mean(precios)
for i in range(1,fil):
  valor3 = float(matriz2[i,18])
  if np.isnan(valor3):
    matriz2[i,18] = media_precios
precios2 = np.array([], dtype = float)
for i in range(1,fil):
  precios2 = np.append(precios2,float(matriz[i,18]))

#Calcular la media de una vivienda
medias = np.zeros([], dtype = float)
for j in range(1,f):
  media = 0
  for k in vector_punt:
    if np.isnan(matriz[j][k]):
      matriz[j][k] = promedio_suma[k]
    media = media + matriz[j][k]
  media = media + map[j] + map2[j] + map3[j]
  media = media / (len(vector_punt) + 3)
  medias = np.append(medias,media)
min = 6
for i in range(len(medias)):
  if medias[i] < min and medias[i] > 1:
    min = medias[i]
#Regresión lineal para estimar los precios
medias_mejor = medias[1:]

a, b = np.polyfit(medias_mejor, precios2, 1)

# Generar puntos para la recta de regresión
x_recta = np.linspace(np.min(medias_mejor), np.max(medias_mejor), 100)  # Valores equiespaciados en el rango de medias
y_recta = a * x_recta + b  # Valores de Y usando la ecuación de la recta

# Graficar los datos originales (dispersión)
plt.scatter(medias_mejor, precios2, color='blue', label='Datos originales')

# Graficar la recta de regresión
plt.plot(x_recta, y_recta, color='red', label=f'Recta de regresión: Y = {a:.2f}X + {b:.2f}')

ax = plt.gca()  # Obtener el eje actual
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))  # Evitar notación científica
ax.ticklabel_format(style='plain', axis='y')  # Asegurar formato plano

# Configurar etiquetas y título
plt.xlabel('Medias de los inmuebles')
plt.ylabel('Precios($)')
plt.title('Regresión Lineal Training: Medias vs. Precios')
plt.legend()

# Mostrar el gráfico
plt.show()

#                          APLICACIÓN TEST.CSV
# Leer el archivo CSV
da = pd.read_csv('test.csv', header=None)  # Usa header=None si no hay encabezados

# Convertir a matriz NumPy
matriz5 = da.to_numpy()

f2 = len(matriz5)
c2 = len(matriz5[0])

#Eliminar columnas con poca información
# Recorrer la matriz y limpiar valores
for i in range(f2):  # Recorrer las filas
    for j in range(c2):  # Recorrer las columnas
        try:
            # Intentar convertir el elemento a float
            valor = float(matriz5[i, j])
            # Si el valor es NaN, no hacer nada
            if np.isnan(valor):
                continue
        except ValueError:
            # Si ocurre un ValueError (no es un número), se convierte a 0
            matriz5[i, j] = 0

#Calculamos el promedio de los valores no nan de una característica
matriz5 = matriz5.astype(float)
promedio = np.zeros(9)
h = 0
for i in vector_punt:
    for j in range(f2):
      cont = 1
      if not np.isnan(matriz5[j][i]) and matriz5[j, i] != 0:
            promedio[h] = promedio[h] + matriz5[j, i]
            cont = cont + 1
      promedio[h] = promedio[h] / cont
    h = h + 1
promedio_suma = np.zeros(12, dtype = float)
k = 0
for i in vector_punt:
  promedio_suma[i] = promedio[k]
  k = k + 1

#Recuperamos la matriz original
# Leer el archivo CSV
db = pd.read_csv('test.csv', header=None)  # Usa header=None si no hay encabezados

# Convertir a matriz NumPy
matriz6 = db.to_numpy()

fil2 = len(matriz6)
col2 = len(matriz6[0])

#ImageData.features_reso.results
utiles = np.zeros(fil2, dtype = int)
for i in range(1,fil2):
  if type(matriz6[i][7]) == str:
    utiles[i] = len(matriz6[i][7])
  else:
    utiles[i] = 0
n = np.max(utiles)  # Valor máximo del rango origina
map = np.zeros(fil2, dtype = float)
k = 0
for i in utiles:
  map[k] = 6 - 5 * (i / n)
  k = k + 1

#ImageData.room_type_reso.results
utiles2 = np.zeros(fil2, dtype = int)
for i in range(1,fil2):
  if type(matriz6[i][13]) == str:
    utiles2[i] = len(matriz6[i][13])
  else:
    utiles2[i] = 0
n2 = np.max(utiles)  # Valor máximo del rango origina
map2 = np.zeros(fil2, dtype = float)
k2 = 0
for i in utiles:
  map[k2] = 6 - 5 * (i / n2)
  k2 = k2 + 1

#Structure.YearBuilt
media3 = 0
cont3 = 1
año = np.zeros([], dtype = int)
for i in range(1,fil2):
  valor7 = float(matriz6[i,51])
  if not np.isnan(valor7) and valor7 > 1900:
    media3 = media3 + valor7
    cont3 = cont3 + 1
    año = np.append(año, valor7)
media3 = media3 / cont3
min3 = 2024
for i in range(len(año)):
  if año[i] < min3 and año[i] > 1900:
    min3 = año[i]
map3 = np.zeros(fil2, dtype = float)
for i in range(1,fil2):
  matriz6[i,51] = float(matriz6[i,51])
  if np.isnan(matriz6[i,51]):
    matriz6[i,51] = media3
    map3[i] = 6 - ((matriz6[i,51] - 1900) / 124) * (6 - 1)
  elif matriz6[i,51] <= 1900:
    map3[i] = 6
  else:
    map3[i] = 6 - ((matriz5[i,51] - 1900) / 124) * (6 - 1)

#Calcular la media de una vivienda
medias = np.zeros([], dtype = float)
for j in range(1,f2):
  media = 0
  for k in vector_punt:
    if np.isnan(matriz5[j][k]):
      matriz5[j][k] = promedio_suma[k]
    media = media + matriz5[j][k]
  media = media + map[j] + map2[j] + map3[j]
  media = media / (len(vector_punt) + 3)
  medias = np.append(medias,media)
medidas_mejor = medias[1:]

Precio = np.zeros(len(medidas_mejor), dtype = float)
for i in range(len(medidas_mejor)):
  Precio[i] = round(a * medidas_mejor[i] + b, 2)
df = pd.DataFrame({'Listing.ListingId': matriz6[1:,17], 'Listing.Price.ClosePrice': Precio})
df.to_csv('Resultados', index = False)
print(df)