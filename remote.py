from microbit import *
import radio

print('Control')
radio.on()

yIni = pin0.read_analog()
xIni = pin1.read_analog()

# def strPad(val):
#     s = str(val)
#     l = 4 - len(s)
#     return ' ' * l + s

def to_byte(val):
    forward = val & 512
    val = val & 511 if forward else ~val

    if val & 992 == 0:
        return 0

    val = val >> 2
    return val & 255

def to_bytes(y, x):
    x = 0 if x >= 496 and x <= 528 else x - 512
    x = x // 2
    return [to_byte(min(1023, max(0, y - x))), to_byte(min(1023, max(0, y + x)))]


while True:
    val = to_bytes(pin0.read_analog(), pin1.read_analog())
    print(val)
    radio.send_bytes(bytearray(val))
    # y = -1 * (pin0.read_analog() - yIni)
    # x = pin1.read_analog() - xIni
    # izq = y + x
    # der = y - x
    # print(strPad(izq) + ' ' + strPad(der) + ' ' + strPad(y) + ' ' + strPad(x))
