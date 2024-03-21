import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Sample data for each subplot
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.tan(x)
y4 = np.sin(x) * np.cos(x)

# Create subplots
fig, axs = plt.subplots(5, 1, figsize=(8, 12), sharex='none')

# Plot data on each subplot
axs[0].plot(x, y1, color='blue')
axs[1].plot(x, y2, color='red')
axs[2].plot(x, y3, color='green')
axs[3].plot(x, y4, color='orange')

# Remove x-axis and spines from each subplot
for ax in axs:
    ax.xaxis.set_visible(False)
    ax.spines[['top', 'bottom', 'right', 'left']].set_visible(False)


# Remove titles from each subplot
for ax in axs:
    ax.set_title('')

# Draw a line from the first subplot to the second one
# axs[0].plot([0, 10], [0, 0], linestyle='--', color='black')  # Change [0, 10] to desired x-range

# Remove spaces between subplots
plt.subplots_adjust(hspace=0)

# Alternating y-axis position
for i, ax in enumerate(axs):
    if i % 2 == 0:  # Even index subplots
        ax.yaxis.tick_left()
        ax.spines['left'].set_visible(True)  # Remove y-axis

    else:  # Odd index subplots
        ax.yaxis.tick_right()
        ax.spines['right'].set_visible(True)


# Fifth subplot for projection
axs[4].plot(x[:10], y2[:10], label='Data from Subplot 2', color='purple')
axs[4].plot(x[10:20], y1[10:20], label='Data from Subplot 1', color='gray')
axs[4].plot(x[20:100], y4[20:100], label='Data from Subplot 1', color='gray')

# Add more data projections as needed

plt.show()


