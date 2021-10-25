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
  print("\n Enter the account name")
  account = input("\n Account: @")
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
  plot_seed_dict = reportBuilder.plantables_by_region(account)
  plantables = {}
  for region in plot_seed_dict:
    plantables = {**plantables, **plot_seed_dict[region]}
  broadcasts.plant(plantables, account)
  menu(account)

def plant_region(region, account):
  plot_seed_dict = reportBuilder.plantables_by_region(account)
  plantables = {}
  plantable_count = 0
  try:
    plantable_count = len(plot_seed_dict[region])
  except:
    print(" Nothing to plant in", region)

  if plantable_count > 0:
    plantables = plot_seed_dict[region]
    broadcasts.plant(plantables, account)
  planting_menu(account)

def water_region(region, account):
  print("Chose to water", region)
  water_region_menu(account)

def water_spt(spt, account):
  print("Chose to water spt", spt)
  water_spt_menu(account)

def water_all_all(account):
  print("  Refresing water data...")
  for day in range(8):
    to_water = reportBuilder.need_water(account, day)
    broadcasts.water_seeds(to_water, account)
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
  print("  1 to water the harvest \n  2 to harvest \n  3 to plant max \n  4 to see forecast \n  5 to refresh \n  6 for advanced \n  7 to exit")
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
    advanced_menu(account)
  elif todo == 'wallet':
    broadcasts.create_new_wallet()
    menu(account)
  elif todo == 'doall':
    the_secret(account)
  elif todo == 'waterall':
    water_all_all(account)

def advanced_menu(account):
  print("\n Enter activity for " + account + ":")
  print("  1 to plant by region")
  #print("  2 to water by region")
  #print("  3 to water by SPT")
  print("  4 to change accounts")
  print("  5 to return to main menu")
  todo = input("\n Choice: ")

  if todo == '1':
    planting_menu(account)
  #elif todo == '2':
  #  water_region_menu(account)
  #elif todo == '3':
  #  water_spt_menu(account)
  elif todo == '4':
    account = set_account()
  elif todo == '5':
    menu(account)

def planting_menu(account):
  print("Getting planting information...")
  plot_seed_dict = reportBuilder.plantables_by_region(account)
  region_list = ["Asia", "Jamaica", "Africa", "Afghanistan", "Mexico", "South America"]
  region_plantable_counts = {}
  for region in region_list:
    region_plantable_counts[region] = 0
    if region in plot_seed_dict:
      region_plantable_counts[region] += len(plot_seed_dict[region])
  print("\n Choose region to plant maximum seeds for ", account, ":")
  print(f"  1 Asia ({region_plantable_counts['Asia']} to plant)")
  print(f"  2 Jamaica ({region_plantable_counts['Jamaica']} to plant)")
  print(f"  3 Africa ({region_plantable_counts['Africa']} to plant)")
  print(f"  4 Afghanistan ({region_plantable_counts['Afghanistan']} to plant)")
  print(f"  5 Mexico ({region_plantable_counts['Mexico']} to plant)")
  print(f"  6 South America ({region_plantable_counts['South America']} to plant)")
  print(f"  7 Return to advanced menu")
  todo = input("\n Choice: ")

  if todo == '1':
    plant_region("Asia", account)
  elif todo == '2':
    plant_region("Jamaica", account)
  elif todo == '3':
    plant_region("Africa", account)
  elif todo == '4':
    plant_region("Afghanistan", account)
  elif todo == '5':
    plant_region("Mexico", account)
  elif todo == '6':
    plant_region("South America", account)
  elif todo == '7':
    advanced_menu(account)

def water_region_menu(account):
  print("\n Choose region to water maximum for ", account, ":")
  print("  1 Asia \n  2 Jamaica \n  3 Africa \n  4 Afghanistan \n  5 Mexico \n  6 South America \n  7 Return to advanced menu")
  todo = input("\n Choice: ")

  if todo == '1':
    water_region("Asia", account)
  elif todo == '2':
    water_region("Jamaica", account)
  elif todo == '3':
    water_region("Africa", account)
  elif todo == '4':
    water_region("Afghanistan", account)
  elif todo == '5':
    water_region("Mexico", account)
  elif todo == '6':
    water_region("South America", account)
  elif todo == '7':
    advanced_menu(account)

def water_spt_menu(account):
  print("\n Choose region to water maximum for ", account, ":")
  print("  1 Asia \n  2 Jamaica \n  3 Africa \n  4 Afghanistan \n  5 Mexico \n  6 South America \n  7 Return to advanced menu")
  todo = input("\n Choice: ")

  if todo == '1':
    water_spt("1", account)
  elif todo == '2':
    water_spt("2", account)
  elif todo == '3':
    water_spt("3", account)
  elif todo == '4':
    water_spt("4", account)
  elif todo == '5':
    water_spt("5", account)
  elif todo == '6':
    water_spt("6", account)
  elif todo == '7':
    water_spt("7", account)
  elif todo == '8':
    advanced_menu(account)

account = set_account()
