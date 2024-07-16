# libdev

Files here support intellisense/autocomplete in VS Code, which otherwise does not work since the circuitpython core libraries are not available for installation in a desktop python environment. This is hacky -- be careful!

## `usb_cdc`

This is hacked together into what VS Code will accept as an importable module based on comments in the circuitpython core [C implementation of usb_cdc](https://github.com/adafruit/circuitpython/tree/937cfa674857c4a1c5c0adefb3f58f3c54cca724/shared-bindings/usb_cdc)

## `canio`

canio is pulled from the [adafruit libraries bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/tag/20240716) where it was hidden within the mcp2515 library.