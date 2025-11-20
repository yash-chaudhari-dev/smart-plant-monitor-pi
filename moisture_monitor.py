"""
Name: Yash Chaudhari
Date: 11/10/2025
"""
import BlynkLib
import time
import logging
import smtplib, ssl
from email.mime.text import MIMEText
from sensor import Sensor
from gpiozero import LED, RGBLED

# --- CONFIGURATION (Update these with your own details) ---
BLYNK_TEMPLATE_ID = "YOUR_TEMPLATE_ID"
BLYNK_DEVICE_NAME = "YOUR_DEVICE_NAME"
BLYNK_AUTH = "YOUR_BLYNK_AUTH_TOKEN_HERE"
blynk = BlynkLib.Blynk(BLYNK_AUTH)


# Logging setup
logging.basicConfig(
    filename='moisture.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# Sensor setup
sensor = Sensor()
V_PIN_MOISTURE = 0
V_PIN_STATUS = 1
last_status = None
last_read_time = 0


# Simple LEDs (optional)

try:
    redLED = LED(21)
    greenLED = LED(20)
    blueLED = LED(16)
    simpleLEDs = True
except Exception as e:
    print("Simple LEDs not available:", e)
    simpleLEDs = False


# RGB LED (optional)

try:
    rgb = RGBLED(red=18, green=23, blue=12)
    rgbLED = True
except Exception as e:
    print("RGB LED not available:", e)
    rgbLED = False


# Moisture thresholds
# very wet
HIGH = 420
# too dry
LOW = 605    


# Email alert setup

def send_email_alert(moisture):
    """Send an email alert when soil moisture is LOW"""
    # SSL port
    port = 465  
    smtp_server = "smtp.gmail.com"
    sender_email = "YOUR_EMAIL@gmail.com"      # <--- Changed for privacy
    receiver_email = "YOUR_EMAIL@gmail.com"    # <--- Changed for privacy
    password = "YOUR_APP_PASSWORD_HERE"        # <--- Changed for privacy         

    message = MIMEText(f"️Alert! Soil moisture is LOW: {moisture}")
    message["Subject"] = "Soil Moisture Alert"
    message["To"] = receiver_email

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send_message(message)

        print("Email alert sent successfully!")
        logging.info("Email alert sent for Low moisture.")
    except Exception as e:
        print("Email sending failed:", e)
        logging.error(f"Email sending failed: {e}")

print("Soil Moisture Monitor Started (with LEDs + Email Alert)")

while True:
    blynk.run()

    if time.time() - last_read_time >= 1:
        try:
            moisture = sensor.moisture()

            if moisture is not None:
                # Determine moisture status
                if moisture < HIGH:
                    status = "High"   
                    if simpleLEDs:
                        redLED.off()
                        greenLED.off()
                        blueLED.on()
                    if rgbLED:
                        rgb.color = (0, 0, 1)

                elif moisture > LOW:
                    status = "Low"   
                    if simpleLEDs:
                        redLED.on()
                        greenLED.off()
                        blueLED.off()
                    if rgbLED:
                        # Flash red LED
                        for _ in range(2):
                            rgb.color = (1, 0, 0)
                            time.sleep(0.2)
                            rgb.off()
                            time.sleep(0.2)
                        rgb.color = (1, 0, 0)

                else:
                    status = "Normal" 
                    if simpleLEDs:
                        redLED.off()
                        greenLED.on()
                        blueLED.off()
                    if rgbLED:
                        rgb.color = (0, 1, 0)

                # Send to Blynk
                blynk.virtual_write(V_PIN_MOISTURE, moisture)
                blynk.virtual_write(V_PIN_STATUS, status)
                print(f"Moisture: {moisture} ({status})")
                

                # Log only when status changes
                if status != last_status:
                    logging.info(f"Moisture changed to {status} ({moisture})")
                    last_status = status

                    # Send email alert when LOW
                    if status == "Low":
                        send_email_alert(moisture)

        except Exception as e:
            print("Sensor read error:", e)
            logging.error(f"Sensor read error: {e}")

        last_read_time = time.time()

    time.sleep(0.05)
