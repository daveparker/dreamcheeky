#!/usr/bin/env python

import cmd
from launcher import Launcher

launcher = Launcher(calibrate=False)

class LauncherCli(cmd.Cmd):
    """Simple launch controller."""
    
    prompt = 'DreamCheeky> '
    def do_up(self, line):
      launcher.up()

    def do_down(self, line):
      launcher.down()

    def do_left(self, line):
      launcher.left()
    
    def do_right(self, line):
      launcher.right()

    def do_center(self, line):
      launcher.center()

    def do_calibrate(self, line):
      launcher.calibrate()

    def do_fire(self, line):
      launcher.fire()

    def do_led(self, line):
      if line.lower() == 'on':
         launcher.led_on()
      elif line.lower() == 'off':
         launcher.led_off()
    
    def do_exit(self, line):
        return True

    def do_quit(self, line):
        return True

    def do_EOF(self, line):
        return True


if __name__ == '__main__':
    LauncherCli().cmdloop()


