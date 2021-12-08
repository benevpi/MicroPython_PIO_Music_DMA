# MicroPython_PIO_Music_DMA
Play music on Raspberry Pi Pico Without CPU involvement

This is based on PIOBeep (https://github.com/benevpi/pico_pio_buzz) but lets you setup a piece of sound and then play it without processor involvement.

It's a little RAM intensive (circa 2K per second). It *might* be possible to improve this but might not. The DMA transfer is running as slowly as it can. I suppose slowing down the clock frequency would decrease RAM useage, but that probably defeats the point. It's probably possible to double-buffer and do some cleaver things that way, but you might not end up gaining much.

I still need to think about the API a bit as it's pretty rough at the moment.
