# pip install pandas streamlit matplotlib
import streamlit as st
import matplotlib.pyplot as plt
import time
from averager import Averager, start, stop
import pandas as pd
import csv
import yaml
import plotly.graph_objs as go
import plotly.express as px
# import timer as time_stamp
import threading
from datetime import datetime

# time_stamp_ = threading.Thread(target = time_stamp.timer2, daemon=True)
# time_stamp_.start()
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
st.title("Real Time Temperature Averager")
if "averager" not in st.session_state:
    st.session_state.averager = Averager(config)

averager = st.session_state.averager

temp_option = st.radio("Choose Temperature Input", options=["Use Definite Temperature", "Use Random Temperature"])

if temp_option == "Use Definite Temperature":
    averager.definite_temp = True
    averager.use_random = False
    averager.input_value = st.slider("Input Offset Value (Temp) ",
                                     min_value=config["temp_slider"]["min"],
                                     max_value=config["temp_slider"]["max"],
                                     value=config["temp_slider"]["default"]
                                     )
elif temp_option == "Use Random Temperature":
    averager.definite_temp = False
    averager.use_random = True

    temp_min = st.slider("Temperature Random Min",
                         min_value=config["temp_random_slider"]["min_limit"],
                         max_value=config["temp_random_slider"]["max_limit"],
                         value=averager.temp_min)

    temp_max = st.slider("Temperature Random Max",
                         min_value=temp_min,
                         max_value=config["temp_random_slider"]["max_limit"],
                         value=averager.temp_max)

    averager.temp_min = temp_min
    averager.temp_max = temp_max

averager.vel = st.slider("Velocity Value (kmph)",
                         min_value=config["vel_slider"]["min"],
                         max_value=config["vel_slider"]["max"],
                         value=config["vel_slider"]["default"]
                         )

averager.temp_expr = st.text_input("Enter Temperature Function  :  ", averager.temp_expr)
averager.vel_expr = st.text_input("Enter Velocity Function : ", averager.vel_expr)

if averager.input_value >= config["thresholds"]["temp_limit"]:
    st.write(f"Exceeding the temperature {averager.input_value} degree stopping the process ")
    averager.process_enabled = False
elif (averager.input_value >= config["thresholds"]["combined_limit"]["temp"] and averager.vel >=
      config["thresholds"]["combined_limit"]["vel"]):
    st.write(
        f"Temperature {averager.input_value} degree and velocity {averager.vel} kmph. Exceeded! Stopping the process")
    averager.process_enabled = False
else:
    averager.process_enabled = True

col1, col2, col3, col4 = st.columns(4)

if col1.button("Start"):
    # time_stamp.start_timer2()
    start(averager)

if col2.button("Stop"):
    # time_stamp.stop_timer2()
    # time_stamp.reset_timer2()
    stop(averager)

if col3.button("Reset"):
    stop(averager)
    averager.reset()

max_len = max(len(averager.raw_values), len(averager.velocity), len(averager.avg_history),
              len(averager.first_avg_history))

raw_values = averager.raw_values
velocity = averager.velocity
avg_history = averager.avg_history
first_avg_history = averager.first_avg_history

data = []

# timestamps = []


for i in range(len(raw_values)):
    temp = raw_values[i] if i < len(raw_values) else '-'
    vel = velocity[i] if i < len(velocity) else '-'
    adjusted_index = i - 4
    if i >= 18 and (adjusted_index // 15) < len(avg_history) and (i - 18) % 15 == 0:
        avg = avg_history[adjusted_index // 15]
    else:
        avg = '-'

    if i >= 18 and (adjusted_index // 15) < len(first_avg_history) and (i - 18) % 15 == 0:
        weighted_avg = first_avg_history[adjusted_index // 15]
    else:
        weighted_avg = '-'
    # if i>= len(timestamps):
    #     timestamps.append(datetime.now().strftime("%H:%M:%S"))

    data.append({
        "Step": i,
        "Temperature": temp,
        "Velocity": vel,
        "Initial Average": avg,
        "Regular Average": weighted_avg,
        "Time Stamp": averager.timestamps[i] if i < len(averager.timestamps) else '-'
    })
df = pd.DataFrame(data)
df = df.round(2)
csv_data = df.to_csv(index=False).encode('utf-8')

st.download_button("Download CSV", csv_data, "averager_data.csv", "text/csv")

##Display
if first_avg_history:
    st.metric(label="Current Average Temperature ", value=round(first_avg_history[-1], 2))
    if first_avg_history:
        current_temp = round(first_avg_history[-1], 2)
        st.markdown(
            f"""
            <div style="
                background-color: black;
                border: 2px solid limegreen;
                border-radius: 12px;
                padding: 16px;
                text-align: center;
                width: 250px;
                margin-bottom: 20px;
            ">
                <h4 style="color: white; margin: 0;">Current Average Temperature</h4>
                <p style="color: limegreen; font-size: 32px; font-weight: bold; margin: 0;">{current_temp}°C</p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.subheader("Past 15 Temperature Values")

window_size = 15
raw_values_to_display = raw_values[4:]  # Skip first 4
recent_values = raw_values_to_display[-window_size:] if len(
    raw_values_to_display) >= window_size else raw_values_to_display

cols = st.columns(window_size)

for i, col in enumerate(cols):
    value = f"{recent_values[i]:.2f}" if i < len(recent_values) else "-"
    col.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:16px;
            border:1px solid #ddd;
            border-radius:8px;
            padding:8px;
            background-color:#111;
            color:#0f0;
            width: 60px;
            overflow-wrap: break-word;
            white-space: normal;
            word-wrap: break-word;
        ">
            {value}
        </div>
        """,
        unsafe_allow_html=True
    )

st.subheader("Live Input Values")
fig, ax = plt.subplots()
ax.plot(averager.raw_values, label='Input Value')
ax.plot(averager.velocity, label='Input Velocity')
ax.plot(averager.avg_history, label='15 point avg')
ax.plot(averager.first_avg_history, label='Weighted Avg')
ax.legend()
st.pyplot(fig)

st.rerun()