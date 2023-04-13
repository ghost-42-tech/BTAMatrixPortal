# scroller
This is the codebase for the SFHS BTA MatrixPortal M4 LED Scroller.

Requirements:
------------------------------------------
> Use the MatrixPortal M4 (https://learn.adafruit.com/adafruit-matrixportal-m4/overview) and dual 64x32 4mm pitch LED screens 
> Connect to the SFHS IoT WiFi and accomodate no DHCP and requires gateway, DNS, and static IP configuration parameters
> Leverage Adafruit IO (AIO) as the back end (feed)
> Support an "instant" mode where a message is posted an AIO feed, and then immediately displayed on the device 
> Support display of random quotes at a timed interval using a "pull" model from the device (currently set to 5 minutes)
> Support display of Spotify "now playing" playlist messages every 5 minutes

Implementation:
------------------------------------------
> Use Adafruit IO CircuitPython MQTT as message broker 
> Use Python v8
> Use Adafruit ESP32SPI to set fixed IP, DNS, gateway WiFi configuration (https://docs.circuitpython.org/projects/esp32spi/en/latest/api.html)
> Uses Adafruit IO "wchesherwu" account 
> Uses 4 Adafruit IO feeds in the "Scroller" group to function:

"instant" this feed accepts text posts which are instantly displayed, and scrolled/repeated 3 times
"spotify" this feed is populated by a spotify account, and then using an IFTTT applet (https://ifttt.com/), accepts posts of currently playing song info every 5 minutes
"quoterequest" this feed accepts posts (a bit) from the device on a timed interval (300 seconds) which fires off a Zapier (https://zapier.com/) applet which reads a Google sheet (https://tinyurl.com/scrollerquotes), selects a random quote which is then posted to the "quote" feed, and displayed on the device.

Issues:
------------------------------------------
> Generic catch-all error handling in main loop needs to be broken down
> Overall/Console logging needs to be improved. Ran into some issues implementing "Adafruit Logger" for circuitpython. Had to back out implementation and go with "print" statements to console.
> Connectivity: It does not run for long periods of time without running into connection issues. Undocuemnted how long, but longer than 1 hour. This is the main issue. At some point the device stops listening, and the Adafruit IO messages just pile up in the queue. The device and system have no concept of logging which messages have been read, nor should that be implemented. WiFi is a flaky protocol, and the device needs to gracefully handle disconnections and reconnections. It needs to be able to run for days or weeks without issue. 
> Needs a time implementation for realtime logging and measuring uptime. 

Future Features:
------------------------------------------
> Text color configuration
> Font choices
> BMP display as part of the "scroller". Implemented this partially using sample code from the FlightPortal "plane" scrolling LED using DisplayIO, but there is a bug in the implementation which causes sample code to render messages undisplayable after showing the bmp. 
> Support additional feeds and message types, particularly with all of the options from IFTTT and Zapier.
