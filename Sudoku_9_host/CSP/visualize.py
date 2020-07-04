import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(1, 2)
a = np.array([0.118553, .069657, 0.086994, 0.069494, 0.081130, 0.084005, 0.081254])
b = np.array([22.1445, 22.1250, 21.9570, 22.1562, 22.2305, 22.2422, 22.0508])
plt.subplot(1, 2, 1)
plt.plot(range(a.shape[0]), a)
plt.xlabel('# of containers')
plt.ylabel('time (s)')
plt.xticks(ticks = range(b.shape[0]), labels = range(1, 8))
plt.subplot(1, 2, 2)
plt.plot(range(b.shape[0]), b)
plt.ylabel('usage memory (MB)')
plt.xlabel('# of containers')
plt.xticks(ticks = range(b.shape[0]), labels = range(1, 8))
plt.show()
