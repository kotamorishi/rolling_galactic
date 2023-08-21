import time
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY
import uasyncio
from network_manager import NetworkManager
import urequests
import WIFI_CONFIG
import ujson


# constants for controlling scrolling text
PADDING = 5
MESSAGE_COLOUR = (255, 255, 255)
OUTLINE_COLOUR = (0, 0, 0)
HOLD_TIME = 2.0
STEP_TIME = 0.075

# setup graphics
gu = GalacticUnicorn()
graphics = PicoGraphics(DISPLAY)
width = GalacticUnicorn.WIDTH
height = GalacticUnicorn.HEIGHT


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
def outline_text(text, x, y):
    graphics.set_pen(graphics.create_pen(int(OUTLINE_COLOUR[0]), int(OUTLINE_COLOUR[1]), int(OUTLINE_COLOUR[2])))
    graphics.text(text, x - 1, y - 1, -1, 1)
    graphics.text(text, x, y - 1, -1, 1)
    graphics.text(text, x + 1, y - 1, -1, 1)
    graphics.text(text, x - 1, y, -1, 1)
    graphics.text(text, x + 1, y, -1, 1)
    graphics.text(text, x - 1, y + 1, -1, 1)
    graphics.text(text, x, y + 1, -1, 1)
    graphics.text(text, x + 1, y + 1, -1, 1)

    graphics.set_pen(graphics.create_pen(int(MESSAGE_COLOUR[0]), int(MESSAGE_COLOUR[1]), int(MESSAGE_COLOUR[2])))
    graphics.text(text, x, y, -1, 1)

def scrollText(message, background_color = (255,255,255)):

    gu.set_brightness(0.5)

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
            gu.adjust_brightness(+0.01)

        if gu.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN):
            gu.adjust_brightness(-0.01)

        if state == STATE_PRE_SCROLL and time_ms - last_time > HOLD_TIME * 1000:
            if msg_width + PADDING * 2 >= width:
                state = STATE_SCROLLING
            last_time = time_ms

        if state == STATE_SCROLLING and time_ms - last_time > STEP_TIME * 1000:
            shift += 1
            if shift >= (msg_width + PADDING * 2) - width - 1 + (width / 2):
                state = STATE_POST_SCROLL
                return
            last_time = time_ms

        if state == STATE_POST_SCROLL and time_ms - last_time > HOLD_TIME * 1000:
            state = STATE_PRE_SCROLL
            shift = 0
            last_time = time_ms

        graphics.set_pen(graphics.create_pen(int(background_color[0]), int(background_color[1]), int(background_color[2])))
        graphics.clear()

        outline_text(message, x=PADDING - shift, y=2)

        # update the display
        gu.update(graphics)

        # pause for a moment (important or the USB serial device will fail)
        time.sleep(0.001)


# get request
while True:
    # set up wifi
    try:
        network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=status_handler)
        uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))
    except Exception as e:
        print(f'Wifi connection failed! {e}')

    r = urequests.get('http://10.10.22.168:3999/api/164127fd-87a0-48fe-8b83-be60cba41fc3')
    json_str = '{"color": "#36AE7C", "message": "To Emma & Leo, this is the message :) Love you!"}'
    #data = ujson.loads(json_str)
    # retrive r content
    data = r.json()

    print(f'{data["message"]}')
    rgb_color = tuple(int(data["color"][i:i+2], 16) for i in (1, 3, 5))

    scrollText(data["message"],rgb_color)
    r.close()
    time.sleep(15)
