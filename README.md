# Discord Music Bot (aka JokergeFM)

A python discord music bot that uses yt-dlp and FFmpeg to play music with such slash-commands: `/play`, `/skip_vote`, `/skip`, `/stop`, `/disconnect`, `/pause`, `/repeat` and `/queue`.  
This version uses system tray and has FFmpeg preinstalled.

## Setup

1. Have [Python](https://www.python.org/downloads/) installed on your machine.

2. Download and unpack the code.

3. Paste your discord bot token into TOKEN in [config/settings.py](config\settings.py).

4. Get YouTube account's cookies from youtube.com (required by yt-dlp) by either:
   - Get YouTube cookies from selected browsers automatically by uncommenting the line 15 in [config/settings.py](config/settings.py):  
   `# "cookiesfrombrowser": ("default", )`
   OR
   - Get cookies.txt file with a browser extension (for example: [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)) and put it inside [config/](config). **As with any browser extension, be careful about what you install.**
   OR
   - Get cookies.txt file with [yt-dlp](https://github.com/yt-dlp/yt-dlp) (needs to be installed on your machine) and put it inside [config/](config):  
   `yt-dlp --cookies-from-browser your_browser --cookies cookies.txt`

## How to use

- Run [run_tray.bat](run_tray.bat), a system tray will appear.
- To close the bot, right-click the system tray and press **Exit**.

## Future Improvements

- Making `/skip` `/stop` and `/disconnect` available if a user is alone with the bot.

Feel free to contribute or suggest improvements!

## Disclaimer

This bot is intended for personal use only. Ensure you comply with YouTube's Terms of Service and copyright laws when using this bot.

This project includes FFmpeg, for more information see [ffmpeg/README.txt](ffmpeg/README.txt).

## License

This project is open-source and available under the [MIT License](LICENSE).

This project includes FFmpeg, which is licensed under the LGPL or GPL. For more details, see [ffmpeg/LICENSE](ffmpeg/LICENSE) or the FFmpeg [license page](https://ffmpeg.org/legal.html).
