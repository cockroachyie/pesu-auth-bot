import logging
import subprocess
import sys
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands


class DeveloperCog(commands.Cog):
    """
    This cog contains all commands and functionalities available to the bot developers
    """

    def __init__(self, client: commands.Bot, config: dict):
        self.client = client
        self.config = config
        self.developer_user_ids = config["bot"]["developer_user_ids"]
        self.developer_channel_ids = config["bot"]["developer_channel_ids"]
        self.developer_log_channels = [
            self.client.get_channel(channel_id)
            for channel_id in self.developer_channel_ids
        ]

    @staticmethod
    def check_developer_permissions():
        """
        Checks if the user is a developer
        """

        async def predicate(interaction: discord.Interaction):
            return interaction.user.id in interaction.client.cogs["DeveloperCog"].developer_user_ids

        return app_commands.check(predicate)

    @app_commands.command(name="gitpull", description="Pull the latest changes from GitHub")
    @check_developer_permissions()
    async def git_pull(self, interaction: discord.Interaction):
        """
        Pulls the latest changes from the git repository
        """
        await interaction.response.defer()
        logging.info(f"Pulling latest changes from git repository")
        sys.stdout.flush()

        embed = discord.Embed(
            title="Git pull",
            description="Pulling changes from GitHub...",
            color=discord.Color.blue(),
        )
        await interaction.followup.send(embed=embed)

        output = list()
        p = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
        for line in iter(p.stdout.readline, ""):
            if not line:
                break
            line = str(line.rstrip(), "utf-8", "ignore").strip()
            logging.info(line)
            output.append(line)

        output = '\n'.join(output)
        output = f"```bash\n{output}```"
        embed = discord.Embed(
            title="Git pull complete",
            description=output,
            color=discord.Color.green(),
        )
        await interaction.followup.send(embed=embed)
        sys.stdout.flush()

    @app_commands.command(name="sync", description="Sync commands with Discord")
    @check_developer_permissions()
    async def sync_command(self, interaction: discord.Interaction):
        """
        Syncs commands with Discord
        """
        await interaction.response.defer()
        logging.info(f"Synchronizing commands with Discord")
        await self.client.tree.sync()
        embed = discord.Embed(
            title="Commands synced with Discord",
            description="The bot has finished syncing commands with Discord",
            color=discord.Color.green(),
        )
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="log", description="Get the logs of the bot")
    @app_commands.describe(lines="The number of lines to fetch from EOF")
    @check_developer_permissions()
    async def logs(self, interaction: discord.Interaction, lines: Optional[int] = None):
        await interaction.response.defer()
        try:
            lines = int(lines)
        except (TypeError, ValueError):
            lines = None

        if lines is None:
            await interaction.followup.send(file=discord.File(open("bot.log", "rb")))
        else:
            logs = open("bot.log", "r").readlines()
            logs = logs[-lines:]
            logs = f"```log\n{''.join(logs)}```"
            await interaction.followup.send(logs)

    @app_commands.command(name="shutdown", description="Shutdown the bot")
    @check_developer_permissions()
    async def shutdown(self, interaction: discord.Interaction):
        """
        Shuts down the bot
        """
        await interaction.response.defer()
        logging.info(f"Shutting down")
        embed = discord.Embed(
            title="Shutting down",
            description="The bot has been shut down",
            color=discord.Color.red(),
        )
        await interaction.followup.send(embed=embed)
        await self.client.close()

    @app_commands.command(name="restart", description="Restart the bot")
    @check_developer_permissions()
    async def restart(self, interaction: discord.Interaction):
        """
        Restarts the bot
        """
        await interaction.response.defer()
        logging.info(f"Restarting")
        embed = discord.Embed(
            title="Restarting",
            description="The bot has been restarted",
            color=discord.Color.red(),
        )
        await interaction.followup.send(embed=embed)
        subprocess.Popen(["python", "bot/bot.py"])
        await self.client.close()


