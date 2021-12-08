from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep
import rp2040_pio_dma

max_count = 5000
freq = 1000000

#based on the PWM example.
@asm_pio(sideset_init=PIO.OUT_LOW)
def square_prog():
    label("restart")
    pull(noblock) .side(0)
    mov(x, osr)
    jmp(not_x, "restart")
    mov(y, isr)
    
    #start loop
    #here, the pin is low, and it will count down y
    #until y=x, then put the pin high and jump to the next secion
    label("uploop")
    jmp(x_not_y, "skip_up")
    nop()         .side(1)
    jmp("down")
    label("skip_up")
    jmp(y_dec, "uploop")
    
    #mirror the above loop, but with the pin high to form the second
    #half of the square wave
    label("down")
    mov(y, isr)
    label("down_loop")
    jmp(x_not_y, "skip_down")
    nop() .side(0)
    jmp("restart")
    label("skip_down")
    jmp(y_dec, "down_loop")
    
class PIOBeep:
    def __init__(self, sm_id, pin,dma=False, dma_chan=0, dma_timer=0):
    
        self.square_sm = StateMachine(sm_id, square_prog, freq=freq, sideset_base=Pin(pin))
        

        #pre-load the isr with the value of max_count
        self.square_sm.put(max_count)
        self.square_sm.exec("pull()")
        self.square_sm.exec("mov(isr, osr)")
        
        if dma:
            import rp2040_pio_dma
            self.dma_timer = dma_timer
            self.dma_class = rp2040_pio_dma.PIO_DMA_Transfer(dma_chan, sm_id, 32, 4000)
            self.dma_class.use_timer(0)
            

    #note - based on current values of max_count and freq
    # this will be slightly out because of the initial mov instructions,
    #but that should only have an effect at very high frequencies
    def calc_pitch(self, hertz):
        return int( -1 * (((1000000/hertz) -20000)/4))
    
    def play_value(self, note_len, pause_len, val):
        self.square_sm.active(1)
        self.square_sm.put(val)
        sleep(note_len)
        self.square_sm.active(0)
        sleep(pause_len)
        
    def start_statemachine(self):
        self.square_sm.active(1)
    def stop_statemachine(self):
        self.square_sm.active(0)
        
    def play_pitch(self, note_len, pause_len, pitch):
        self.play_value(note_len, pause_len, self.calc_pitch(pitch))
        
    def play_dma_buffer(self, buffer, length):
        self.dma_class.set_transfer_count(length)
        #rp2040_pio_dma.create_dma_to_stop_pio0(1)
        #self.dma_class.chain_to(1)
        self.dma_class.start_transfer(buffer)
    
    def set_dma_speed(self, x, y):
        rp2040_pio_dma.set_timer_reg(self.dma_timer, x, y)
        
    def get_dma_stats(self):
        print(self.dma_class.busy())
        print(self.dma_class.transfer_count())
        
