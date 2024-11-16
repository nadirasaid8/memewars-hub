import os
import asyncio
import json
import re
import aiohttp
import random
from colorama import *
from urllib.parse import quote, unquote, parse_qs
from src.deeplchain import kng, pth, hju, mrh, bru, htm, countdown_timer, log, _banner, _clear, read_config, log_error

init(autoreset=True)

class MemesWarBot:
    def __init__(self):
        self.config = read_config()
        self.base_url = "https://memes-war.memecore.com/api"
        self.referral_code = 'RXGT3R'
        self.guild_id = self.config.get('guild_id', '07c2382c-1258-4f77-a57c-9f64caa82c1e')
        self.query_id_user_agent_map = {}
        self.proxies = self.load_proxies()

        with open('src/lock-agent.txt', 'r') as file:
            self.user_agents = file.read().strip().split('\n')

        with open('data.txt', 'r') as file:
            self.query_ids = file.read().strip().split('\n')

    def load_proxies(self):
        proxies_file = os.path.join(os.path.dirname(__file__), './proxies.txt')
        formatted_proxies = []
        with open(proxies_file, 'r') as file:
            for line in file:
                proxy = line.strip()
                if proxy:
                    if proxy.startswith("socks5://"):
                        formatted_proxies.append(proxy)
                    elif not (proxy.startswith("http://") or proxy.startswith("https://")):
                        formatted_proxies.append(f"http://{proxy}")
                    else:
                        formatted_proxies.append(proxy)
        return formatted_proxies
    
    def is_valid_user_agent(self, user_agent):
        if not user_agent or not isinstance(user_agent, str):
            return False
        forbidden_chars_regex = r'[\n\r\t\b\f\v]'
        return not bool(re.search(forbidden_chars_regex, user_agent))

    def get_random_user_agent(self):
        random_user_agent = None
        while not random_user_agent or not self.is_valid_user_agent(random_user_agent):
            random_user_agent = random.choice(self.user_agents).strip()
        return random_user_agent

    async def get_user_info(self, query_id, proxy, session):
        try:
            encoded_query_id = quote(query_id)
            headers = {
                'Cookie': f'telegramInitData={encoded_query_id}',
                'User-Agent': self.query_id_user_agent_map.get(query_id)
            }
            
            async with session.get(f'{self.base_url}/user', headers=headers, proxy=proxy) as response:
                response.raise_for_status()
                data = await response.json()
                return data
        except aiohttp.ClientError as error:
            log(mrh + f'Error getting user info: detail on last.log!')
            log_error(f"{error}")

    async def set_referral_code(self, query_id, user_info, proxy, session):
        if user_info and user_info.get('inputReferralCode') is None:
            try:
                encoded_query_id = quote(query_id)
                headers = {
                    'Cookie': f'telegramInitData={encoded_query_id}',
                    'User-Agent': self.query_id_user_agent_map.get(query_id)
                }
                url = f'{self.base_url}/user/referral/{self.referral_code}'
                async with session.put(url, headers=headers, proxy=proxy) as response:
                    response.raise_for_status()
            except aiohttp.ClientError as error:
                log(mrh + f'Error setting referral detail on last.log!')
                log_error(f"{error}")
        else:
            log(kng + f'Referral code already set.')

    async def check_rewards(self, query_id, proxy, session):
        try:
            encoded_query_id = quote(query_id)
            headers = {
                'Cookie': f'telegramInitData={encoded_query_id}',
                'User-Agent': self.query_id_user_agent_map.get(query_id)
            }
            async with session.get(f'{self.base_url}/quest/treasury/rewards', headers=headers, proxy=proxy) as response:
                response.raise_for_status()
                data = await response.json()
                amazen = data.get('data')
                return amazen
        except aiohttp.ClientError as error:
            log(mrh + f'Error checking rewards: detail on last.log!')
            log_error(f"{error}")

    async def claim_rewards(self, query_id, rewards, proxy, session):
        try:
            encoded_query_id = quote(query_id)
            headers = {
                'Cookie': f'telegramInitData={encoded_query_id}',
                'User-Agent': self.query_id_user_agent_map.get(query_id)
            }
            payload = {
                'data': rewards
            }
            async with session.post(f'{self.base_url}/quest/treasury', json=payload, headers=headers, proxy=proxy) as response:
                response.raise_for_status()
                data = await response.json()
                rewards_data = data.get('data', {}).get('rewards', [])
                if rewards_data:
                    reward_details = ', '.join([f'{reward["rewardAmount"]} {reward["rewardType"]}' for reward in rewards_data])
                    log(hju + f'Treasury rewards claimed: {pth}{reward_details}')
                else:
                    log(kng + 'No rewards data found in the response.')
        except aiohttp.ClientError as error:
            log(mrh + f'Error claiming rewards: detail on last.log!')
            log_error(f"{error}")

    async def check_in(self, query_id, proxy, session):
        try:
            encoded_query_id = quote(query_id)
            headers = {
                'Cookie': f'telegramInitData={encoded_query_id}',
                'User-Agent': self.query_id_user_agent_map.get(query_id)
            }
            async with session.post(f'{self.base_url}/quest/check-in', headers=headers, proxy=proxy) as response:
                response_content = await response.text()
                response.raise_for_status()
                data = await response.json()
                user_data = data.get('data', {}).get('user', None)
                consecutive_check_in = data.get('data', {}).get('currentConsecutiveCheckIn', 0)
                rewards = data.get('data', {}).get('rewards', [])

                if user_data:
                    log(f"User info: {user_data}")
                log(hju + f"Current Consecutive Check-In: {consecutive_check_in}")
                for reward in rewards:
                    log(hju + f"Reward: {pth}{reward['rewardType']} {hju}- Amount: {pth}{reward['rewardAmount']}")

                return user_data, consecutive_check_in, rewards if rewards else None
            
        except aiohttp.ClientResponseError as e:
            if e.status == 409:
                if "Internal Server error" in response_content:
                    log(kng + "User has already checked in today or server error!")
                else:
                    log(bru + f"Check-in conflict: detail on last.log!")
                    log_error(f"{response_content}")
            else:
                log(mrh + f"Error during check-in {e.status}: detail on last.log!")
                log_error(f"{e.message}")

            return None, None, None

        except Exception as e:
            log(mrh + f"Unexpected error during check-in: detail on last.log!")
            log_error(f"{str(e)}")
            return None, None, None

    async def process_task(self, query_id, task_type, quest_id, status, proxy, session, rewards=None):
        encoded_query_id = quote(query_id)
        headers = {
            'Cookie': f'telegramInitData={encoded_query_id}',
            'User-Agent': self.query_id_user_agent_map.get(query_id)
        }
        url = f'{self.base_url}/quest/{task_type}/{quest_id}/progress'
        rewards = rewards or [] 
        payload = {
            'data': {
                'status': status,
                'rewards': rewards
            }
        }

        try:
            async with session.post(url, json=payload, headers=headers, proxy=proxy) as response:
                response.raise_for_status()
                data = await response.json()
                return data
        except aiohttp.ClientError as error:
            log(mrh + f'Error processing task ({task_type}) detail on last.log!')
            log_error(f"{error}")
            return None

    async def get_quest_list(self, query_id, proxy, session, task_type='daily'):
        encoded_query_id = quote(query_id)
        headers = {
            'Cookie': f'telegramInitData={encoded_query_id}',
            'User-Agent': self.query_id_user_agent_map.get(query_id)
        }

        try:
            async with session.get(f'{self.base_url}/quest/{task_type}/list', headers=headers, proxy=proxy) as response:
                response.raise_for_status()
                data = await response.json()
                amazex = data.get('data', {}).get('quests', [])
                return amazex
        except aiohttp.ClientError as error:
            log(mrh + f'Error fetching {task_type} detail on last.log!')
            log_error(f"{error}")
            return []

    async def process_quests(self, query_id, proxy, session, task_type='daily'):
        quests = await self.get_quest_list(query_id, proxy, session, task_type)
        if not quests:
            log(kng + f'No {task_type} quests available')
            return

        for quest in quests:
            quest_id = quest.get('id')
            if not quest_id:
                continue

            log(hju + f'Processing {task_type.capitalize()} {hju}Quest: {pth}{quest["title"]} {hju}(ID: {quest_id})')

            if quest['status'] == 'GO':
                verify_response = await self.process_task(query_id, task_type, quest_id, 'VERIFY', proxy, session)
                if verify_response:
                    log(hju + f'Task verified: {pth}{quest["title"]}')

                    await asyncio.sleep(5)

                    claim_response = await self.process_task(query_id, task_type, quest_id, 'CLAIM', proxy, session)
                    if claim_response:
                        rewards = quest.get('rewards', [])
                        if rewards:
                            await self.process_task(query_id, task_type, quest_id, 'DONE', proxy, session, rewards)
                            log(hju + f'Rewards claimed for {pth}{quest["title"]}')

            elif quest['status'] == 'VERIFY':
                claim_response = await self.process_task(query_id, task_type, quest_id, 'CLAIM', proxy, session)
                if claim_response:
                    log(hju + f'Task claimed: {pth}{quest["title"]}')

                    await asyncio.sleep(5)

                    rewards = quest.get('rewards', [])
                    if rewards:
                        await self.process_task(query_id, task_type, quest_id, 'DONE', proxy, session, rewards)
                        log(hju + f'Rewards claimed for {pth}{quest["title"]}')

            elif quest['status'] == 'CLAIM':
                claim_reward_response = await self.process_task(query_id, task_type, quest_id, 'DONE', proxy, session, quest.get('rewards', []))
                if claim_reward_response:
                    log(hju + f'Rewards claimed for {quest["title"]}')

            elif quest['status'] in ['DONE', 'IN_PROGRESS']:
                log(bru + f'Skipping task: {pth}{quest["title"]} {hju}(Status: {quest["status"]})')

            else:
                log(kng + f'Unknown status for quest: {quest["title"]}')

    def round_to_nearest(self, value, round_to=1000):
        return round(value / round_to) * round_to

    async def get_warbond_tokens(self, query_id, proxy, session):
        try:
            encoded_query_id = quote(query_id)
            headers = {
                'Cookie': f'telegramInitData={encoded_query_id}',
                'User-Agent': self.query_id_user_agent_map.get(query_id)
            }
            async with session.get(f'{self.base_url}/user', headers=headers, proxy=proxy) as response:
                response.raise_for_status()
                data = await response.json()
                warbond_tokens = data.get('data', {}).get('user', {}).get('warbondTokens', 0)
                
                return int(warbond_tokens)
        except aiohttp.ClientError as error: 
            log(mrh + f'Error fetching warbond detail on last.log!')
            log_error(f"{error}")
            return 0  

    async def donate_warbond_to_guild(self, query_id, warbond_tokens, proxy, session):
        try:
            if warbond_tokens <= 0:
                log(kng + "No Warbond tokens to donate.")
                return

            rounded_warbond_tokens = self.round_to_nearest(warbond_tokens, 1000)
            if rounded_warbond_tokens != warbond_tokens:
                log(f"Rounded warbond tokens: {warbond_tokens} -> {rounded_warbond_tokens}")

            encoded_query_id = quote(query_id)
            headers = {
                'Cookie': f'telegramInitData={encoded_query_id}',
                'origin': 'https://memes-war.memecore.com/',
                'referer': 'https://memes-war.memecore.com/guild',
                'User-Agent': self.query_id_user_agent_map.get(query_id),
                'Content-Type': 'application/json' 
            }

            payload = {
                'guildId': self.guild_id,
                'warbondCount': warbond_tokens
            }

            log(hju + f"Sending donation to guild: {pth}{self.guild_id}")
            async with session.post(f'{self.base_url}/guild/warbond', json=payload, headers=headers, proxy=proxy) as response:
                response.raise_for_status()
                data = await response.json()
                amazex = data.get('data')

                if amazex is None:
                    log(hju + f"Donation of {pth}{rounded_warbond_tokens} {hju}Warbond to guild was successful.")
                else:
                    log(bru + f"Error during donation. Detail on last.log!")
                    log_error(f"Response Data: {data}, Full Response: {response.text()}")

        except aiohttp.ClientError as error:
            log(mrh + f'Error donating warbond. Check last.log!')
            log_error(f"{error}")

    async def main(self):
        use_proxy = self.config.get('use_proxy', False)
        auto_complete_task = self.config.get('auto_complete_task', False)
        auto_send_warbond = self.config.get('auto_send_warbond', False)
        account_delay = self.config.get('account_delay', 5)
        countdown_loop = self.config.get('countdown_loop', 3800)
        total = len(self.query_ids)
        proxy_index = 0
        async with aiohttp.ClientSession() as session:
            while True:
                for idx, query_id in enumerate(self.query_ids):
                    decoded_data = unquote(query_id)
                    parsed_data = parse_qs(decoded_data)
                    user_json = parsed_data.get('user', [None])[0]

                    user_info = None
                    proxy = None
                    if user_json:
                        try:
                            user_info = json.loads(user_json)
                        except json.JSONDecodeError as error:
                            log(f'Error parsing user JSON: {error}')

                    username = 'Unknown User'
                    if user_info:
                        username = user_info.get('username', username)

                    if query_id not in self.query_id_user_agent_map:
                        self.query_id_user_agent_map[query_id] = self.get_random_user_agent()

                    log(hju + f'Account: {pth}{idx + 1}/{total}')
                    
                    if use_proxy and self.proxies:
                        proxy = self.proxies[proxy_index]
                        proxy_host = proxy.split('@')[-1]
                        log(hju + f"Proxy: {pth}{proxy_host}")

                        proxy_index = (proxy_index + 1) % len(self.proxies)
                    else:
                        log(pth + "No proxy used or not activate") 

                    log(htm + f"~" * 38)

                    user_info = await self.get_user_info(query_id, proxy, session)            
                    if user_info is not None:
                        user_data = user_info.get('data', {}).get('user')
                        log(hju + f'Username: {pth}{user_data["nickname"]}')
                        log(hju + f'Warbond: {pth}{user_data["warbondTokens"]} {hju}| Honor Point: {pth}{user_data["honorPoints"]} {hju}| Rank: {pth}{user_data["honorPointRank"]}')

                    await self.check_in(query_id, proxy, session)
                    await self.set_referral_code(query_id, user_info, proxy, session)

                    rewards_data = await self.check_rewards(query_id, proxy, session)
                    if rewards_data and rewards_data['leftSecondsUntilTreasury'] == 0:
                        rewards_to_claim = {
                            'rewards': rewards_data['rewards'],
                            'leftSecondsUntilTreasury': 3600,
                            'rewardCooldownSeconds': 3600
                        }
                        await self.claim_rewards(query_id, rewards_to_claim, proxy, session)
                    else:
                        log(kng + 'Treasury Rewards not available yet.')

                    if auto_send_warbond:
                        min_warbond = 1000
                        warbond_tokens = await self.get_warbond_tokens(query_id, proxy, session)

                        if warbond_tokens >= min_warbond:
                            await self.donate_warbond_to_guild(query_id, warbond_tokens, proxy, session)
                        else:
                            log(kng + f'Warbond tokens below minimum threshold {pth}({min_warbond}) {kng}to donate.')

                    if auto_complete_task:
                        await self.process_quests(query_id, proxy, session, 'daily')
                        await self.process_quests(query_id, proxy, session, 'single')
                        
                    log(htm + f"~" * 38)
                    
                    await countdown_timer(account_delay)
                await countdown_timer(countdown_loop)
                proxy_index = 0

if __name__ == "__main__":
    _clear()
    _banner()
    bot = MemesWarBot()
    while True:
        try:
            asyncio.run(bot.main())
        except KeyboardInterrupt as e:
            log(mrh + f"Keyboard omterrupted by users..")
            exit(0)
