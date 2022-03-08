"""
This file is a heavily modified version of https://github.com/x4nth055/pythoncode-tutorials/tree/master/ethical-hacking/keylogger

The original code is licensed under the MIT license (https://github.com/x4nth055/pythoncode-tutorials/blob/master/LICENSE).
This means that we can use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the original code, as long as we give credit to the original author and include the license in our final product.
"""


import re
import keyboard
import asyncio

class splitWatcher:
  def __init__(self):
    print("Split Key Watcher | ON")

    # TODO: make this configurable with pysimple GUI
    self.split_key = input("Enter the key to split: ")
    self.exit_key = input("Enter the key to exit the program: ")

    self.setup = False
    self.exit_program = False

  def callback(self, event):
    name = event.name
    if self.split_key == '!@#$%^&*()': 
      self.split_key = name
    elif self.exit_program:
      self.exit_program = True
      del self
    elif name == self.split_key:
      # TODO: Integrate this with pysimple GUI to save the current time to a csv file
      print(self.split_key + " | was pressed and you have split")
    elif name == self.exit_key:
      print(self.exit_key + " | was pressed and you have exited the program")
      self.exit_program = True

  async def endProgram(self):
    while not self.exit_program:
      await asyncio.sleep(0.1)
    return 1
      
  async def start(self):
    # start the keylogger
    keyboard.on_release(callback=self.callback)
    # block the current thread, wait until CTRL+C is pressed
    await self.endProgram()

    print("END")

    
if __name__ == "__main__":
  # if you want a keylogger to send to your email
  # keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
  # if you want a keylogger to record keylogs to a local file 
  # (and then send it using your favorite method)
  split = splitWatcher()
  asyncio.run(split.start())
  print("Split Key Watcher | OFF")
  del split