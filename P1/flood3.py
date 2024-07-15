import pandas as pd
import matplotlib.pyplot as plt
import pyreadr
import numpy as np
import time

directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
# also works for RData
result = pyreadr.read_r(r"C:\Users\mathi\OneDrive\Documents\Studia\SGH\R\P1\maze.RDS")

# done!
# result is a dictionary where keys are the name of objects and the values python
# objects. In the case of Rds there is only one object with None as key
df = result[None]  # extract the pandas data frame

x1 = []
x2 = []
y1 = []
y2 = []

for x in df.columns.tolist():
    for y in df[x].index.tolist():
        if df[x][y]:
            x1.append(x)
            y1.append(y)
        else:
            x2.append(x)
            y2.append(y)

x_min = min(x2)
x_max = max(x2)
y_min = min(y2)
y_max = max(y2)

df_numpy = df.to_numpy()
numeric_data = df_numpy.astype(int)
num_rows, num_columns = numeric_data.shape
numeric_data[x_min, y_min] = 2

# Turn on interactive mode
fig, ax = plt.subplots()
img = ax.imshow(numeric_data, cmap='viridis', interpolation='nearest', vmin=0, vmax=3)

cbar = plt.colorbar(img, ax=ax, ticks=[0, 1, 2, 3], label='Value')

a = 0
plt.ion()
start = time.time()
coordinates1 = np.where(numeric_data == 0)
while True:
    now = time.time()
    data_old = np.copy(numeric_data)
    coordinates = np.where(numeric_data == 2)
    #numeric_data[numeric_data == 2] = 3
    rows = coordinates[0]
    cols = coordinates[1]

    # Iterate through each cell and check if its neighbours have been filled. If not shoot a laser in that direction
    for row, col in zip(rows, cols):
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if y_min-1 <= row+direction[0] <= y_max+1 and x_min-1 <= col+direction[1] <= x_max+1:
                n_val = numeric_data[row+direction[0], col+direction[1]]
                if n_val == 1:
                    numeric_data[row+direction[0], col+direction[1]] = 2
                    try:
                        row_min = min(np.where(coordinates1[0] > row)[0])
                    except:
                        row_min = row
                    try:
                        row_max = max(np.where(coordinates1[0] < row)[0])
                    except:
                        row_max = row
                    try:
                        col_min = min(np.where(coordinates1[1] > col)[0])
                    except:
                        col_min = col
                    try:
                        col_max = max(np.where(coordinates1[1] < col)[0])
                    except:
                        col_max = col
                    #print(row_min,row_max,col_min ,col_max)
                    numeric_data[row, col_min:col_max] = 2
                    numeric_data[row_min:row_max, col] = 2

    img.set_array(numeric_data)
    fig.canvas.draw()
    fig.canvas.flush_events()

    if np.array_equal(data_old, numeric_data):
        break
    end_loop = time.time()

    a += 1
    print(a, f'{(now-start)//60} m {round((now-start)%60,1)} s', round(end_loop-now, 3))
plt.ioff()
plt.show()
