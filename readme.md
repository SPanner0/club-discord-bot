
# Discord.py Bot for small clubs and groups

Creative name, I know. This bot was made for the personal uses of the author running a small school club on a Discord server.

Feel free to clone this bot and add this to your own project. Do whatever you like with it. Have fun!

Note: This is meant to be an on-going project with no end goal. Cogs are meant to be changed to fit the needs of the current situation.


# How to use

## 1. Clone the bot to your local machine (preferably into an empty directory that you want to store your bot in)

That usually involves running a git command like so:
```
git clone https://github.com/Wolfus20/club-discord-bot.git
```

## 2. Activate a virtual environment (venv)

This step is optional, but it prevents your machine from getting cluttered by all sorts of junk Python modules

Make sure you're in your directory where you cloned the bot into

You can then create a venv by running:
```
python -m venv /path/to/venv
```

Now you can activate the venv by running:
```
./path/to/venv/Scripts/activate.bat
```


## 3. Installing the requirements

Install the requirements by running:
```
pip install -r path/to/requirements.txt
```


## 4. Create a bot account and add it to your server

This is way too many steps to explain and I'm frankly way too lazy.

Here's a guide by discord.py that walks you through the process: https://discordpy.readthedocs.io/en/stable/discord.html


## 5. Setting up config.json

The bot requires a ``config.json`` file to provide the necessary configurations for your bot to run.

Right now, the structure of the ``config.json`` file looks like this:
```json
{
        "prefix": "!",
        "token": "xxxxx"
}
```
Feel free to pick any prefix of your choice and remember to fill your bot token in the appropriate field.


## 6. Running the bot

Finally, you can run the bot by running the ``main.py`` file just like any other Python file

```
./main.py
```