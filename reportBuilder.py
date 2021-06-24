import engineApi
from operator import getitem

seed_region = {}
seed_region['Acapulco Gold'] = 'Mexico'
seed_region['Aceh'] = 'Asia'
seed_region['Afghani'] = 'Afghanistan'
seed_region['Colombian Gold'] = 'South America'
seed_region['Durban Poison'] = 'Africa'
seed_region['Hindu Kush'] = 'Afghanistan'
seed_region['Kilimanjaro'] = 'Africa'
seed_region['King’s Bread'] = 'Jamaica'
seed_region['Lamb’s Bread'] = 'Jamaica'
seed_region['Lashkar Gah'] = 'Afghanistan'
seed_region['Malawi'] = 'Africa'
seed_region['Mazar I Sharif'] = 'Afghanistan'
seed_region['Panama Red'] = 'South America'
seed_region['Swazi Gold'] = 'Africa'
seed_region['Thai'] = 'Asia'
seed_region['Thai Chocolate'] = 'Asia'

def format_number(number):
  formatted_number = "{:_}".format(number).replace("_","'")
  return formatted_number

def get_planted_by_spt(count,account,spt):
  propquery = {}
  propquery['account'] = account
  propquery['properties.TYPE'] = 'seed'
  propquery['properties.SPT'] = spt
  propquery['properties.PLANTED'] = True

  seeds = engineApi.get_nft(count, propquery)

  return seeds


def empty_plots(account):
  propquery = {}
  propquery['account'] = account
  propquery['properties.TYPE'] = 'plot'
  propquery['properties.OCCUPIED'] = False

  plots = engineApi.get_nft(850, propquery)

  return plots

def unplanted_seedids_by_region(account):
  propquery = {}
  propquery['account'] = account
  propquery['properties.TYPE'] = 'seed'

  unplanted_seed_region = {}

  all_seeds = engineApi.get_nft(2500, propquery)
  for result in all_seeds:
    for card in result:
      name = card['properties']['NAME']
      if "PLANTED" not in card['properties']:
        region = seed_region[name]
        card['properties']['REGION'] = region
        if region not in unplanted_seed_region:
          unplanted_seed_region[region] = []
        unplanted_seed_region[region].append(str(card['_id']))

  return unplanted_seed_region

def plantables(account):
  seedids_by_region = unplanted_seedids_by_region(account)
  plots = empty_plots(account)

  plotids_by_region = {}
  for result in plots:
    for card in result:
      name = card['properties']['NAME']
      if name not in plotids_by_region:
        plotids_by_region[name] = []
      plotids_by_region[name].append(str(card['_id']))
  plantable = 0
  to_plant = {}
  for region in plotids_by_region:
    region_plantable = {}
    if region in seedids_by_region:
      plantable = min(len(seedids_by_region[region]), len(plotids_by_region[region]))
      seedids_by_region[region] = seedids_by_region[region][ 0 : plantable ]
      plotids_by_region[region] = plotids_by_region[region][ 0 : plantable ]
      region_plantable = dict(zip(plotids_by_region[region], seedids_by_region[region]))
    to_plant = {**to_plant, **region_plantable}

  return to_plant

def planted_by_region(account, spt):
  cards = get_planted_by_spt(850, account, spt)
  region_data = {}
  for result in cards:
    for seed in result:
      name = seed['properties']['NAME']
      region = seed_region[name]
      seed['properties']['REGION'] = region
  return result

def need_water(account, spt):
  seeds = planted_by_region(account, spt)
  #water_demand = 0
  water_dic = {}
  water_eff = {}
  for seed in seeds:
    if seed['properties']['WATER'] > 0:
      seed['properties']['efficiency'] = seed['properties']['PR'] / seed['properties']['WATER']
      #water_demand += seed['properties']['WATER']
      id = str(seed['_id'])
      water_dic[id] = {}
      water_dic[id]['WATER'] = seed['properties']['WATER']
      water_dic[id]['efficiency'] = seed['properties']['efficiency']

  water_dic = sorted(water_dic.items(), key=lambda x: getitem(x[1], 'efficiency'), reverse=True)

  return water_dic

def ready_to_harvest(account):
  propquery = {}
  propquery['account'] = account
  propquery['properties.TYPE'] = 'seed'
  propquery['properties.SPT'] = 0
  propquery['properties.WATER'] = 0
  propquery['properties.PLANTED'] = True

  cards = engineApi.get_nft(850, propquery)

  seed_id_list = []
  for result in cards:
    for seed in result:
     seed_id_list.append(str(seed['_id']))

  return seed_id_list

def forecast(account,days):
  print("\n")
  for spt in range(days,-1,-1):
    seeds = planted_by_region(account, spt)
    total_plots = 0
    total_water = 0
    total_buds = 0

    region_data = {}

    for seed in seeds:
      name = seed['properties']['NAME']
      region = seed['properties']['REGION']
      water = seed['properties']['WATER']
      buds = seed['properties']['PR']

      total_plots += 1
      total_water += water
      total_buds += buds

      if region not in region_data:
        region_data[region] = [0,0,0]
      region_data[region][0] += 1
      region_data[region][1] += water
      region_data[region][2] += buds

    region_data['Totals'] = [total_plots,total_water,total_buds]

    strDayMod = ''
    if spt > 0:
      strDayMod = " +" + str(spt)
    if len(region_data) > 0:
      print("  Here is the harvesting information for today" + strDayMod + ":\n")
      print ("   {:<15} {:<10} {:<10} {:<10}".format('Region','Plots','Water','BUDS'))
      for k, v in region_data.items():
        plots, water, buds = v
        print ("   {:<15} {:<10} {:<10} {:<10}".format(k, plots, format_number(water), format_number(buds)))
      print("\n")
    else:
      print("  There is nothing to harvest today" + strDayMod + "\n")

def fungibles(account, symbols):
  fungibles_data = engineApi.get_fungibles_balance(account, symbols)
  fungibles_dict = {}
  for result in fungibles_data:
    symbol = result[0]['symbol']
    fungibles_dict[symbol] = {}
    fungibles_dict[symbol]['balance'] = result[0]['balance']
    fungibles_dict[symbol]['stake'] = result[0]['stake']
    fungibles_dict[symbol]['pendingUnstake'] = result[0]['pendingUnstake']
  return fungibles_dict

def print_fungibles(account):
  bal_data = fungibles(account,["HKWATER","BUDS","MOTA"])
  print("\n  HKWATER: " + bal_data['HKWATER']['balance'] + "   BUDS: " + bal_data['BUDS']['balance'] + "    MOTA: " + bal_data['MOTA']['balance'])

#water_dict = need_water("foxon", 0)
#print(water_dict)
