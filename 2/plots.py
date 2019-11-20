from collections import OrderedDict
import matplotlib.pylab as plt
support_time = OrderedDict()
support_time[1000] = 69.789
support_time[1500] = 12.81
support_time[2000] = 8.881
support_time[2500] = 7.966
support_time[3000] = 4.657
support_time[4000] = 4.361
support_time[5000] = 4.005
support_time[10000] = 3.653

lists = sorted(support_time.items())

x, y = zip(*lists)
plt.plot(x, y)
plt.title("Time - Support figure")
plt.xlabel("Support")
plt.ylabel("Time(s)")
plt.savefig("support_time.png")
plt.show()
