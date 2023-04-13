from mattermostdriver import Driver
import json
import time
import asyncio
from watchfiles import awatch
import os

# config
bot_username = "alertbot"
bot_token = ""
server_url = ""
file_path = "/path/to/log/"
file_name = "logname.log"
team_name = ""
channel_name = ""
alert_strings = ['string1', 'string2']

def send(msg):
    bot = Driver({'url': server_url, 'login_id': bot_username, 'token': bot_token, 'scheme': 'http'})
    bot.login()

    team = bot.teams.get_team_by_name(team_name)
    channel = bot.channels.get_channel_by_name(team['id'], channel_name)
    bot.posts.create_post({
        'channel_id': channel['id'],
        'message': str(msg)})

async def main():
    async for changes in awatch(file_path):
        if file_name in str(changes):
            with open(file_path+file_name, "rb") as f:
                lines = f.readlines()[-1:]
                for line in lines:
                    for string in alert_strings:
                        if string in str(line):
                            send(line.decode('utf-8'))
                            print(line.decode('utf-8'))


if __name__ == '__main__':

    asyncio.run(main())


