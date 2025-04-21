from pathlib import Path

PARENT_PATH = Path(__file__).parent.parent

# Bot settings
TOKEN = ''
PREFIX = '!'

YT_DLP_OPTIONS = {
    'format': 'bestaudio[abr<=64]/bestaudio',
    "noplaylist": True,
    "youtube_include_dash_manifest": False,
    "youtube_include_hls_manifest": False,
    "cookiefile": f"{PARENT_PATH}/config/cookies.txt",
    # "cookiesfrombrowser": ("default", )
}
FFMPEG_EXECUTABLE = f"{PARENT_PATH}/ffmpeg/bin/ffmpeg.exe"
FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}

SKIP_VOTING_PERCENTAGE = 0.5

ERROR_NOT_IN_VOICE_CHANNEL = "You must be in a voice channel."
ERROR_WRONG_VOICE_CHANNEL = "You must be in the same voice channel as the bot."
ERROR_DISCONNECTED = "The bot is not connected to any voice channel."
ERROR_NOT_PLAYING = "The bot is not playing any song."
ERROR_SONG_NOT_FOUND = "Song not found."
ERROR_USER_SKIP_BLOCKED = "You cannot use this command, use `/skip-vote` instead."
ERROR_QUEUE_EMPTY = "The queue is empty."

COMMAND_PLAY_DESCRIPTION = "Play a song from YouTube."
COMMAND_SKIP_DESCRIPTION = "Skip the current song."
COMMAND_SKIP_VOTE_DESCRIPTION = "Vote to skip the current song."
COMMAND_STOP_DESCRIPTION = "Stop all songs."
COMMAND_DISCONNECT_DESCRIPTION = "Disconnect the bot from voice channels."
COMMAND_QUEUE_DESCRIPTION = "Show the current queue."
COMMAND_PAUSE_DESCRIPTION = "Toggle pause for the current song."
COMMAND_REPEAT_DESCRIPTION = "Toggle repeat for the current song."

PLAY_MESSAGE = "Added {0} to the queue."
SKIP_VOTE_MESSAGE = "Voted to skip {0}\n{1}/{2} votes."
SKIP_ALREADY_VOTED_MESSAGE = "You have already voted to skip {0}\n{1}/{2} votes."
SKIP_MESSAGE = "Skipped {0}."
STOP_MESSAGE = "Stopped all songs."
DISCONNECT_MESSAGE = "Disconnected from the voice channel."
QUEUE_MESSAGE = "### Queue:{0}"
PAUSE_MESSAGE = "Pause {0}."
REPEAT_MESSAGE = "Repeat {0} for the current song."

ON = "ON"
OFF = "OFF"

# Tray settings
TRAY_ICON = f"{PARENT_PATH}/config/icon.png"
TRAY_TITLE = "JokergeFM"
TRAY_EXIT = "Exit"