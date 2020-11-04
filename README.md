# Kaleidoscope-Layer-Status
System tray icon to indicate current layer for Kaleidoscope keyboards

There are two parts to this project. The first is a plugin on the keyboard which gets the state of the keyboard's layers and sends this information over serial (code snippet provided). The second part is a small python app which polls the serial port, parses the data and displays a system tray icon based on the active layer.

This project was created to work with my keyboard and it's current setup. It hasn't had extensive testing and is probably hideously buggy, but I thought it might be a useful starting point for others.
