# Demo of music playing with callbacks for LED and display effects.
# Small variant on https://github.com/pololu/zumo-2040-robot/blob/master/micropython_demo/music.py

from zumo_2040_robot import robot

####################### music callback #######################

def music_callback(i):
    global buzzer
    update_display(buzzer.beats[i])

    # Set the LED brightness (0-255) according to the
    # note volume (0-128).
    value = min(255, buzzer.volumes[i]*2)

    # Start the hue at red (0) for a middle C (48) and
    # wrap around every 3 octaves (36 notes).
    hue = (buzzer.notes[i] - 48) * 360 // 36

    # Use lower saturation for longer note durations
    # (given in milliseconds).
    saturation = max(0, 255 - buzzer.durations[i] / 4)

    for led in range(6):
        rgb_leds.set_hsv(led, [hue, saturation, 2])

    rgb_leds.show()

####################### update display #######################

def update_display(elapsed_beats):
    display.fill(0)
    display.text("merry peasant", 0, 0)

    # quarter = 20160, 6/8 time
    eigths = elapsed_beats//10080
    measure = measure_offset + 1 + eigths // 6
    beat = 1 + eigths % 6

    display.text("Press B to stop.", 0, 50)
    display.show()

####################### zumo preparation #######################

def zumoPrep():
  global display, rgb_leds, button_b, measure_offset

  display  = robot.Display()
  rgb_leds = robot.RGBLEDs()
  button_b = robot.ButtonB()

  rgb_leds.set_brightness(5)

  measure_offset = 0

####################### zumo preparation #######################

def zumoLoop(song):
  global buzzer, measure_offset, button_b, rgb_leds
  try:
    while not button_b.check():
      if not buzzer.is_playing():
        measure_offset = 4
        buzzer.play_in_background(song)
  finally:
    rgb_leds.off()
    buzzer.off()
    display.fill(0)
    display.show()

####################### main #######################

global buzzer, motors

buzzer = robot.Buzzer()
buzzer.set_callback(music_callback)

motors = robot.Motors()

### end ###
