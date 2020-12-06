from microbit import *
import radio
import utime

print('Car')
pin14.write_digital(1)
radio.on()

def from_byte(val):
    forward = 1
    if val & 128:
        forward = 0
        val = val & 127

    val = val << 3
    if val:
        val = val | 7
    return [val, forward]

def acc(val):
    valI, valD = val
    speedI, dirI = from_byte(valI)
    speedD, dirD = from_byte(valD)

    pin1.write_analog(speedI)
    pin12.write_digital(dirI)
    pin13.write_digital(dirI ^ 1)

    pin2.write_analog(speedD)
    pin15.write_digital(dirD)
    pin16.write_digital(dirD ^ 1)


last = b''
last_timestamp = 0

while True:
    # msg = radio.receive_bytes()
    details = radio.receive_full()
    if details:
        msg, rssi, timestamp = details
        last_timestamp = timestamp
        if last != msg:
            acc(msg)
            last = msg
        # print(msg[0] * 8, msg[1] * 8)
        # print(msg[0], msg[1])
    elif utime.ticks_diff(utime.ticks_us(), last_timestamp) > 1000000:
        msg = [0, 0]
        if last != msg:
            print('Detenerse')
            acc(msg)
            last = msg
