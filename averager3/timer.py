import time

counter_1 = 0
seconds_1 = 0
minutes_1 = 0
hours_1 = 0
timer1_running = False

seconds_2 = 0
minutes_2 = 0
hours_2 = 0
timer2_running = False

def timer1():
    global seconds_1, minutes_1, hours_1, timer1_running, counter_1
    while True:
        if timer1_running:
            time.sleep(0.1)
            seconds_1 += 0.1
            counter_1 += 0.1
            if seconds_1 >= 60:
                seconds_1 = 0
                minutes_1 += 1
                counter_1 = counter_1
            if minutes_1 >= 60:
                minutes_1 = 0
                hours_1 += 1
            print(f"Timer 1 - {int(hours_1):02}:{int(minutes_1):02}:{int(seconds_1):02}", end="\r")
        else:
            time.sleep(0.1)  

def timer2():
    global seconds_2, minutes_2, hours_2, timer2_running
    while True:
        if timer2_running:
            time.sleep(0.1)
            seconds_2 += 0.1
            if seconds_2 >= 60:
                seconds_2 = 0
                minutes_2 += 1
            if minutes_2 >= 60:
                minutes_2 = 0
                hours_2 += 1
            print(f"\nTimer 2 - {int(hours_2):02}:{int(minutes_2):02}:{int(seconds_2):02}", end="\r")
        else:
            time.sleep(0.1)  

def start_timer1():
    global timer1_running
    timer1_running = True

def stop_timer1():
    global timer1_running
    timer1_running = False

def reset_timer1():
    global seconds_1, minutes_1, hours_1, counter_1
    seconds_1 = 0
    counter_1 = 0
    minutes_1 = 0
    hours_1 = 0

def start_timer2():
    global timer2_running
    timer2_running = True

def stop_timer2():
    global timer2_running
    timer2_running = False

def reset_timer2():
    global seconds_2, minutes_2, hours_2
    seconds_2 = 0
    minutes_2 = 0
    hours_2 = 0