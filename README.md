# kingfarmer

python client for hashkings

1. pip (or pip3) install -r requirements.txt
to get dependencies

2. configure wallet in Beem
 - for help getting beem running on your platform, see the Beem repo: https://github.com/holgern/beem
 - once Beem is installed, start beempy
 - 1. `createwallet` to set an unlock password
 - 2. then set keys with one of the two following options:
 - - `importaccount accountname` to import all keys with a master password (beem will call it "passphrase")
 - **OR**
 - - `addkey` and follow the prompts to add the posting key. Then `addkey` again to add the active key

3. python (or python3) main.py


Option 1 will water all planted seeds at SPT: 0
- if the player does not have enough water, watering will maximize for BUDS

Option 2 will harvest all SPT: 0 with WATER: 0

Option 3 will plant the maximum number of seeds

Option 4 shows a 7-day forecast

Option 5 shows a refreshed summary

Option 6 to change to a different account
