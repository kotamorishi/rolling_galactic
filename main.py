import time
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY
import uasyncio
from network_manager import NetworkManager
import urequests
import WIFI_CONFIG

# Server
GALACTIC_SEVER = 'https://rolling.kotamorishita.com/api/'
# unique id for your device
UUID = '692a216f-967b-49ec-95f5-ef307982c4b0'


mtx_starting = [
    "                                                     ",
    "                                                     ",
    " OOOOO   OOOOOO    OO    OOOO    OO  OO      XXXXXXX ",
    " OO  OO  OO       OOOO   OO OO   OO  OO      XXXXXXX ",
    " OO  OO  OO      OO  OO  OO  OO  OO  OO      XXXXXXX ",
    " OOOOO   OOOO    OOOOOO  OO  OO   OOOO       XXXXXXX ",
    " OOOO    OO      OO  OO  OO  OO    OO        XXXXXXX ",
    " OO OO   OO      OO  OO  OO OO     OO    OO  XXXXXXX ",
    " OO  OO  OOOOOO  OO  OO  OOOO      OO    OO  XXXXXXX ",
    "                                             XXXXXXX ",
    "                                                     "
]

mtx_error = [
    "                                                     ",
    "                                                     ",
    " OOOOOO  OOOOO   OOOOO     OOOO    OOOOO             ",
    " OO      OO  OO  OO  OO   OO  OO   OO  OO            ",
    " OO      OO  OO  OO  OO  OO    OO  OO  OO            ",
    " OOOO    OOOOO   OOOOO   OO    OO  OOOOO             ",
    " OO      OOOO    OOOO    OO    OO  OOOO              ",
    " OO      OO OO   OO OO    OO  OO   OO OO   OO        ",
    " OOOOOO  OO  OO  OO  OO    OOOO    OO  OO  OO        ",
    "                                                     ",
    "                                                     "
]

# constants for controlling scrolling text
PADDING = 5
OUTLINE_COLOUR = (0, 0, 0)
HOLD_TIME = 2.0
STEP_TIME = 0.075

# Wireless network manager
network_manager = None

# setup graphics
gu = GalacticUnicorn()
graphics = PicoGraphics(DISPLAY)
width = GalacticUnicorn.WIDTH
height = GalacticUnicorn.HEIGHT
brightness = 0.2

def display(image):

    fg_pen = graphics.create_pen(255, 200, 255)
    bg_pen = graphics.create_pen(0, 0, 0)
    gu.set_brightness(brightness)
    graphics.clear()
    for y in range(len(image)):
        row = image[y]
        for x in range(len(row)):
            pixel = row[x]
            # draw the prompt text
            if pixel == 'O':
                graphics.set_pen(fg_pen)
            else:
                graphics.set_pen(bg_pen)

            graphics.pixel(x, y)
    gu.update(graphics)

# fill display
def draw(colour):

    graphics.set_pen(colour)
    graphics.clear()
    gu.update(graphics)


def status_handler(mode, status, ip):
    # reports wifi connection status
    print(mode, status, ip)
    print('Connecting to wifi...')
    if status is not None:
        if status:
            print('Wifi connection successful!')
        else:
            print('Wifi connection failed!')


# function for drawing outlined text
def outline_text(text, x, y, message_color):
    graphics.set_pen(graphics.create_pen(int(OUTLINE_COLOUR[0]), int(OUTLINE_COLOUR[1]), int(OUTLINE_COLOUR[2])))
    graphics.text(text, x - 1, y - 1, -1, 1)
    graphics.text(text, x, y - 1, -1, 1)
    graphics.text(text, x + 1, y - 1, -1, 1)
    graphics.text(text, x - 1, y, -1, 1)
    graphics.text(text, x + 1, y, -1, 1)
    graphics.text(text, x - 1, y + 1, -1, 1)
    graphics.text(text, x, y + 1, -1, 1)
    graphics.text(text, x + 1, y + 1, -1, 1)

    graphics.set_pen(graphics.create_pen(int(message_color[0]), int(message_color[1]), int(message_color[2])))
    graphics.text(text, x, y, -1, 1)

def scrollText(message, text_color = (255,255,255),  background_color = (0,0,0)):
    global brightness

    gu.set_brightness(brightness)

    # state constants
    STATE_PRE_SCROLL = 0
    STATE_SCROLLING = 1
    STATE_POST_SCROLL = 2

    shift = 0
    state = STATE_PRE_SCROLL

    # set the font
    graphics.set_font("bitmap8")

    # calculate the message width so scrolling can happen
    msg_width = graphics.measure_text(message, 1)

    last_time = time.ticks_ms()

    while True:
        time_ms = time.ticks_ms()

        if gu.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_UP):
            brightness = brightness + 0.01 
            gu.adjust_brightness(+0.01)

        if gu.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN):
            brightness = brightness - 0.01 
            gu.adjust_brightness(-0.01)

        if state == STATE_PRE_SCROLL and time_ms - last_time > HOLD_TIME * 1000:
            if msg_width + PADDING * 2 >= width:
                state = STATE_SCROLLING
            last_time = time_ms

        if state == STATE_SCROLLING and time_ms - last_time > STEP_TIME * 1000:
            shift += 1
            if shift >= (msg_width + PADDING * 2) - 1:
                state = STATE_POST_SCROLL
                print("EEND")
                return
            last_time = time_ms

        if state == STATE_POST_SCROLL and time_ms - last_time > HOLD_TIME * 1000:
            state = STATE_PRE_SCROLL
            shift = 0
            last_time = time_ms

        graphics.set_pen(graphics.create_pen(int(background_color[0]), int(background_color[1]), int(background_color[2])))
        graphics.clear()

        outline_text(message, x=PADDING - shift, y=2, message_color=text_color)

        # update the display
        gu.update(graphics)

        # pause for a moment (important or the USB serial device will fail)
        time.sleep(0.001)


display(mtx_starting)
time.sleep(2)

def connectToWifi():
    global network_manager
    try:
        network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=status_handler)
        uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))
        return True
    except Exception as e:
        print(f'Wifi connection failed! {e}')
    return False


while True:
    # connect if not connected
    print(network_manager)
    if network_manager is None:
        connectToWifi()
        time.sleep(3)
        continue
    
    # reconnect if disconnected
    if network_manager.isconnected() == False:
        success = connectToWifi()
        if success == False:
            display(mtx_error)
            time.sleep(5)
            scrollText(f'Wifi connection failed!')
            continue

    try:
        r = urequests.get(f'{GALACTIC_SEVER}{UUID}')
        print(r)

        data = r.json()

        print(f'{data["message"]}')
        print(f'{data}')
        text_color = tuple(int(data["text_color"][i:i+2], 16) for i in (1, 3, 5))
        background_color = tuple(int(data["background_color"][i:i+2], 16) for i in (1, 3, 5))

        scrollText(data["message"],text_color, background_color)
        r.close()
    except Exception as e:
        print(f'Error: {e}')
        display(mtx_error)
        time.sleep(5)
        if(f'{e}' != '-2'):
            scrollText(f'{e}')
        
    time.sleep(1)

