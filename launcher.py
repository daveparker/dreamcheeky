import usb.core # pip install pyusb
import sys
import time


class Launcher():
  # Low level launcher driver commands
  # this code mostly taken from https://github.com/nmilford/stormLauncher
  # with bits from https://github.com/codedance/Retaliation

  MAX_ANGLE = 10
  MIN_ANGLE = -10
  MAX_INCLINATION = 2
  MIN_INCLINATION = -2

  def __init__(self, calibrate=True):
    self.dev = usb.core.find(idVendor=0x2123, idProduct=0x1010)
    if self.dev is None:
      raise ValueError('Missile launcher not found.')

    self.dev.set_configuration()
    self.led_off()
    if calibrate:
      self.center()
    else:
      self.inclination = 0
      self.angle = 0
    self.darts_fired = 0

  def _send_command(self, subsystem, command, duration):
    self.dev.ctrl_transfer(0x21,0x09,0,0,[subsystem,command,0x00,0x00,0x00,0x00,0x00,0x00])
    if duration is not None:
      time.sleep(duration)
      self.stop()

  def calibrate(self):
    self.center()

  def center(self):
    self.stop()
    self._left(duration=7)
    self._right(duration=2.75)
    self._up(duration=1.0)
    self._down(duration=0.40)
    self.inclination = 0
    self.angle = 0

  def _up(self, duration):
    self._send_command(0x02, 0x02, duration)

  def _down(self, duration):
    self._send_command(0x02, 0x01, duration)

  def _left(self, duration):
    self._send_command(0x02, 0x04, duration)

  def _right(self, duration):
    self._send_command(0x02, 0x08, duration)

  def up(self):
    if self.inclination >= Launcher.MAX_INCLINATION:
      return

    self._send_command(0x02, 0x02, 0.1)
    self.inclination = min(self.inclination + 1, Launcher.MAX_INCLINATION)

  def down(self):
    if self.inclination <= Launcher.MIN_INCLINATION:
      return

    self._send_command(0x02, 0x01, 0.1)
    self.inclination = max(self.inclination - 1, Launcher.MIN_INCLINATION)

  def left(self):
    if self.angle <= Launcher.MIN_ANGLE:
      return

    self._send_command(0x02, 0x04, 0.2)
    self.angle = max(self.angle - 1, Launcher.MIN_ANGLE)

  def right(self):
    if self.angle >= Launcher.MAX_ANGLE:
      return

    self._send_command(0x02, 0x08, 0.2)
    self.angle = min(self.angle + 1, Launcher.MAX_ANGLE)

  def stop(self):
    self._send_command(0x02, 0x20, None)

  def fire(self):
    self._send_command(0x02, 0x10, 3.0)
    self.darts_fired += 1

  def led_on(self):
    self._send_command(0x03, 0x01, None)
    self.led = 1

  def led_off(self):
    self._send_command(0x03, 0x00, None)
    self.led = 0

