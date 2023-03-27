# Streamlit-Stuff

This Python program allows you to monitor system performance, test internet speeds, and plot speed history. It's user-friendly, utilizing psutil and GPUtil libraries for performance monitoring and speedtest, pandas, and matplotlib libraries for speed testing and plotting. 

## Usage

1. Install the required libraries: `pip install psutil GPUtil speedtest pandas matplotlib streamlit`
2. Run the program: `streamlit run streamlit_stuff.py`
3. Choose the desired section from the navigation menu:
    - "System Information" displays CPU, RAM, and GPU usage.
    - "Download Speed" tests download and upload speeds and records speed history.
    - "OCTOPRINT" displays an OCTOPRINT dashboard.
    - "Share" displays a share dashboard.

## Dependencies

- psutil
- GPUtil
- speedtest
- pandas
- matplotlib
- streamlit

## License

This software is released under the GNU Public License (GPL), a free, open-source license that allows users to use, modify, and distribute the software as long as they also distribute the source code under the same license. For more information, please refer to the LICENSE file.
