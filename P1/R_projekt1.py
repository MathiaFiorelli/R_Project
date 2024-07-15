import pandas as pd
import matplotlib.pyplot as plt
import pyreadr
import numpy as np
# %%


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
# %%
x_min = min(x2)
x_max = max(x2)
y_min = min(y2)
y_max = max(y2)
fig, axes = plt.subplots(figsize=(10, 10), dpi=300, layout='constrained')
plt.style.use('ggplot')
axes.scatter([x for x in x1 if x >= x_min-1 and x <= x_max+1],
             [x for x in y1 if x >= y_min-1 and x <= y_max+1], color='grey', marker='.', s=1)
axes.scatter(x2, y2, color='black', marker='*', s=1)

# %%
df_numpy = df.to_numpy()
numeric_data = df_numpy.astype(int)
num_rows, num_columns = numeric_data.shape
numeric_data[x_min, y_min] = 2

# Turn on interactive mode
fig, ax = plt.subplots()
img = ax.imshow(numeric_data, cmap='viridis', interpolation='nearest')

# Adding legend
legend_elements = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='white', markersize=10, label='Value 0'),
                   plt.Line2D([0], [0], marker='o', color='w',
                              markerfacecolor='blue', markersize=10, label='Value 1'),
                   plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='yellow', markersize=10, label='Value 2')]

ax.legend(handles=legend_elements, loc='upper right')

a = 0
# plt.ion()
while True:
    a += 1
    print(a)
    data_old = np.copy(numeric_data)
    for row in np.arange(x_min-1, x_max+2):
        for col in np.arange(y_min-1, y_max+2):
            val = numeric_data[row, col]
            if val == 1:
                for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    try:
                        n_val = numeric_data[row+direction[0], col+direction[1]]
                        if n_val == 2:
                            numeric_data[row, col] = 2
                            continue
                    except:
                        continue
            elif val == 2:
                for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    try:
                        n_val = numeric_data[row+direction[0], col+direction[1]]
                        if n_val == 1:
                            numeric_data[row+direction[0], col+direction[1]] = 2
                            continue
                    except:
                        continue

    # img.set_array(numeric_data)
    # fig.canvas.draw()
    # fig.canvas.flush_events()

    if np.array_equal(data_old, numeric_data):
        break
# plt.ioff()
# plt.show()
# %%
# do the algorythm until you either find the point or after one iteration it's still the same or there is no possible way to go


def mark(val):
    if val:
        val = 1
    elif val == 1:
        val = 2

    return val


def direction(row, col, array):
    col_max = array.shape[1]
    row_max = array.shape[0]
    decision = {}
    # check if you can go up
    if row+1 <= row_max and array[row-1, col] and array[row+1, col]:
        decision['up'] = array[row-1, col]
    # check if you can go down
    elif row-1 >= 0 and array[row+1, col]:
        decision['down'] = array[row+1, col]
    # check if you can go right
    elif col+1 <= col_max and array[row, col+1]:
        decision['right'] = array[row, col+1]
    # check if you can go left
    elif col-1 >= 0 and array[row, col-1]:
        decision['left'] = array[row, col-1]

    decision = dict(sorted(decision.items(), key=lambda item: item[1]))
    decision = list(decision.keys())[0]
    return decision


def move(decision, row, col):
    if decision == 'up':
        row_new = row-1
        col_new = col
    elif decision == 'down':
        row_new = row+1
        col_new = col
    elif decision == 'right':
        row_new = row+1
        col_new = col
    elif decision == 'left':
        row_new = row-1
        col_new = col
    return row_new, col_new


row0 = 0
col0 = 0
target = {'x_min': 387,
          'x_max': 413,
          'y_min': 322,
          'y_max': 348}

df_it0 = df_numpy
df_it1 = df_numpy
df_it1[row0, col0] = 1
iteration = 0
while df_it0 != df_it1:
    if iteration == 0:
        df_it1[row0, col0] = df_numpy[row0, col0]
    iteration += 1
    df_it0 = df_it1


# %%
def change(val):
    if val:
        return 'Red'


vecfun = np.vectorize(change)
df_aux = vecfun(df_numpy)
