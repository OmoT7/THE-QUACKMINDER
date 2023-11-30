
import board
import pwmio
import busio
import time
import audiocore 
import audiobusio 
import adafruit_vl53l0x

# import datetime
# current_time = datetime.datetime(2023, 2, 15, 23, 41, 0).time()


# THis is the dispensing code comment this out then try to implement later

servo = pwmio.PWMOut(board.GP16, variable_frequency=True)
servo.frequency = 50

degrees = 175
increment = 25

duty_min = int(65535 * 0.5 / 20)
duty_max = int(65535 * 2.5 / 20)
duty_range = duty_max - duty_min

# audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2) # I2S pins BCLK, LRC, DIN
"""
tone_volume = 1  # digital volume, 0.0 to 1.0
frequency = 440  # tone frequency
samplerate = 8000
length = samplerate // frequency # // takes the floor() after doing the division
# make an array of signed 16bit values, which is what the MAX98357 takes
sine_wave = array.array("h", [0] * length) # the values are all initially 0

# make a single cycle of a sine wave to be played at 8kHz
for i in range(length):
    sine_wave[i] = int((math.sin(math.pi * 2 * i / length)) * tone_volume * (2 ** 15 - 1))

sine_wave_sample = audiocore.RawSample(sine_wave)
"""


times_dispensed = 1
"""
wave_file = open("duck_alarm.wav", "rb") # from https://cdn-learn.adafruit.com/assets/assets/000/057/801/original/StreetChicken.wav?
wave = audiocore.WaveFile(wave_file)
audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2) # MAX98357, I2S pins BCLK, LRC, DIN
"""
audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2) # MAX98357, I2S pins BCLK, LRC, DIN
wave_file = open("duck_alarm_2.wav", "rb") # from https://cdn-learn.adafruit.com/assets/assets/000/057/801/original/StreetChicken.wav?
wave = audiocore.WaveFile(wave_file)


i2c = busio.I2C(board.GP15, board.GP14)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)


HAS_PILL = vl53.range < 50

def checkpill(laser_range):
    while laser_range < 50:
        time.sleep(1)
        audio.play(wave, loop=True)
        laser_range = vl53.range
        if laser_range >= 50:
            audio.stop()


 
 
 
while True:
    if times_dispensed >= 7:
        print("Its time to refill the QuackMinder!!! Load 7 pills.")
        break
    else:
        current_range = vl53.range
        checkpill(current_range)

        print("Waiting for program to start")
        
        for angle in range(0, degrees, increment):
            time.sleep(3)
            duty_start = duty_min + int(angle/180 * duty_range)
            duty_end = duty_start + int(increment/180 * duty_range)

            for duty in range(duty_start, duty_end, 1):
                servo.duty_cycle = duty
                time.sleep(0.001) # smooth motion
            print("Executed the turn")
            print("Pill despinsed")
            current_range = vl53.range
            checkpill(current_range)
            print(times_dispensed)

            times_dispensed += 1

            time.sleep(2) # pause between increments
        servo.duty_cycle = duty_min # return to 0 degrees
        time.sleep(1)

# play a tone 

 # library to use I2S to communicate with MAX98357 amplifier

# for the MAX98357 amplifier
# Vin can be 3.3V or 5V, 5V is louder
# SD is shutdown if put to GND
# Gain: loudest with 100k to GND, loud straight to GND, regular no connection, 
#       quieter straight to VIN, quietest 100k to VIN



## Have to figure out how to implement the sound on to the pick later


