# By 💜 Hexa Studios 🌐 discord.gg/ezGvtVJvWk
import discord
from discord import app_commands
from discord.ext import commands

LOG_CHOICES = [
    app_commands.Choice(name="📝 Message Edits", value="message_edit"),
    app_commands.Choice(name="🗑️ Message Deletes", value="message_delete"),
    app_commands.Choice(name="📁 Channel Create", value="channel_create"),
    app_commands.Choice(name="🎙️ Voice Join", value="voice_join"),
    app_commands.Choice(name="🔇 Voice Leave", value="voice_leave"),
    app_commands.Choice(name="🏷️ Role Create", value="role_create"),
    app_commands.Choice(name="🎭 Role Assign", value="role_assign")
]

class SetLogsCommand(commands.Cog):
    def __init__(self, bot, log_manager):
        self.bot = bot
        self.log_manager = log_manager
    
    @app_commands.command(name="set_logs", description="Configure logs to be sent to a specific channel")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(
        channel="The channel where logs will be sent",
        log1="Log type 1/7",
        log2="Log type 2/7",
        log3="Log type 3/7",
        log4="Log type 4/7",
        log5="Log type 5/7",
        log6="Log type 6/7",
        log7="Log type 7/7"
    )
    @app_commands.choices(
        log1=LOG_CHOICES, log2=LOG_CHOICES, log3=LOG_CHOICES,
        log4=LOG_CHOICES, log5=LOG_CHOICES, log6=LOG_CHOICES, log7=LOG_CHOICES
    )
    async def set_logs(
        self, 
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        log1: str = None, 
        log2: str = None, 
        log3: str = None,
        log4: str = None, 
        log5: str = None, 
        log6: str = None,
        log7: str = None
    ):
        
        selected = [x for x in [log1, log2, log3, log4, log5, log6, log7] if x is not None]
        
        if not selected:
            embed = discord.Embed(
                title="⚠️ Error",
                description="Please select at least one log type!",
                color=0xFF0000
            )
            embed.set_footer(text="By 💜 Hexa Studios 🌐 discord.gg/ezGvtVJvWk")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Save settings for the selected channel
        self.log_manager.set_logs(interaction.guild_id, channel.id, selected)
        
        log_names = {
            "message_edit": "📝 Message Edits",
            "message_delete": "🗑️ Message Deletes", 
            "channel_create": "📁 Channel Create",
            "voice_join": "🎙️ Voice Join",
            "voice_leave": "🔇 Voice Leave",
            "role_create": "🏷️ Role Create",
            "role_assign": "🎭 Role Assign"
        }
        
        embed = discord.Embed(
            title="📋 Log Channel Configured",
            description=f"Logs will be sent to {channel.mention}",
            color=0x9B59B6  # Purple like Hexa Studios
        )
        embed.add_field(
            name="✅ Active Logs",
            value="\n".join([f"• {log_names.get(l, l)}" for l in selected]) or "None",
            inline=False
        )
        embed.set_footer(text="By 💜 Hexa Studios 🌐 discord.gg/ezGvtVJvWk")
        embed.timestamp = discord.utils.utcnow()
        
        await interaction.response.send_message(embed=embed)
        
        # Send a test message to the log channel
        test_embed = discord.Embed(
            title="✅ Log System Active",
            description=f"Logs configured by {interaction.user.mention}\n\n**Active logs:**\n" + "\n".join([f"• {log_names.get(l, l)}" for l in selected]),
            color=0x00FF00
        )
        test_embed.set_footer(text="By 💜 Hexa Studios 🌐 discord.gg/ezGvtVJvWk")
        test_embed.timestamp = discord.utils.utcnow()
        await channel.send(embed=test_embed)