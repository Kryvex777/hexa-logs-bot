# By 💜 Hexa Studios 🌐 discord.gg/ezGvtVJvWk
import discord
from discord import app_commands
from discord.ext import commands

# 🔴 CAMBIA QUESTO LINK CON IL TUO LOGO! 🔴
HEXA_LOGO_URL = "https://cdn.discordapp.com/attachments/1511779633010442295/1515361038281871471/Hexa_Studios_logo.png?ex=6a2eb971&is=6a2d67f1&hm=802d5f1de131418ae7dfdf432c272f3de7522dc1e2ab6d0f82645ce1291c988a&"

class HexaStudiosCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="hexastudios", description="Show information about Hexa Studios")
    async def hexastudios(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="💜 By Hexa Studios",
            description="**Your trusted Discord bot development team!**\n\nWe create high-quality, open-source Discord bots for everyone. This log bot is one of our many projects.",
            color=0x9B59B6
        )
        embed.add_field(
            name="👨‍💻 Developers",
            value="💜 Hexa Studios Development Team",
            inline=False
        )
        embed.add_field(
            name="🌐 Join Our Community",
            value="https://discord.gg/ezGvtVJvWk",
            inline=False
        )
        embed.add_field(
            name="📦 Current Bot",
            value="Advanced Log Bot - Track all server activities",
            inline=False
        )
        embed.add_field(
            name="🔗 GitHub",
            value="[github.com/hexastudios](https://github.com/Kryvex777)",
            inline=False
        )
        # 🔴 QUESTA RIGA METTE IL LOGO IN ALTO A DESTRA 🔴
        embed.set_thumbnail(url=HEXA_LOGO_URL)
        embed.set_footer(text="Thanks for using Hexa Studios bots! 💜")
        embed.timestamp = discord.utils.utcnow()
        
        await interaction.response.send_message(embed=embed, ephemeral=True)