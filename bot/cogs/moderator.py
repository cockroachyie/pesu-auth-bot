import logging

import discord
from discord import app_commands
from discord.ext import commands

from .db import DatabaseCog


class ModeratorCog(commands.Cog):
    """
    This cog contains all commands and functionalities available to server admins
    """

    def __init__(self, client: commands.Bot, db: DatabaseCog):
        self.client = client
        self.db = db

    @app_commands.command(name="ping", description="Perform a ping test")
    @app_commands.default_permissions(administrator=True)
    async def ping(self, interaction: discord.Interaction):
        """
        Performs a ping test
        """
        logging.info(f"Running ping test")
        embed = discord.Embed(
            title="Ping Test",
            description=f"{round(self.client.latency * 1000)} ms",
            color=discord.Color.blue(),
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="setup", description="Setup a verification role for your server")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(role="The role to be used for verification")
    async def setup(self, interaction: discord.Interaction, role: discord.Role):
        """
        Sets up the verification role for the server
        """
        logging.info(f"Setting up verification role for {interaction.guild}")
        await interaction.response.defer()

        existing_verification_role = self.db.get_verification_role_for_server(guild_id=interaction.guild_id)
        if existing_verification_role:
            embed = discord.Embed(
                title="Verification Role Setup Failed",
                description=f"Verification role already set to {existing_verification_role.mention}. "
                            "Use the `/update` command to update the verification role",
                color=discord.Color.red(),
            )
        else:
            self.db.add_verification_role(guild_id=interaction.guild_id, role_id=role.id)
            embed = discord.Embed(
                title="Verification Role Setup Successful",
                description=f"Verification role set to {role.mention}. "
                            "Members can now use the `/auth` command to verify themselves",
                color=discord.Color.green(),
            )
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="remove", description="Remove the verification role for your server")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(deverify="Remove the verification role from existing members")
    @app_commands.choices(deverify=[
        app_commands.Choice(name="Yes", value=1),
        app_commands.Choice(name="No", value=0)
    ])
    async def remove(self, interaction: discord.Interaction, deverify: int = 0):
        """
        Removes the verification role for the server
        """
        logging.info(f"Removing verification role for {interaction.guild}")
        await interaction.response.defer()

        existing_verification_role = self.db.get_verification_role_for_server(guild_id=interaction.guild_id)
        if existing_verification_role:
            existing_verification_role = interaction.guild.get_role(existing_verification_role)
            self.db.remove_verification_role(guild_id=interaction.guild_id)
            embed = discord.Embed(
                title="Verification Role Removal Successful",
                description=f"Verification role {existing_verification_role.mention} removed",
                color=discord.Color.green(),
            )
            if deverify:
                embed.description += f"\n The verification role has been removed from all existing members."
                for member in interaction.guild.members:
                    if existing_verification_role in member.roles:
                        await member.remove_roles(existing_verification_role)

        else:
            embed = discord.Embed(
                title="Verification Role Removal Failed",
                description="No verification role set for this server",
                color=discord.Color.red(),
            )
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="update", description="Update the verification role for your server")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(role="The role to be used for verification")
    @app_commands.describe(reverify="Update the verification role for existing members. Note that this will remove "
                                    "the existing verification role.")
    @app_commands.choices(reverify=[
        app_commands.Choice(name="Yes", value=1),
        app_commands.Choice(name="No", value=0)
    ])
    async def update(self, interaction: discord.Interaction, role: discord.Role, reverify: int = 0):
        """
        Updates the verification role for the server
        """
        logging.info(f"Updating verification role for {interaction.guild}")
        await interaction.response.defer()

        existing_verification_role = self.db.get_verification_role_for_server(guild_id=interaction.guild_id)
        if existing_verification_role:
            existing_verification_role = interaction.guild.get_role(existing_verification_role)
            self.db.add_verification_role(guild_id=interaction.guild_id, role_id=role.id)
            embed = discord.Embed(
                title="Verification Role Update Successful",
                description=f"Verification role updated from {existing_verification_role.mention} to {role.mention}",
                color=discord.Color.green(),
            )
            if reverify:
                embed.description += f"\n The verification role has been updated for all existing members."
                for member in interaction.guild.members:
                    if existing_verification_role in member.roles:
                        await member.remove_roles(existing_verification_role)
                        if role not in member.roles:
                            await member.add_roles(role)

        else:
            embed = discord.Embed(
                title="Verification Role Update Failed",
                description="No verification role set for this server",
                color=discord.Color.red(),
            )
        await interaction.followup.send(embed=embed)
