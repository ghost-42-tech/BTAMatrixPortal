# Using the Adafruit IO CircuitPython MQTT client
# to subscribe to Adafruit IO feeds

import sys
import time
import adafruit_logging as logging
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal
import busio
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import neopixel
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_io.adafruit_io import IO_MQTT
from adafruit_minimqtt.adafruit_minimqtt import MMQTTException
#import ssl

#***************************************************************
# CONSTANTS

#RED, YELLOW, GREEN, BLUE
COLORS = [0xff0000, 0xffff00, 0x00ff00, 0x0000ff]
FONT = terminalio.FONT
SCROLL_DELAY = 0.04

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

#***************************************************************
# UNCOMMENT FOLLOWING 2 LINES FOR SFHS BTA WiFi

#esp.set_ip_config("192.168.61.10", "192.168.61.1", "255.255.255.6")
#esp.set_dns_config("8.8.8.8", "8.8.4.4")

status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)

#***************************************************************
#CALLBACKS

def connected(client):
    # Called when the client is connected to Adafruit IO.
    print("Connected to Adafruit IO!")
    client.subscribe("scroller.quote")
    client.subscribe("scroller.instant")
    client.subscribe("scroller.spotify")
    client.subscribe("errors")
    client.subscribe("throttle")

def subscribe(client, userdata, feed, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}. Listening for feed changes...".format(feed, granted_qos))

def unsubscribe(client, userdata, feed, pid):
    # This method is called when the client unsubscribes from a feed.
    print("Unsubscribed from {0} with PID {1}".format(feed, pid))

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print("Disconnected from Adafruit IO!")

def message(client, feed, message):
    # Message function will be called when a subscribed feed has a new value.
    print("Topic {0} received new value: {1}".format(feed, message))
    if feed == "scroller.quote":
        strtitle = "Quote"
        for x in range(1):
            cleartext()
            matrixportal.set_text(str(message),0)
            matrixportal.set_text(str(strtitle),1)
            matrixportal.scroll_text(0.02)
            time.sleep(2)
    if feed == "scroller.spotify":
        strtitle = "Spotify"
        cleartext()
        matrixportal.set_text(str(message),0)
        matrixportal.set_text(str(strtitle),2)
        matrixportal.scroll_text(0.04)
        time.sleep(2)
    if feed == "scroller.instant":
        strtitle = "Message"
        for x in range(3):
            cleartext()
            matrixportal.set_text(str(message),0)
            matrixportal.set_text(str(strtitle),1)
            matrixportal.scroll_text(0.03)
            time.sleep(2)
    if feed == "wchesherwu/integration/weather/2626/forecast_hours_24":
        strtitle = "Message"
        for x in range(3):
            cleartext()
            matrixportal.set_text(str(message),0)
            matrixportal.set_text(str(strtitle),1)
            matrixportal.scroll_text(0.03)
            time.sleep(2)
    if feed == "errors":
        print("Adafruit IO Error: "  + str(message))
    if feed == "throttle":
        print("Adafruit IO Throttle Error: "  + str(message))
    cleartext()

def cleartext():
    matrixportal.set_text("",0)
    matrixportal.set_text("",1)
    matrixportal.set_text("",2)

# Connect to WiFi

print("Connecting to WiFi...")
try:
    wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)
    wifi.connect()
except Exception as ex:
        print(
            "Failed wifi connect. Error:",
            ex,
        )

# Initialize MQTT interface with the esp interface
MQTT.set_socket(socket, esp)
pool = socket

# Initialize a new MQTT Client object
mqtt_client = MQTT.MQTT(
    broker="io.adafruit.com",
    port=1883,
    username=secrets["aio_username"],
    password=secrets["aio_key"],
    socket_pool=pool,
    #ssl_context=ssl.create_default_context(),
    keep_alive=5000,
)
mqtt_client.enable_logger(logging, log_level=logging.DEBUG)

# Initialize an Adafruit IO MQTT Client
io = IO_MQTT(mqtt_client)

# Connect the callback methods defined above to Adafruit IO
io.on_connect = connected
io.on_disconnect = disconnected
io.on_subscribe = subscribe
io.on_unsubscribe = unsubscribe
io.on_message = message

#io.add_feed_callback("relay", on_relay_msg)

#***************************************************************
#***  MATRIXPORTAL STUFF

#ONE RGB PANEL
#matrixportal = MatrixPortal(esp=esp, debug=True, width=64, height=32)

#TWO RGB PANELS
matrixportal = MatrixPortal(esp=esp, debug=True, width=128, height=32, tile_rows=1)
matrixportal.scroll_text(0.04)

matrixportal.add_text( #**** blue for main scrolling text (0)
    text_font=FONT,
    text_position=(2, 25),
    text_color=COLORS[3],
    scrolling=True
)

matrixportal.add_text( #**** yellow for instant, quote title (1)
    text_font=FONT,
    text_position=((matrixportal.graphics.display.width // 12) - 1, (matrixportal.graphics.display.height // 2) - 4),
    text_color=COLORS[1],
)

matrixportal.add_text( #**** green for spotify title (2)
    text_font=FONT,
    text_position=((matrixportal.graphics.display.width // 12) - 1, (matrixportal.graphics.display.height // 2) - 4),
    text_color=COLORS[2],
)

matrixportal.set_text("Welcome!", 0)
matrixportal.scroll_text(0.04)

# Connect to Adafruit IO
print("Connecting to Adafruit IO...")
io.connect()

# while (io.status() < AIO_CONNECTED):
#     Serial.print(".")
# delay(500)

#***************************************************************
#*** MAIN LOOP BEGINS

print("Starting main loop...")

timercount = 0
lasttimer = 0

while True:
    # Poll for incoming messages
    try:
        io.loop()

        if (time.monotonic() - lasttimer) >= 600:
            print("Posting testtimer.")
            io.publish("scroller.testtimer", timercount)
            timercount += 10
            lasttimer = time.monotonic()
    except (Exception) as e:
        print("Failed to get data, retrying\n", e)
        wifi.reset()
        wifi.connect()
        io.reconnect()
        continue
    time.sleep(0.5)


#https://github.com/adafruit/circuitpython/issues/7606
