import time
import threading
import math
import streamlit as st
import random
import timer as counter
from timer import timer1, timer2
from datetime import datetime

class Averager:
    def __init__(self, config=None):
        self.t=config["t_init"] if config else 0
        self.t_step=config["t_step"] if config else 0.1
        self.v_t=config['vel_init'] if config else 0
        self.v_step= config["vel_step"] if config else 0.1
        self.sleep_t=config["sleep_time"] if config else 0.1
        self.value = []
        self.call_count = 0
        self.first_avg = 0
        self.first_avg_history = []
        self.avg_history = []
        self.running = False
        self.lock = threading.Lock()
        self.raw_values = []
        self.timestamps = []
        self.input_value = 50
        self.vel=40
        self.velocity=[]
        self.process_enabled=True
        self.temp_expr="50*math.sin(t)+input_value"
        self.vel_expr="100*math.sin(t)+vel"
        self.initial_avg_calculated = False
        self.initial_average = 0
        self.previous_average = 0
        

    def process_value(self, value):
        try:
            self.call_count += 1
            self.raw_values.append(value)
            self.timestamps.append(datetime.now().strftime("%H:%M:%S"))
            print(f"Processing value: {value}")

            if not self.process_enabled:
                last_avg=self.avg_history[-1] if self.avg_history else None
                last_first_avg=self.first_avg_history[-1] if self.first_avg_history else None
                self.avg_history.append(last_avg)
                self.first_avg_history.append(last_first_avg)
                return


            if self.call_count <= 4:
                print(f"Ignoring {self.call_count} : {value} ")
                pass

                # return None
            else:
                print(f"For call {self.call_count} : Input Value is {value}")
                self.value.append(value)
                if len(self.value) == 15:
                    if not self.initial_avg_calculated:
                        self.initial_average = sum(self.value) / 15
                        self.initial_avg_calculated = True
                        self.previous_average = self.initial_average
                        
                        print("Total_seconds_Passed " + str(counter.seconds_1))
                        print(f"For call {self.call_count} : Initial Average is {self.initial_average}")
                        print(f"For call {self.call_count} : Regular Average is {self.first_avg}")
                        self.avg_history.append(self.initial_average)
                        self.first_avg_history.append(self.first_avg)
                        self.value = []
                        self.previous_average = self.first_avg

                    # avg = sum(self.value) / 15
                    # if self.first_avg is None:
                        # avg = sum(self.value) / 15
                        # self.first_avg = avg
                    else:
                        if counter.counter_1>=90:
                            print(f"when greater than 90 {self.first_avg}")
                            current_average = (self.first_avg + (sum(self.value))) / 16
                            if(current_average<self.previous_average):
                                self.first_avg = self.first_avg + 1
                            else:
                                self.first_avg = (self.first_avg + (sum(self.value))) / 16    
                            
                            
                        elif counter.counter_1 >=30:
                            print(f"when greater than 30 {self.first_avg}")
                            current_average = (self.first_avg + (sum(self.value))) / 16
                            if(current_average>=self.previous_average):
                                self.first_avg = self.first_avg - 1
                            else:
                                self.first_avg = (self.first_avg + (sum(self.value))) / 16
                                
                            
                            
                            
                        else:
                            self.first_avg = (self.first_avg + (sum(self.value))) / 16
                    
                    print("Total_seconds_Passed " + str(counter.seconds_1))
                    print(f"For call {self.call_count} : Initial Average is {self.initial_average}")
                    print(f"For call {self.call_count} : Regular Average is {self.first_avg}")
                    self.avg_history.append(self.initial_average)
                    self.first_avg_history.append(self.first_avg)
                    self.value = []
                    self.previous_average = self.first_avg

        except Exception as e:
            print(f"Error in process value {e}", flush=True)

    def reset(self):
        with self.lock:
            self.value = []
            self.raw_values = []
            self.call_count = 0
            self.first_avg = None
            self.first_avg_history = []
            self.avg_history = []
            self.running = False
            self.velocity=[]
            self.process_enabled=True

def stimulate_velocity(averager):
    while True:
        with averager.lock:
            if not averager.running:
                break
            try:
                t=averager.v_t
                math_funcs ={ k: getattr(math,k) for k in dir(math) if not k.startswith("__")}
                local_vars={
                    **math_funcs,
                    "math":math,
                    "t":t,
                    "input_value":averager.input_value,
                    "vel":averager.vel,
                    "random": random
                }
                vel_value=eval(averager.vel_expr,{"__builtins__":{}},local_vars)
                print(vel_value)
                if vel_value >=30:
                    counter.start_timer1()
                if vel_value < 30:
                    counter.stop_timer1()
                    counter.reset_timer1()
                    # timer.stop_timer2()
                    # timer.reset_timer2()
                
                averager.velocity.append(vel_value)
            except Exception as e:
                print(f"Error in velocity eval : {e}")
                averager.velocity.append(None)
            averager.v_t+=averager.v_step
        time.sleep(averager.sleep_t)


def periodic_function(averager):
    while True:
        with averager.lock:
            if not averager.running:
                break
            try:
                t=averager.t
                math_funcs = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
                local_vars1={
                    **math_funcs,
                    "math":math,
                    "t":t,
                    "input_value":averager.input_value,
                    "vel":averager.vel,
                    "random": random
                }
                value=eval(averager.temp_expr,{"__builtins__":{}}, local_vars1)
                averager.process_value(value)
                #print(f"Processed value : {value}")
            except Exception as e:
                print(f"Error in Temperature eval : {e}")
                averager.process_value(None)
            averager.t+=averager.t_step
        time.sleep(averager.sleep_t)

def start(averager):
    with averager.lock:
        if averager.running:
            return
        averager.running=True
    thread1 = threading.Thread(target=periodic_function, args=(averager,))
    thread2=threading.Thread(target=stimulate_velocity, args=(averager,))
    timer_thread1 = threading.Thread(target = counter.timer1, daemon=True)
    # timer_thread2 = threading.Thread(target=counter.timer2, daemon=True)
    thread1.start()
    thread2.start()
    timer_thread1.start()
    # timer_thread2.start()
    
    
def timer():
    pass

def stop(averager):
    with averager.lock:
        averager.running = False


