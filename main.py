from realtimeDisplay_func import real_display
from bluetooth_server_func import blu_server
from threading import Thread
from multiprocessing import Process, Manager
from renogywanderer import get_power_data
from power_class import power

power_metric = get_power_data()

batteryLevel = power_metric[4]
batteryVoltage = power_metric[0]
batteryAmperage = power_metric[1]
panelAmperage = power_metric[3]
panelWattage = power_metric[2]

power_data = power(batteryLevel, batteryVoltage, batteryAmperage, panelAmperage, panelWattage)

manager = Manager()
FS = manager.Value('i', 0)
HI = manager.Value('i', 0)
TS = manager.Value('i', 72)
HS = manager.Value('i', 35)
p_list = manager.list()
C_L = manager.Value('i',0)
B_V = manager.Value('d',0)
B_A = manager.Value('d',0)
P_A = manager.Value('d',0)
P_W = manager.Value('i',0)
p_list = power_metric
C_L.value = power_metric[4]

p1 = Process(target=real_display, args=[FS,HI, power_data, TS, HS, p_list, C_L, B_V, B_A, P_A, P_W])
p2 = Process(target=blu_server, args=[FS,HI, power_data, TS, HS, p_list, C_L, B_V, B_A, P_A, P_W])
p2.start()
p1.start()
p2.join()
p1.join()