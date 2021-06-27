import time
from beem.transactionbuilder import TransactionBuilder
from beembase.operations import Custom_json
from beem import Hive
from beem.blockchain import Blockchain
from beem.nodelist import NodeList
from getpass import getpass
import reportBuilder

print("Verifying Hive nodes...")
nodelist = NodeList()
nodelist.update_nodes()
nodes = nodelist.get_hive_nodes()
hive = Hive(node=nodes, nobroadcast=False)
#hive.chain_params['chain_id'] = 'beeab0de00000000000000000000000000000000000000000000000000000000'
blockchain = Blockchain(hive)

def unlock_hive_wallet():
  if hive.wallet.locked() == True:
    wallet_password = getpass(" Password to unlock wallet: ")
    hive.wallet.unlock(wallet_password)
    wallet_password = ''

def get_key(account, auth):
  wallet_is_created = hive.wallet.created()
  if wallet_is_created == False:
    create_new_wallet()

  unlock_hive_wallet()
  #check for needed key in hive wallet. If not there add_keys_to_wallet()

def create_new_wallet():
  wallet_is_created = hive.wallet.created()
  if wallet_is_created == True:
    #probably add a confirm before wiping the beem wallet
    hive.wallet.wipe(True)
  new_wallet_password = getpass(" Create a new password for unlocking the wallet (keys will be added later): ")
  hive.wallet.newWallet(new_wallet_password)
  add_keys_to_wallet()

def add_keys_to_wallet():
  print(" Enter the private posting key below to be stored in the wallet ")
  posting_key = getpass(" posting key: ")
  hive.wallet.addPrivateKey(posting_key)
  posting_key = ''
  print("\n Enter the private active key below to be stored in the wallet ")
  active_key = getpass("\n active key: ")
  hive.wallet.addPrivateKey(active_key)
  active_key = ''


def water_seeds(water_dict, account):
  hkwater_balance = int(float(reportBuilder.fungibles(account,["HKWATER"])['HKWATER']['balance']))
  broadcasted = 0
  seeds_to_water = str(len(water_dict))
  for seed in water_dict:
    if seed[1]['WATER'] <= hkwater_balance:
      tx = TransactionBuilder(blockchain_instance=hive)
      payload = {}
      payload['symbol'] = 'HKWATER'
      payload['to'] = 'hk-vault'
      payload['quantity'] = str(seed[1]['WATER']) + ".000"
      payload['memo'] = int(seed[0])
      action = {}
      action['contractName'] = 'tokens'
      action['contractAction'] = 'transfer'
      action['contractPayload'] = payload
      cj = {
        "required_auths": [account],
        "required_posting_auths": [],
        "id": "ssc-mainnet-hive",
        "json": action
      }
      tx.appendOps(Custom_json(cj))
      get_key(account, "active")
      tx.appendSigner(account, "active")
      #tx.appendWif(active)
      signed_tx = tx.sign()
      try:
        #print(tx)
        broadcast_tx = tx.broadcast()
        print(broadcast_tx)
      except Exception as e:
        print(e)
        print(tx)
      broadcasted += 1
      print(" Watered " + str(broadcasted) + " of " + seeds_to_water + ". Please wait...")
      time.sleep(3)
      hkwater_balance -= seed[1]['WATER']
    else:
      print(" Skipping " + seed[0] + ": insufficient balance")



def harvest_seeds(seed_list, account):
  total_to_harvest = len(seed_list)
  harvested = 0
  for seed in seed_list:
    tx = TransactionBuilder(blockchain_instance=hive)
    nfts = {}
    nfts['symbol'] = 'HKFARM'
    nfts['ids'] = [seed]
    payload = {}
    payload['to'] = 'hk-vault'
    payload['nfts'] = [nfts]
    action = {}
    action['contractName'] = 'nft'
    action['contractAction'] = 'transfer'
    action['contractPayload'] = payload
    cj = {
        "required_auths": [account],
        "required_posting_auths": [],
        "id": "ssc-mainnet-hive",
        "json": action
      }
    tx.appendOps(Custom_json(cj))
    get_key(account, "active")
    tx.appendSigner(account, "active")
    #tx.appendWif(active)
    signed_tx = tx.sign()
    #print(tx)
    try:
      #print(signed_tx)
      broadcast_tx = tx.broadcast()
      print(broadcast_tx)
    except Exception as e:
      print(e)
      print(tx)
    harvested += 1
    print("Harvested " + str(harvested) + " of " + str(total_to_harvest) + ". Please wait...")
    time.sleep(3)

def plant(plot_seed_dict, account):
  total_to_plant = len(plot_seed_dict)
  planted = 0
  for key in plot_seed_dict:
    tx = TransactionBuilder(blockchain_instance=hive)
    action = {}
    action['plotID'] = key
    action['seedID'] = plot_seed_dict[key]
    cj = {
        "required_auths": [],
        "required_posting_auths": [account],
        "id": "qwoyn_plant_plot",
        "json": action
      }
    tx.appendOps(Custom_json(cj))
    #tx.appendWif(posting)
    get_key(account, "posting")
    tx.appendSigner(account, "posting")
    signed_tx = tx.sign()
    try:
      broadcast_tx = tx.broadcast()
      print(broadcast_tx)
    except Exception as e:
      print(e)
      print(tx)
    planted += 1
    print("Planted " + str(planted) + " of " + str(total_to_plant) + ". Please wait...")
    time.sleep(3)
