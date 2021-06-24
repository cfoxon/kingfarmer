print("Starting up...")
import reportBuilder
import broadcasts
import time

def water_all_day_zero(account):
  print("  Refresing water data...")
  to_water = reportBuilder.need_water(account, 0)
  broadcasts.water_seeds(to_water, account)
  menu(account)

def harvest_all(account):
  print("Refreshing harvest data...")
  to_harvest = reportBuilder.ready_to_harvest(account)
  broadcasts.harvest_seeds(to_harvest, account)
  menu(account)

def set_account():
  print("\n Enter the account without the @ (ex: qwoyn)")
  account = input("\n Account: ")
  show_summary(account)

def show_summary(account):
  canPlant = len(reportBuilder.plantables(account))
  reportBuilder.forecast(account, 0)
  print("  " + str(canPlant) + " can be planted")
  reportBuilder.print_fungibles(account)
  menu(account)

def get_forecast(account):
  print(" " + account)
  reportBuilder.forecast(account, 7)
  menu(account)

def plant_all(account):
  plot_seed_dict = reportBuilder.plantables(account)
  broadcasts.plant(plot_seed_dict, account)
  menu(account)

def the_secret(account):
  to_water = reportBuilder.need_water(account, 0)
  broadcasts.water_seeds(to_water, account)
  print("  Watering complete. Pausing for 5 minutes before harvesting...")
  time.sleep(300)
  to_harvest = reportBuilder.ready_to_harvest(account)
  broadcasts.harvest_seeds(to_harvest, account)
  print("  Harvest complete. Pausing for 5 minutes before planting...")
  time.sleep(300)
  plot_seed_dict = reportBuilder.plantables(account)
  broadcasts.plant(plot_seed_dict, account)
  print("  Planting complete")
  show_summary(account)

def menu(account):
  print("\n Enter activity for " + account + ":")
  print("  1 to water \n  2 to harvest \n  3 to plant \n  4 to see forecast \n  5 to refresh \n  6 to change accounts \n  7 to exit")
  todo = input("\n Choice: ")

  if todo == '1':
    water_all_day_zero(account)
  elif todo == '2':
    harvest_all(account)
  elif todo == '3':
    plant_all(account)
  elif todo == '4':
    get_forecast(account)
  elif todo == '5':
    show_summary(account)
  elif todo == '6':
    account = set_account()
  elif todo == 'wallet':
    broadcasts.create_new_wallet()
    menu(account)
  elif todo == 'doall':
    the_secret(account)

account = set_account()
