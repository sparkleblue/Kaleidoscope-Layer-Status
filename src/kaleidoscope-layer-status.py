## kaleidoscope-layer-status -- System tray icon to indicate current
## layer for Kaleidoscope keyboards
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

import serial
import pystray
import time
import sys

from PIL import Image
from pystray import Menu, MenuItem

# Handler for Exit menu item
def exit(icon, item):
    icon.visible=False
    icon.stop()

# Send layer request to keyboard
def sendLayerRequest():
    # request must end with \n.
    ser.write("layers\n.".encode())

# pystray icon callback - process keyboard responses and update icon
def callback(icon):
    icon.visible = True
    response = ""
    sendLayerRequest()

    currentLayer = -1
    while True:
        line = ser.readline().decode()
        response += line

        # full response received - parse it
        if "." in line:
            #print(response)

            layers = list(response)
            
            # valid response is 3 chars starting with a t
            try:
                if len(layers) < 3 or layers[0] != 't':
                    pass
                elif layers[1] == 't':
                    if currentLayer != 1:
                        icon.icon = imageLayer1
                        currentLayer = 1
                elif layers[2] == 't':
                    if currentLayer != 2:
                        icon.icon = imageLayer2
                        currentLayer = 2
                else:
                    if currentLayer != 0:
                        icon.icon = imageLayer0
                        currentLayer = 0

                # reset the response and buffers, and send another request
                response = ""
                ser.reset_input_buffer()
                ser.reset_output_buffer()
                sendLayerRequest()

            except Exception:
                #print('exception')
                icon.visible=False
                icon.stop()

        # check if we should exit
        if icon.visible == False:
            break


def main():
    global ser, imageLayer0, imageLayer1, imageLayer2
    ser = serial.Serial('COM3', 9600, timeout=0.5)  # open serial port
    
    # create icons for each layer
    imageLayer0 = Image.new('RGBA', (128,128), (105,105,105,255)) # image for layer 0
    imageLayer1 = Image.new('RGBA', (128,128), (52,186,7,255)) # image for layer 1
    imageLayer2 = Image.new('RGBA', (128,128), (209,194,23,255)) # image for layer 2
    
    menu = Menu(MenuItem('Exit', exit))

    icon = pystray.Icon("Layer Icon", imageLayer0, "KaleidoscopeLayerStatus", menu)
    icon.run(callback) # use a callback otherwise this will run in the main thread

    ser.close()   # close port


if __name__ == "__main__":
    main()
