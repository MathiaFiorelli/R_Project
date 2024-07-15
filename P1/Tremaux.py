import pandas as pd
import matplotlib.pyplot as plt
import pyreadr
import numpy as np

destination = {'x': (387, 413), 'y': (322, 348)}

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
fig, axes = plt.subplots(figsize=(10, 10), dpi=300, layout='constrained')
plt.style.use('ggplot')
axes.scatter([x for x in x1 if x >= x_min-1 and x <= x_max+1],
             [x for x in y1 if x >= y_min-1 and x <= y_max+1], color='grey', marker='.', s=1)
axes.scatter(x2, y2, color='black', marker='*', s=1)


df_numpy = df.to_numpy()
numeric_data = df_numpy.astype(int)
numeric_data[numeric_data == 0] = 2
num_rows, num_columns = numeric_data.shape
#numeric_data[x_min, y_min] = 2

# Turn on interactive mode
fig, ax = plt.subplots()
img = ax.imshow(numeric_data, cmap='viridis', interpolation='nearest')

cbar = plt.colorbar(img, ax=ax, ticks=[0, 1, 2], label='Value')
cbar.set_ticklabels(['Value 0', 'Value 1', 'Value 2'])

directions = {'up': (1, 0), 'down': (-1, 0), 'right': (0, 1), 'left': (0, -1)}


def move(array, row, col):
    dir_ret = directions.copy()
    for d, v in directions.items():
        try:
            n_val = numeric_data[row+v[0], col+v[1]]
            dir_ret[d] = n_val
        except:
            dir_ret[d] = 2
    dir_ret = dict(sorted(dir_ret.items(), key=lambda item: item[1]))
    d = list(dir_ret.keys())[0]
    v0 = dir_ret[d]
    if v0 >= 2:
        return 'break'
    v = directions[d]
    return v


a = 0
plt.ion()
row, col = 0, 0
while True:
    print(row, col)
    a += 1
    # print(a)
    data_old = np.copy(numeric_data)
    row0, col0 = row, col
    direction = move(data_old, row, col)
    if direction == 'break':
        break
    numeric_data[row, col] = numeric_data[row, col]+1
    row = row+direction[0]
    col = col+direction[1]

    img.set_array(numeric_data)
    fig.canvas.draw()
    fig.canvas.flush_events()
    # plt.pause(0.5)

    if np.array_equal(data_old, numeric_data) or (min(destination['y']) < row < max(destination['y'])
                                                  and min(destination['x']) < col < max(destination['x'])):
        break
plt.ioff()
plt.show()
