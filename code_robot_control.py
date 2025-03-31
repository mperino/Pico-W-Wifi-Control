# rename me to code.py to run on circutpython
# add adafruit_httpserver library to pico W to get this to run 
# Code based on circutpython 9
# Wifi Hot spot and password are defined under settings..
# YES I know there are more secure ways to do this, but this is intended for insecure use and easy to change/find.

import socketpool
import wifi

from adafruit_httpserver import Server, Request, Response, POST

# settings 
AP_SSID = "4160Robot1"   # Access point name
AP_PASSWORD = "TheRoBucs"  # Access point pw (Case Sensitive) 
font_family = "monospace"
html_page_title = "Robot Control"  # Title of the Page in the tab
html_page_header = "Simple Robot Control"  # Title at the top of the page
html_page_summary = "Control the Robot with these buttons:" # Page summary
html_section1_header = "Directions"
html_section2_header = "Servo Motor #1"

# Web page Function.  Edit this to change what the page displays, buttons, etc..
def webpage():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-type" content="text/html;charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    html{{font-family: {font_family}; background-color: lightgrey;
    display:inline-block; margin: 0px auto; text-align: center;}}
      h1{{color: deeppink; width: 200; word-wrap: break-word; padding: 2vh; font-size: 35px;}}
      p{{font-size: 1.5rem; width: 200; word-wrap: break-word;}}
      .button{{font-family: {font_family};display: inline-block;
      background-color: black; border: none;
      border-radius: 4px; color: white; padding: 16px 40px;
      text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}}
      p.dotted {{margin: auto;
      width: 75%; font-size: 25px; text-align: center;}}
    </style>
    </head>
    <body>
    <title>{html_page_title}</title>
    <h1>{html_page_header}</h1>
    <br>
    <h1>{html_page_summary}</h1><br>
    <h1>{html_section1_header}</h1><br>
    <form accept-charset="utf-8" method="POST">
    <button class="button" name="Direction" value="Forward" type="submit">Forward</button></a></p></form>
    <form accept-charset="utf-8" method="POST">
    <table>
    <tr>
    <th><button class="button" name="Direction" value="Left_90" type="submit">Left 90°</button></a></form>
    <form accept-charset="utf-8" method="POST"></th>
    <th><button class="button" name="Direction" value="Left_45" type="submit">Left 45°</button></a></form>
    <form accept-charset="utf-8" method="POST"></th>
    <th><button class="button" name="Direction" value="Stop" type="submit">Stop</button></a></form>
    <form accept-charset="utf-8" method="POST"></th>
    <th><button class="button" name="Direction" value="Right_45" type="submit">Right 45°</button></a></form>
    <form accept-charset="utf-8" method="POST"></th>
    <th><button class="button" name="Direction" value="Right_90" type="submit">Right 90°</button></a></form>
    <form accept-charset="utf-8" method="POST"></th>
    </tr>
    </table>
    
    <button class="button" name="Direction" value="Back" type="submit">Back</button></a></p></form>
    <h1>{html_section2_header}</h>
    <p><form accept-charset="utf-8" method="POST">
    <button class="button" name="Servo1" value="0" type="submit">Servo1 to 0 Degrees</button></a></p></form>
    </body></html>
    """
    return html

# setup wifi access point using the AP name and password defined at the top of the page

print("Creating access point...")
wifi.radio.start_ap(ssid=AP_SSID, password=AP_PASSWORD)
print(f"Created access point {AP_SSID}")


# server HTTP on http://192.168.4.1:5000
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)


@server.route("/")
def base(request: Request):
    """
    Serve a default static plain text message.
    """
    return Response(request, f"{webpage()}", content_type='text/html')
#  if a button is pressed on the site
@server.route("/", POST)
def buttonpress(request: Request):
    #  get the raw text
    raw_text = request.raw_request.decode("utf8")
    print(raw_text)
    #  if the led on button was pressed
    if "Direction=Forward" in raw_text:
        #  turn on the onboard LED
        print("Forward Robot")
    #  if the led off button was pressed
    if "Direction=Back" in raw_text:
        #  turn the onboard LED off
        print("Backup Robot")
    #  if the party button was pressed
    if "Direction=Stop" in raw_text:
        #  toggle the parrot_pin value
        print("Stop Robot")
    #  reload site
    return Response(request, f"{webpage()}", content_type='text/html')


server.serve_forever(str(wifi.radio.ipv4_address_ap))
