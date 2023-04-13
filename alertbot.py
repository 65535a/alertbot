from mattermostdriver import Driver
import json
import time
import asyncio
from watchfiles import awatch
import os

# Config (change these)

bot_username = 'alertbot'
bot_token = ''
server_url = ''
file_path = "/path/to/log"
file_name = "logfile.log"
team_name = ""
channel_name = ""
alert_string = ""



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
                lines = f.readlines()[-2:]
            for line in lines:
                if alert_string in str(line):
                    send(str(line))
                    print(line)




if __name__ == '__main__':

    asyncio.run(main())

