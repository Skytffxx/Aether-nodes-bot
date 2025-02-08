import discord
from discord.ext import commands
import random
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_data = {}  # In-memory storage for user levels and XP

    def get_user_data(self, user_id):
        # Retrieve user data, return default if not found
        return self.user_data.get(user_id, {"level": 1, "xp": 0})

    def update_user_data(self, user_id, xp):
        # Update user XP and level
        if user_id not in self.user_data:
            self.user_data[user_id] = {"level": 1, "xp": 0}
        
        self.user_data[user_id]["xp"] += xp
        
        # Level up if XP exceeds threshold
        if self.user_data[user_id]["xp"] >= 100:  # Example threshold for leveling up
            self.user_data[user_id]["level"] += 1
            self.user_data[user_id]["xp"] = 0  # Reset XP after leveling up
            return True  # Indicate that the user leveled up
        return False  # No level up

    @discord.app_commands.command(name="level", description="Check your current level and XP")
    async def level(self, interaction: discord.Interaction):
        user_data = self.get_user_data(interaction.user.id)
        embed = discord.Embed(
            title=f"{interaction.user.name}'s Level",
            description=f"Level: {user_data['level']}\nXP: {user_data['xp']}/100",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)
        logger.info(f'User  {interaction.user.id} checked their level: {user_data["level"]}.')

    @discord.app_commands.command(name="gainxp", description="Gain XP (for testing purposes)")
    async def gain_xp(self, interaction: discord.Interaction, amount: int):
        if amount <= 0:
            await interaction.response.send_message("You must gain a positive amount of XP.", ephemeral=True)
            return

        leveled_up = self.update_user_data(interaction.user.id, amount)
        if leveled_up:
            await interaction.response.send_message(f'You gained {amount} XP and leveled up! 🎉', ephemeral=True)
        else:
            await interaction.response.send_message(f'You gained {amount} XP.', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Levels(bot))