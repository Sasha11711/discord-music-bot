import discord
import yt_dlp
from discord.ext import commands
from config.settings import *
from classes.VoiceInfo import VoiceInfo

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

voices_info: dict[str, VoiceInfo] = {}

async def can_use(interaction: discord.Interaction) -> bool:
    voice_client = interaction.guild.voice_client
    
    if voice_client is None:
        await interaction.response.send_message(ERROR_DISCONNECTED)
        return False
    
    voice = interaction.user.voice
    if voice is None:
        await interaction.response.send_message(ERROR_NOT_IN_VOICE_CHANNEL)
        return False
    
    if voice_client.channel.id != voice.channel.id:
        await interaction.response.send_message(ERROR_WRONG_VOICE_CHANNEL)
        return False
    return True

async def is_playing(interaction: discord.Interaction) -> bool:
    if not await can_use(interaction):
        return False

    if not interaction.guild.voice_client.is_playing():
        await interaction.response.send_message(ERROR_NOT_PLAYING)
        return False
    return True

def format_time(seconds: int) -> str:
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02d}"

def format_song(song, with_url: bool = True, elapsed: int = None) -> str:
    message = f"[{song['title']}]({song['url']})" if with_url else song['title']
    message += " - "
    if elapsed: message += format_time(elapsed) + "/"
    message += format_time(song["duration"])
    return message

def get_required_votes(voice_channel: discord.VoiceChannel) -> int:
    return int((len(voice_channel.members) - 1) * SKIP_VOTING_PERCENTAGE) + 1

def is_url(url: str) -> bool:
    return url.startswith(("https://youtu.be/", "https://www.youtube.com/watch?v="))


@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands")

@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if member == bot.user:
        if before.channel and after.channel is None:
            del voices_info[str(before.channel.guild.id)]
    else:
        voice_client = member.guild.voice_client
        if  voice_client:
            voice_client_channel = voice_client.channel
            
            if len(voice_client_channel.members) == 1:
                await voice_client.disconnect()
                return
            
            if before.channel and before.channel.id == voice_client_channel.id and (after.channel is None or after.channel.id != voice_client_channel.id):
                current_votes = len(voices_info[str(member.guild.id)].skip_votes)
                required_votes = get_required_votes(voice_client_channel)
                if current_votes >= required_votes:
                    await voice_client.stop()


@bot.tree.command(name="play", description=COMMAND_PLAY_DESCRIPTION)
async def play(interaction: discord.Interaction, song: str):
    await interaction.response.defer()

    voice = interaction.user.voice

    if voice is None:
        await interaction.followup.send(ERROR_NOT_IN_VOICE_CHANNEL)
        return
    
    voice_client = interaction.guild.voice_client
    guild_id = str(interaction.guild_id)
    
    if voice_client and voice_client.channel.id != voice.channel.id:
        await interaction.followup.send(ERROR_WRONG_VOICE_CHANNEL)
        return
    
    song_result = None
    if is_url(song):
        result = await bot.loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(YT_DLP_OPTIONS).extract_info(song, download=False))
        if result is None:
            await interaction.followup.send(ERROR_SONG_NOT_FOUND)
            return
        song_result = result
    else:
        result = await bot.loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(YT_DLP_OPTIONS).extract_info("ytsearch1:" + song, download=False))
        songs = result.get("entries", None)
        if songs is None:
            await interaction.followup.send(ERROR_SONG_NOT_FOUND)
            return
        song_result = songs[0]

    song_info = {
        "title": song_result["title"], 
        "duration": song_result["duration"], 
        "url": song_result["url"]}

    if not voice_client:
        voice_client = await voice.channel.connect(cls=discord.VoiceClient)
        voices_info[guild_id] = VoiceInfo()
    voices_info[guild_id].queue.append(song_info)

    if not voice_client.is_playing():
        await play_next(voice_client, guild_id)
    
    await interaction.followup.send(PLAY_MESSAGE.format(format_song(song_info)))

async def play_next(voice_client: discord.VoiceClient, guild_id: str, repeated_song_info=None):
    if guild_id not in voices_info:
        return

    voice_info = voices_info[guild_id]

    song_info = repeated_song_info
    if repeated_song_info:
        song_info = repeated_song_info
    else:
        voice_info.skip_votes = []

        if not voice_info.queue:
            return
        
        song_info = voice_info.queue[0]
    
    source = discord.FFmpegPCMAudio(song_info["url"], **FFMPEG_OPTIONS, executable=FFMPEG_EXECUTABLE)
    
    
    def after_playing(error):
        if error:
            print(f"Error playing audio: {error}")
        if voice_info.is_repeating:
            bot.loop.create_task(play_next(voice_client, guild_id, song_info))
        else:
            del voice_info.queue[0]
            bot.loop.create_task(play_next(voice_client, guild_id))

    voice_client.play(source, after=after_playing)
    voice_info.song_start_time = int(voice_client.timestamp)

