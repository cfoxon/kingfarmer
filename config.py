import json
import os.path


try:
  with open(os.path.expanduser('~/kingofh.json')) as settings_file:
    settings = json.load(settings_file)
except:
  with open('defaults.json') as settings_file:
    settings = json.load(settings_file)

def saveSettings():
  try:
    with open(os.path.expanduser('~/kingofh.json'), 'w') as settings_file:
      json.dump(settings, settings_file)
  except:
   print(" Err: Could not save settings " )
