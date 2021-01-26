import matplotlib.pyplot as plt

plt.style.use('seaborn-whitegrid')


x_=[
0.73,
0.47,
0.8,
0.87,
0.6,
0.73,
0.47,
0.6,
0.73,
0.6,
0.66
]
y_=[
0.625,
0.33,
0.67,
0.83,
0.67,
0.857,
0.571,
0.714,
0.7,
1,
0.705
]
z_=[
0.83,
0.33,
1,
0.83,
0.67,
0.67,
0.44,
0.56,
0.875,
0.6,
0.662
]


t=[1,2,3,4,5,6,7,8,9,10,'avg']

# axes[0].plot(t, kf_x,'-ok', color = 'orange', markersize=4)
# axes[0].plot(t, x_)
# plt.xlabel('time')
# axes[0].plot(t, kf_x)
# plt.ylabel('x - axis')
# axes[1].plot(t, y_)
# plt.xlabel('time')
# axes[1].plot(t, kf_y)
# plt.ylabel('y - axis')

plt.subplot(2, 1, 1)
plt.plot(t, x_)
plt.plot(t, y_)
plt.plot(t, z_)

plt.xlabel('Skenario')
plt.legend(('akurasi','presisi','recall'),loc='upper center', bbox_to_anchor=(0.5, -0.2),
          fancybox=True, shadow=True, ncol=5)
#3plt.ylabel('y-axis')

plt.show()