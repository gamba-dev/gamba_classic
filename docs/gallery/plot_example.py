"""
Neon Line Plot
==========================

This is a test figure using code from `Dominik Haitz cyberpunk article for matplotlib <https://matplotlib.org/matplotblog/posts/matplotlib-cyberpunk-style/>`_
"""

import matplotlib.pyplot as plt, pandas as pd

data = [10,11,14,8,9,11,11,14,8,9,11]
color = '#00ff41'

plt.style.use("dark_background")
plt.rcParams['axes.axisbelow'] = True
for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey

for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey

plt.figure(figsize=[10,4])

plt.plot(range(len(data)), data, color=color, label='data') # plot the line

for n in range(1, 10):
    plt.plot(range(len(data)), data, linewidth=(1.1 * n), alpha=0.03, color=color) # add blur around the line
plt.fill_between(range(len(data)), data, [min(data)*0.9]*len(data), alpha=0.1, color=color)

plt.ylim(min(data)*0.9, max(data)*1.08)

plt.grid(color='#2A3459')
plt.legend()
plt.scatter(range(len(data)), data, color=color) # plot the points
plt.show()

