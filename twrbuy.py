import engineApi
import broadcasts
import requests
import time
from beem.account import Account

hashkingsApi = 'https://hashkings.xyz'

def get_towers(account):
  print(" Getting list of towers for account...")
  propquery = {}
  propquery['account'] = account
  propquery['properties.TYPE'] = "water"
  result = engineApi.get_nft(3000, propquery)
  twr_dict = {}
  for towers in result:
    for twr in towers:
      twrlvl = twr['properties']['LVL']
      if twrlvl not in twr_dict:
        twr_dict[twrlvl] = []
      twr_dict[twrlvl].append(twr['_id'])
  twr_dict_sorted = dict(sorted(twr_dict.items(), key=lambda item: item[0]))
  return twr_dict_sorted

def costOfTower(targetLvl):
  targetLvl = targetLvl
  res = requests.get(hashkingsApi)
  costs = res.json()['stats']['prices']['waterPlants']['lvl'+str(targetLvl)]['price']

  return round((float(costs)),3)

def playerLevel(account):
  print(" Getting account information from Hashkings...")
  res = requests.get(hashkingsApi+"/utest/"+account)
  level = res.json()['lvl']
  return level

def getMaxUpgradable(level):
  player_level = level//10
  if player_level > 8:
    max_upgradable_from = 9
  else:
    max_upgradable_from = player_level
  return max_upgradable_from

print(" This script will upgrade Hashkings water towers. It will use the Beem wallet\n")
print(" After entering the account name, tower lvl and quantity will be selected before setting a cancel price\n")
print(" Enter the account without the @ ")

#comment out the input line and add name below to skip the input
#account = "foxon"
account = input(" Account name: ")

account_level = playerLevel(account)
max_upgrade_from = getMaxUpgradable(account_level)
tower_dict = get_towers(account)

print(" " + account + " has level " + str(account_level))
print("\n \n Here are the towers that can be upgraded: ")
upgradable_twrs = {}
for lvl in tower_dict:
  if lvl <= max_upgrade_from:
    print(" lvl " + str(lvl) + " tower X " + str(len(tower_dict[lvl])))
    upgradable_twrs[lvl] = tower_dict[lvl]

print("\n What level tower to upgrade from? ")
level_to_upgrade_from = int(input(" Tower lvl : "))
level_to_upgrade_to = level_to_upgrade_from + 1

cost = costOfTower(level_to_upgrade_to)
print("\n The current cost of an upgrade is " + str(cost) + "HIVE")

qty_upgradable = len(tower_dict[level_to_upgrade_from])

print("\n How many to upgrade?")
qty_to_upgrade = int(input(" Number to upgrade from 1 to " + str(qty_upgradable) + ": "))

towers_to_upgrade = []
towers_to_upgrade = upgradable_twrs[level_to_upgrade_from][0:qty_to_upgrade]

#comment out the input line and set max below to skip the input
#max_price = 100
max_price = float(input(" Cancel upgrades if price reaches (in HIVE): "))

broadcasts.unlock_hive_wallet()
hive_account = Account(account, blockchain_instance=broadcasts.hive)

memo_prefix = "water" + str(level_to_upgrade_to) + " "

print("\n")
for tower in towers_to_upgrade:
  cost = costOfTower(level_to_upgrade_to)
  if cost < max_price:
    memo = memo_prefix + str(tower)
    print(" Upgrading " + memo + " for " + str(cost) + " HIVE")
    hive_account.transfer("hashkings", cost, "HIVE", memo)
    time.sleep(3)
