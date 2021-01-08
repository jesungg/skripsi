import matplotlib.pyplot as plt


t_object = [7, 8, 9, 10, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 35, 36]
_x=[385, 378, 354, 342, 318, 318, 350, 399, 441, 444, 449, 453, 448, 552, 475, 492, 502, 521, 457, 483, 472, 401, 365, 328, 306, 318, 337, 335, 340, 379]
_y=[239, 242, 250, 267, 234, 239, 253, 271, 263, 265, 263, 265, 268, 297, 266, 260, 264, 280, 291, 287, 281, 277, 262, 255, 256, 231, 221, 230, 262, 261]
kf_x = [339.0, 318.0, 311.0, 326.0, 359.0, 395.0, 416.0, 434.0, 447.0, 455.0, 498.0, 497.0, 507.0, 517.0, 529.0, 521.0, 524.0, 522.0, 506.0, 487.0, 465.0, 443.0, 426.0, 415.0, 404.0, 395.0, 393.0]
kf_y = [265.0, 246.0, 243.0, 248.0, 260.0, 261.0, 264.0, 265.0, 267.0, 269.0, 279.0, 277.0, 274.0, 274.0, 277.0, 281.0, 284.0, 285.0, 285.0, 282.0, 279.0, 276.0, 270.0, 263.0, 259.0, 259.0, 259.0]
time_kf = []

print(t_object)
for i in range(len(t_object)):
    time_kf.append(t_object[i]+1)
print(t_object)
print(time_kf)
#try plotting
plotx_=_x+[None]
ploty_=_y+[None]
plot_kfx=[None,None,None,None]+kf_x
plot_kfy=[None,None,None,None]+kf_y
t_object = [0]+ t_object
time_kf = [0]+time_kf
print(t_object)
print(time_kf)

plt.style.use('seaborn-whitegrid')
plt.subplot(2,1,1)
plt.plot(t_object, plotx_)
plt.plot(time_kf, plot_kfx)
# plt.plot(t ,plotx_)
plt.ylabel('x-axis')

plt.subplot(2,1,2)
plt.plot(t_object, ploty_)
plt.plot(time_kf, plot_kfy)
plt.xlabel('time (s)')
plt.ylabel('y-axis')

plt.savefig('final_plot.png')

plt.show()