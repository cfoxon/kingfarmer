import aiohttp
import asyncio
import math

rpc = "https://engine.rishipanthee.com"
#rpc = "http://104.238.153.130:5000"

endpoint_contract = "/contracts"
headers = {'content-type': 'application/json'}

def form_contract_query(contract, table, offset, query={}):
  query_contract = {}
  query_contract['method'] = "find"
  query_contract['jsonrpc'] = "2.0"
  query_contract['id'] = 1
  params = {}
  params['contract'] = contract
  params['table'] = table
  params['query'] = query
  params['limit'] = 1000
  params['offset'] = offset
  params['indexes'] = []
  query_contract['params'] = params
  return query_contract

def getOffsetsFromCount(count):
  connections = math.ceil(count / 1000)
  offsets = [(i*1000) for i in range(0,connections)]
  return offsets

def query_list_maker(contract, table, offsets, propquery):
  queries = {}
  for offset in offsets:
    queries[offset] = form_contract_query(contract, table, offset, query = propquery)
  return queries

def query_fungible_list_maker(account, symbols):
  contract = "tokens"
  table = "balances"
  queries = {}
  propquery = {}
  for symbol in symbols:
    queries[symbol] = form_contract_query(contract, table, 0, query = {"account": account, "symbol": symbol})
  return queries

async def fetch_contract(session, query_contract):
  async with session.post(rpc + endpoint_contract, json=query_contract) as res:
    response = await res.json()
    return response['result']
    #response = await res.text()
    #return response

async def fetch_all_contract(queries, loop):
  async with aiohttp.ClientSession(loop=loop, headers=headers) as session:
    results = await asyncio.gather(*[fetch_contract(session, query) for query in queries.values()], return_exceptions=True)
    return results

def get_fungibles_balance(account, symbols):
  queries = query_fungible_list_maker(account, symbols)

  loop = asyncio.get_event_loop()
  data = loop.run_until_complete(fetch_all_contract(queries, loop))

  return data


def get_nft(count,propquery):
  contract = "nft"
  table = "HKFARMinstances"

  offsets = getOffsetsFromCount(count)
  queries = query_list_maker(contract, table, offsets, propquery)

  loop = asyncio.get_event_loop()
  data = loop.run_until_complete(fetch_all_contract(queries, loop))

  return data
