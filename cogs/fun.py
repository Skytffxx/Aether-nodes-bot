import discord
from discord.ext import commands
import random
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="flipcoin", description="Flip a coin")
    async def flip_coin(self, interaction: discord.Interaction):
        result = random.choice(["Heads", "Tails"])
        embed = discord.Embed(title="Coin Flip", description=f'The coin landed on: **{result}**', color=discord.Color.gold())
        await interaction.response.send_message(embed=embed)
        logger.info(f'User  {interaction.user.id} flipped a coin and got {result}.')

    @discord.app_commands.command(name="slots", description="Play a slot machine game")
    async def slots(self, interaction: discord.Interaction):
        symbols = ["🍒", "🍋", "🍊", "🍉", "⭐", "💎"]
        result = [random.choice(symbols) for _ in range(3)]
        embed = discord.Embed(title="Slots", description=f'| {" | ".join(result)} |', color=discord.Color.green())

        if result[0] == result[1] == result[2]:
            embed.add_field(name="Result", value="🎉 You win! 🎉", inline=False)
        else:
            embed.add_field(name="Result", value="😢 You lose. Try again!", inline=False)

        await interaction.response.send_message(embed=embed)
        logger.info(f'User  {interaction.user.id} played slots and got: {" | ".join(result)}.')

    @discord.app_commands.command(name="gamble", description="Gamble a certain amount of coins")
    async def gamble(self, interaction: discord.Interaction, amount: int):
        if amount <= 0:
            await interaction.response.send_message("You must gamble a positive amount.", ephemeral=True)
            return

        # Simulate a 50/50 chance to win or lose
        if random.choice([True, False]):
            embed = discord.Embed(title="Gamble Result", description=f'You gambled **{amount}** coins and won! 🎉', color=discord.Color.green())
        else:
            embed = discord.Embed(title="Gamble Result", description=f'You gambled **{amount}** coins and lost. 😢', color=discord.Color.red())

        await interaction.response.send_message(embed=embed)
        logger.info(f'User  {interaction.user.id} gambled {amount} coins.')

async def setup(bot):
    await bot.add_cog(Fun(bot))