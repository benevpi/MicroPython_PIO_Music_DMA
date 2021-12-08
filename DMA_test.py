import PIOBeep
import array
beeper = PIOBeep.PIOBeep(0,0, dma=True, dma_timer=0)

#note can probably do a chain into the state machine active register?

note_1 = beeper.calc_pitch(200)
note_2 = beeper.calc_pitch(400)

#max_y = 65,536
#min_speed = 125000000/65536 = 1907 samples per second.

buffer = array.array("L", 0 for x in range(4000))

for x in range(2000):
    buffer[x] = beeper.calc_pitch(int( x/10 + 200))
    
for x in range(2500, 3990):
    buffer[x] = beeper.calc_pitch(400 - int( x/10))

beeper.set_dma_speed(1,65535)
beeper.start_statemachine()

beeper.play_dma_buffer(buffer, 4000)
beeper.get_dma_stats()

