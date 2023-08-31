# PESU-Auth-Bot

A simple bot to authenticate users in any server using their PESU credentials.

## Usage

### Invite the bot to your server

Use this [link](https://discord.com/api/oauth2/authorize?client_id=1146109578241638593&permissions=1377007037446&scope=bot) to invite the bot to your server.

### Run/Deploy the bot yourself

1. Clone the repository
2. Install the dependencies using `pip install -r requirements.txt`
3. Create a `config.yml` file in the root directory of the project and add the following:
    ```yaml
    bot:
        token: 'your-bot-token'
        developer_user_ids:
            - <discord_developer_id_1>
            - <discord_developer_id_2>
        developer_guild_ids:
            - <discord_developer_guild_id_1>
            - <discord_developer_guild_id_2>
        developer_channel_ids:
            - <discord_developer_channel_id_1>
            - <discord_developer_channel_id_2>

        prefix: 'bot-prefix'
    db: 'path/to/mongo_database/file.db' # if local host - 'mongodb://localhost:27017/'
    ```
4. Run the bot using the `bot.py` file

<hr>

Made with ❤️ by [Space-Gamer](https://github.com/Space-Gamer) and [Aditeya Baral
](https://github.com/aditeyabaral)