@bot.tree.command(name="skip-vote", description=COMMAND_SKIP_VOTE_DESCRIPTION)
async def skip_vote(interaction: discord.Interaction):
    if not await is_playing(interaction):
        return
    
    voice_info = voices_info[str(interaction.guild_id)]
    user = interaction.user

    if user.id in voice_info.skip_votes:
        await interaction.response.send_message(SKIP_ALREADY_VOTED_MESSAGE.format(formatted_song, current_votes, required_votes))
        return
    
    formatted_song = format_song(voice_info.queue[0])
    current_votes = len(voice_info.skip_votes)
    required_votes = get_required_votes(interaction.user.voice.channel)

    voice_info.skip_votes.append(user.id)
    current_votes += 1
    
    if current_votes >= required_votes:
        voice_info.is_repeating = False
        interaction.guild.voice_client.stop()

    await interaction.response.send_message(SKIP_VOTE_MESSAGE.format(formatted_song, current_votes, required_votes))

@bot.tree.command(name="skip", description=COMMAND_SKIP_DESCRIPTION)
async def skip(interaction: discord.Interaction):
    if not await is_playing(interaction):
        return
    
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(ERROR_USER_SKIP_BLOCKED)
        return
    
    voice_info = voices_info[str(interaction.guild_id)]

    voice_info.is_repeating = False
    interaction.guild.voice_client.stop()
    await interaction.response.send_message(SKIP_MESSAGE.format(format_song(voice_info.queue[0])))

@bot.tree.command(name="stop", description=COMMAND_STOP_DESCRIPTION)
async def stop(interaction: discord.Interaction):
    if not await is_playing(interaction):
        return
    
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(ERROR_USER_SKIP_BLOCKED)
        return

    voice_info = voices_info[str(interaction.guild_id)]

    voice_info.queue = []
    voice_info.is_repeating = False

    interaction.guild.voice_client.stop()

    await interaction.response.send_message(STOP_MESSAGE)

@bot.tree.command(name="disconnect", description=COMMAND_DISCONNECT_DESCRIPTION)
async def disconnect(interaction: discord.Interaction):
    if not await can_use(interaction):
        return
    
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(ERROR_USER_SKIP_BLOCKED)
        return
    
    await interaction.response.send_message(DISCONNECT_MESSAGE)
    await interaction.guild.voice_client.disconnect()

@bot.tree.command(name="pause", description=COMMAND_PAUSE_DESCRIPTION)
async def pause(interaction: discord.Interaction):
    if not await is_playing(interaction):
        return
    
    voice_client = interaction.guild.voice_client

    if voice_client.is_paused():
        voice_client.resume()
        await interaction.response.send_message(PAUSE_MESSAGE.format(OFF))
    else:
        voice_client.pause()
        await interaction.response.send_message(PAUSE_MESSAGE.format(ON))

@bot.tree.command(name="repeat", description=COMMAND_REPEAT_DESCRIPTION)
async def repeat(interaction: discord.Interaction):
    if not await is_playing(interaction):
        return
    
    voice_info = voices_info[str(interaction.guild_id)]
    
    voice_info.is_repeating = not voice_info.is_repeating
    await interaction.response.send_message(REPEAT_MESSAGE.format(ON if voice_info.is_repeating else OFF))

@bot.tree.command(name="queue", description=COMMAND_QUEUE_DESCRIPTION)
async def queue(interaction: discord.Interaction):
    guild_id = str(interaction.guild_id)

    if guild_id not in voices_info or not voices_info[guild_id].queue:
        await interaction.response.send_message(ERROR_QUEUE_EMPTY)
        return
    
    current_queue = list(voices_info[guild_id].queue)
    timestamp = interaction.guild.voice_client.timestamp - voices_info[guild_id].song_start_time
    message = "\n - " + format_song(current_queue.pop(0), elapsed=int(timestamp / 48000))
    for id, song in enumerate(current_queue):
        message += f"\n{id}. {format_song(song, False)}"

    await interaction.response.send_message(QUEUE_MESSAGE.format(message))

bot.run(TOKEN)