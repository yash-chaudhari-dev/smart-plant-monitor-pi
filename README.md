# Smart IoT Plant Monitor (Raspberry Pi) 

##  About This Project
I built this project for a class assignment to learn how to connect hardware sensors to the internet.

The goal was simple: build a device that watches my plant 24/7 and "screams" at me (via email) if it gets too dry. It uses a **Raspberry Pi** to read the sensors and connects to the **Blynk IoT Cloud** so I can check the status from my phone anywhere.

##  What It Does
* Monitors Soil: Continuously checks if the plant has enough water.
* Visual Alerts: If it's dry, a (Red LED) turns on and a (Buzzer) sounds to alert anyone nearby.
* Email Notifications: Sends me an email instantly if the moisture drops too low.
* Cloud Dashboard: Syncs live data to the Blynk app for remote monitoring.

##  Tech Stack
* Hardware: Raspberry Pi 4, Grove Moisture Sensor, Grove ADC, LEDs, Buzzer.
* Software: Python 3.
* Libraries: `BlynkLib`, `smtplib` (for Email), `gpiozero`, `logging`.

##  Logs & Data History
The system automatically creates a local log file to track the plant's health over time.
* File Name: `moisture.log`
* What it records: Every time the status changes (e.g., from "Normal" to "Low") and timestamps of when Email Alerts are sent.
* How to view it:
    ```bash
    cat moisture.log
    ```

##  How to Run It
1.  Clone this repository.
2.  Install the required libraries:
    ```bash
    pip install blynklib gpiozero grove.py
    ```
3.  Update the `main.py` file with your own **Blynk Auth Token** and **Email Password**.
4.  Run the script:
    ```bash
    python3 main.py
    ```

---
### ⚠️ Important Note for Students
**This code is uploaded for portfolio display purposes only.** If you are a student at **Red River College (RRC)** or another institution, please **do not copy or submit this code** for your own assignments. This repository is public to demonstrate my skills to potential employers, not to provide a shortcut for schoolwork. Plagiarism is taken seriously—please write your own code!
