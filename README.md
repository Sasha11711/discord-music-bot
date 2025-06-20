# Discord Music Bot (aka JokergeFM)

A python discord music bot that uses yt-dlp and FFmpeg to play music with such slash-commands: `/play`, `/skip_vote`, `/skip`, `/stop`, `/disconnect`, `/pause`, `/repeat` and `/queue`.

## How to use

1. Install [Python](https://www.python.org/downloads/) and [FFmpeg](https://www.ffmpeg.org/download.html) on your machine.

2. **(Optional)** Create and activate a python virtual environment in project:  
   `python -m venv venv`  
   `call venv\Scripts\activate.bat`

3. Install requirements:  
`pip install -r requirements.txt`

4. Paste your discord bot token into TOKEN and ffmpeg executable path into FFMPEG_EXECUTABLE in [config/settings.py](config\settings.py).

5. Get YouTube account's cookies from youtube.com (required by yt-dlp) by either:
   - Get YouTube cookies from selected browsers automatically by uncommenting the line 10 in [config/settings.py](config/settings.py):  
   `# "cookiesfrombrowser": ("default", )`
   OR
   - Get cookies.txt file with a browser extension (for example: [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)) and put it inside [config/](config). **As with any browser extension, be careful about what you install.**
   OR
   - Get cookies.txt file with [yt-dlp](https://github.com/yt-dlp/yt-dlp) (needs to be installed on your machine) and put it inside [config/](config):  
   `yt-dlp --cookies-from-browser your_browser --cookies cookies.txt`

6. Run [bot.py](bot.py):  
   `python bot.py`

## Future Improvements

- ~~Making `/skip` `/stop` and `/disconnect` available if a user is alone with the bot.~~ Done

Feel free to contribute or suggest improvements!

## Disclaimer

This bot is intended for personal use only. Ensure you comply with YouTube's Terms of Service and copyright laws when using this bot.

## License

This project is open-source and available under the [MIT License](LICENSE).