# By 💜 Hexa Studios 🌐 discord.gg/ezGvtVJvWk
import discord
from discord.ext import commands
import json
import os
from utils.log_manager import LogManager
from commands.set_logs import SetLogsCommand
from commands.hexastudios import HexaStudiosCommand

CONFIG_FILE = "config.json"

def first_time_setup():
    print("=" * 50)
    print("🤖 Hexa Studios - Discord Log Bot")
    print("=" * 50)
    print("\nFirst time setup!")
    print("\n📌 Follow these steps:")
    print("   1. Go to https://discord.com/developers/applications")
    print("   2. Create a new application")
    print("   3. Go to Bot section -> Add Bot")
    print("   4. Copy the token")
    print("   5. Enable MESSAGE CONTENT INTENT and SERVER MEMBERS INTENT")
    
    token = input("\n📝 Paste your bot token: ").strip()
    
    if not token:
        print("❌ Token cannot be empty!")
        return first_time_setup()
    
    config = {"token": token}
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
    
    print("\n✅ Config saved! Starting bot...\n")
    return config

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return first_time_setup()
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

config = load_config()
token = config.get("token")

if not token:
    print("❌ No token found. Restart the bot.")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
intents.voice_states = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
log_manager = LogManager()

def get_log_channels(guild_id, log_type):
    """Returns list of channel IDs that have this log type enabled"""
    channels = []
    for key, settings in log_manager.settings.items():
        if settings["guild_id"] == guild_id and log_type in settings["log_types"]:
            channels.append(settings["channel_id"])
    return channels

@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online!")
    print(f"💜 Log bot by Hexa Studios")
    await bot.change_presence(activity=discord.Game(name="By 💜 Hexa Studios"))
    
    await bot.add_cog(SetLogsCommand(bot, log_manager))
    await bot.add_cog(HexaStudiosCommand(bot))
    
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
        for cmd in synced:
            print(f"   - /{cmd.name}")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

# ==================== VOICE LOGS ====================

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel == after.channel:
        return
    
    # User joined a voice channel
    if after.channel and not before.channel:
        embed = discord.Embed(
            title="🎙️ Voice Join",
            description=f"{member.mention} (`{member}`) joined **{after.channel.name}**",
            color=0x00FF00
        )
        embed.add_field(name="Channel", value=after.channel.mention, inline=False)
        embed.set_footer(text="By 💜 Hexa Studios 🌐 discord.gg/ezGvtVJvWk")
        embed.timestamp = discord.utils.utcnow()
        
        for channel_id in get_log_channels(member.guild.id, "voice_join"):
            channel = bot.get_channel(channel_id)
            if channel:
                await channel.send(embed=embed)
    
    # User left a voice channel
    elif before.channel and not after.channel:
        embed = discord.Embed(
            title="🔇 Voice Leave",
            description=f"{member.mention} (`{member}`) left **{before.channel.name}**",
            color=0xFF0000
        )
        embed.add_field(name="Channel", value=before.channel.mention, inline=False)
        embed.set_footer(text="By 💜 Hexa Studios 🌐 discord.gg/ezGvtVJvWk")
        embed.timestamp = discord.utils.utcnow()
        
        for channel_id in get_log_channels(member.guild.id, "voice_leave"):
            channel = bot.get_channel(channel_id)
            if channel:
                await channel.send(embed=embed)

# ==================== CHANNEL LOGS ====================

@bot.event
async def on_guild_channel_create(channel):
    if isinstance(channel, discord.TextChannel):
        channel_type = "Text Channel"
    elif isinstance(channel, discord.VoiceChannel):
        channel_type = "Voice Channel"
    else:
        channel_type = "Category"
    
    embed = discord.Embed(
        title="📁 Channel Created",
        description=f"**Name:** {channel.mention}\n**Type:** {channel_type}\n**ID:** `{channel.id}`",
        color=0x00FF00
    )
    embed.set_footer(text="By 💜 Hexa Studios 🌐 discord.gg/ezGvtVJvWk")
    embed.timestamp = discord.utils.utcnow()
    
    for channel_id in get_log_channels(channel.guild.id, "channel_create"):
        log_channel = bot.get_channel(channel_id)
        if log_channel:
            await log_channel.send(embed=embed)

# ==================== MESSAGE LOGS ====================

@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    
    embed = discord.Embed(
        title="✏️ Message Edited",
        description=f"**Author:** {before.author.mention}\n**Channel:** {before.channel.mention}\n[Jump to message]({after.jump_url})",
        color=0xFFA500
    )
    embed.add_field(name="Before", value=before.content[:1000] or "*empty*", inline=False)
    embed.add_field(name="After", value=after.content[:1000] or "*empty*", inline=False)
    embed.set_footer(text="By 💜 Hexa Studios 🌐 discord.gg/ezGvtVJvWk")
    embed.timestamp = discord.utils.utcnow()
    
    for channel_id in get_log_channels(before.guild.id, "message_edit"):
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(embed=embed)

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    
    embed = discord.Embed(
        title="🗑️ Message Deleted",
        description=f"**Author:** {message.author.mention}\n**Channel:** {message.channel.mention}",
        color=0xFF0000
    )
    embed.add_field(name="Content", value=message.content[:1000] or "*no content*", inline=False)
    embed.set_footer(text="By 💜 Hexa Studios 🌐 discord.gg/ezGvtVJvWk")
    embed.timestamp = discord.utils.utcnow()
    
    for channel_id in get_log_channels(message.guild.id, "message_delete"):
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(embed=embed)

# ==================== ROLE LOGS ====================

@bot.event
async def on_guild_role_create(role):
    embed = discord.Embed(
        title="🏷️ Role Created",
        description=f"**Name:** {role.mention}\n**ID:** `{role.id}`\n**Color:** {str(role.color)}",
        color=0x00AAFF
    )
    embed.set_footer(text="By 💜 Hexa Studios 🌐 discord.gg/ezGvtVJvWk")
    embed.timestamp = discord.utils.utcnow()
    
    for channel_id in get_log_channels(role.guild.id, "role_create"):
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(embed=embed)

@bot.event
async def on_member_update(before, after):
    added_roles = [role for role in after.roles if role not in before.roles]
    for role in added_roles:
        embed = discord.Embed(
            title="🎭 Role Assigned",
            description=f"{after.mention} got role **{role.name}**",
            color=0xAA00FF
        )
        embed.set_footer(text="By 💜 Hexa Studios 🌐 discord.gg/ezGvtVJvWk")
        embed.timestamp = discord.utils.utcnow()
        
        for channel_id in get_log_channels(after.guild.id, "role_assign"):
            channel = bot.get_channel(channel_id)
            if channel:
                await channel.send(embed=embed)

if __name__ == "__main__":
    bot.run(token)