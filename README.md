# M3M3WARS BY MM3M3CORE TELEGRAM BOT

this is just a simple code to run m3m3wars telegram which automates, checks in, claims treasury every hour, completes daily tasks and singles (which is only once). can be operated 24/7. for vps / rdp like not fully supported yet (but you try first). 

[TELEGRAM CHANNEL](https://t.me/Deeplchain) | [CONTACT](https://t.me/imspecials)

### Please support me by buying me a coffee: 
```
Binance ID - 46141558
0x705C71fc031B378586695c8f888231e9d24381b4 - EVM
TDTtTc4hSnK9ii1VDudZij8FVK2ZtwChja - TRON
UQBy7ICXV6qFGeFTRWSpnMtoH6agYF3PRa5nufcTr3GVOPri - TON
```

## REGISTRATIONS (POTENTIAL BIG $M TOKEN AIRDROP)
All users can send their acquired $War.bond to Guilds as Raid funding. The Honor points received as a token of appreciation represent your contribution.

 1. Register : [M3M3 WARS BY M3M3CORE](https://t.me/Memes_War_Start_Bot/MemesWar?startapp=RXGT3R)
 2. Click 'Start' & Claim $War.Bond
 3. Click 'Check in' Daily
 4. Bind Code "RXGT3R"
 5. Complete Available Quest
 6. Search "Deeplchain" Guild
 7. Send Some "$War.Bond" to Guild
 8. Collect $War.Bond / Hours

## Features
- Daily Check-in Feature to sign in.
- Claim Tresury Every 1 Hours
- Completes All Daily And Single Quest.
- Automatic Send $WarBond to Guild (Earn AIRDROP Point)
- Proxy support for multiple accounts.
- Configurable through `config.json`.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/nadirasaid8/memewars-hub.git
   cd memewars-hub
      ```
2. **Create a virtual environment (optional but recommended)**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**

The bot uses Python 3 and requires some external libraries. You can install them using:

  ```bash
    pip install -r requirements.txt
  ```

### Dependencies include:

   ```txt
aiohttp==3.8.1
colorama==0.4.6
   ```

## Configuration Setup:

Create a `config.json` file in the project root directory:

   ```json
   {
      "use_proxy": false,
      "guild_id": "07c2382c-1258-4f77-a57c-9f64caa82c1e",
      "auto_complete_task": false,
      "auto_send_warbond": false,
      "account_delay": 5,
      "countdown_loop": 3800
   }
   ```
- `use_proxy`: Enable/disable proxy usage (true/false).
- `auto_complete_task`: Enable/disable automatic task completion (true/false).
- `account_delay`: Delay (in seconds) between processing each account.
- `countdown_loop`: Time (in seconds) before restarting the bot cycle.

## Query Setup:

Add your m3m3wars account tokens to a file named `data.txt` in the root directory. Each token should be on a new line.

1. Use PC/Laptop or Use USB Debugging Phone
2. open the `m3m3wars telegram bot`
3. Inspect Element `(F12)` on the keyboard
4. at the top of the choose "`Application`" 
5. then select "`Session Storage`" 
6. Select the links of "`m3m3wars`" and "`tgWebAppData`"
7. Take the value part of "`tgWebAppData`"
8. take the part that looks like this: 

```txt 
query_id=xxxxxxxxx-Rxxxxxxx&hash=xxxxxxxxxxx
```
9. add it to `data.txt` file or create it if you dont have one


You can add more and run the accounts in turn by entering a query id in new line like this:
```txt
query_id=xxxxxxxxx-Rxxxxxxx&hash=xxxxxxxxxxx
query_id=xxxxxxxxx-Rxxxxxxx&hash=xxxxxxxxxxx
```

### Proxy Setup (Optional):

If you enable proxy support in `config.json`, create a `proxies.txt` file in the root directory, containing a list of proxies, one per line.

Example (proxy format: username:password@host:port):

   ```graphql
user1:pass1@123.123.123.123:8080
user2:pass2@456.456.456.456:8080
   ```

## Usage
Run the script with:

   ```bash
python main.py
   ```

***The bot will:***

Load the accounts from `data.txt`.
Process each account by fetching user info, performing daily sign-in, opening all boxes, executing quacks, and completing tasks (if enabled).

## License
This project is licensed under the `MIT License`.

## Contact
For questions or support, please contact [ https://t.me/DeeplChain ]