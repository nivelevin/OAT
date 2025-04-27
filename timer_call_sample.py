# import timer
# import threading
# import time

# timer_thread = threading.Thread(target=timer.timer1, daemon=True)
# timer_thread2 = threading.Thread(target=timer.timer2, daemon=True)
# timer_thread.start()
# timer_thread2.start()

# for i in range(100000):
#     print("hi_LEvin")
#     timer.start_timer1()  
#     if timer.seconds_1>=30:
#         timer.stop_timer1()
#         # timer.reset_timer1()
#         timer.start_timer2()
#     if timer.seconds_2>=30:
#         timer.stop_timer2()
#         timer.reset_timer2()
#         time.sleep(5)
#         timer.start_timer2()
        
            
            
        
#     time.sleep(1)

# timer.start_timer1()  


# time.sleep(5)  
# timer.stop_timer1()   

# time.sleep(2)  
# timer.reset_timer1()  

# timer.start_timer2() 

# time.sleep(10)  
# timer.stop_timer2()  
# timer.reset_timer2()  

from datetime import datetime
import time

# Current time formatted as HH:MM:SS

for i in range(200):
    time.sleep(1)
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"Current time: {timestamp}", end="\r")

# print(type(timestamp))

