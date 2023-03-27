import psutil
import platform
import streamlit as st
import GPUtil
import speedtest
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_option('deprecation.showPyplotGlobalUse', False)

# Define some color constants
BLUE = "#1E90FF"
GREEN = "#00FF7F"
RED = "#FF4500"
ORANGE = "#FFA500"
PURPLE = "#800080"
YELLOW = "#FFFF00"

# Format the given number with commas for thousand separators
def format_number(num):
    return f"{num:,}"

# Format the given size in bytes to the appropriate unit
def format_size(size):
    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    index = 0
    while size >= 1024:
        size /= 1024
        index += 1
    return f"{size:.2f} {units[index]}"

def get_download_upload_speed():
    stest = speedtest.Speedtest()
    download = round(stest.download() / 1_000_000, 2)
    upload = round(stest.upload() / 1_000_000, 2)
    # Get download and upload speed variance
    download_var = [download] * 10
    upload_var = [upload] * 10
    return download, upload, download_var, upload_var


def get_system_info():
    if platform.system() == "Windows":
        # Get system load averages
        load_avg_1, load_avg_5, load_avg_15 = psutil.getloadavg()
        # Get CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        # Get RAM usage
        mem = psutil.virtual_memory()
        mem_total = mem.total
        mem_used = mem.used
        mem_percent = mem.percent
        # Get GPU usage
        gpu = GPUtil.getGPUs()[0]
        gpu_name = gpu.name
        gpu_load = gpu.load * 100
        gpu_mem_used = gpu.memoryUsed / 1024
        gpu_mem_total = gpu.memoryTotal / 1024
    else:
        load_avg_1 = load_avg_5 = load_avg_15 = cpu_usage = mem_total = mem_used = mem_percent = gpu_name = gpu_load = gpu_mem_used = gpu_mem_total = 0

    return load_avg_1, load_avg_5, load_avg_15, cpu_usage, mem_total, mem_used, mem_percent, gpu_name, gpu_load, gpu_mem_used, gpu_mem_total

def record_speed(download, upload, download_var, upload_var):
    speeds = pd.read_csv("speeds.csv", index_col=0) if "speeds.csv" in os.listdir() else pd.DataFrame(columns=["download", "upload", "download_var", "upload_var"])
    speeds = speeds.append({"download": download, "upload": upload, "download_var": download_var, "upload_var": upload_var}, ignore_index=True)
    speeds.to_csv("speeds.csv")
    return speeds


def get_download_speed():
    stest = speedtest.Speedtest()
    download = round(stest.download() / 1_000_000, 2)
    upload = round(stest.upload() / 1_000_000, 2)
    return download, upload


def plot_speeds(speeds):
    plt.plot(speeds["download"], label="Download Speed", color=BLUE)
    plt.plot(speeds["upload"], label="Upload Speed", color=GREEN)
    plt.legend()
    plt.xlabel("Time")
    plt.ylabel("Speed (Mbps)")
    plt.title("Download and Upload Speeds over Time")
    st.pyplot()

def main():
    st.set_page_config(page_title="System Information", page_icon=":computer:", layout="wide")
    st.sidebar.title("Navigation")
    menu = ["System Information", "Download Speed", "OCTOPRINT", "Share"]
    choice = st.sidebar.selectbox("Go to", menu)

    if choice == "System Information":
        load_avg_1, load_avg_5, load_avg_15, cpu_usage, mem_total, mem_used, mem_percent, gpu_name, gpu_load, gpu_mem_used, gpu_mem_total = get_system_info()

        st.write("# System Information")
        st.write("Load Average (1 min / 5 min / 15 min):", format_number(load_avg_1), "/", format_number(load_avg_5), "/", format_number(load_avg_15))
        st.write("CPU Usage:", format_number(cpu_usage), "%")
        st.write("RAM Usage:", format_size(mem_used), "/", format_size(mem_total), "(", format_number(mem_percent), "%)")
        st.write("GPU Name:", gpu_name)
        st.write("GPU Load:", format_number(gpu_load), "%")
        st.write("GPU Memory Usage:", format_size(gpu_mem_used), "/", format_size(gpu_mem_total))

    elif choice == "OCTOPRINT":
        # Display Seedbox dashboard in an iframe
       url = "http://octopi.local/"
       html = '<iframe src=' + url + ' width=1920 height=1080></iframe>'
       st.write(html, unsafe_allow_html=True)

    elif choice == "Share":
        # load the Deluge dashboard in an iframe
        url = "https://share.6697.org/"
        html = '<iframe src=' + url + ' width=1920 height=1080></iframe>'
        st.write(html, unsafe_allow_html=True)

    elif choice == "Download Speed":
        st.title("Download Speed")
        st.write("Click the button below to test your download and upload speed.")
        if st.button("Test Download and Upload Speed"):
            download, upload, download_var, upload_var = get_download_upload_speed()
            st.write("# Speed Test Results")
            st.write("Your download speed is:", format_number(download), "Mbps")
            st.write("Your upload speed is:", format_number(upload), "Mbps")

            # record the download and upload speeds
            speeds = record_speed(download, upload, download_var, upload_var)
            st.write("# Speed History")
            st.write("Download and Upload Speeds over Time")
            plot_speeds(speeds)



if __name__ == "__main__":
    main()

