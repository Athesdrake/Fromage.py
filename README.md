# Fromage.py
**Fromage.py is the implementation of the [Fromage API](https://github.com/Lautenschlager-id/Fromage) created by Lautenschlager**

Fromage.py is an API for the Atelier801's forums.

**PRE-ALPHA**

## Installation
Install Fromage.py using `pip`:
`pip install pip install -U git+https://github.com/Athesdrake/Fromage.py`

## Requirements
- Python 3.5.3 or higher. **Earlier versions of Python are not supported**
- Fromage.py uses the [`aiohttp`](https://github.com/KeepSafe/aiohttp) module. It's a library for asynchronous HTTP requests.

## Discord
The fromage.py API is compatible **only** with the **rewrite** version of `discord.py`.
`discord.py` is not required but if you want to install it, use: `pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]`.

## Example
**TODO**: make it better.
**Uncertain result**: I want to make it that way but it's W.I.P.
```Python
import fromage
import asyncio
import aiohttp

bot = fromage.Client()

@bot.event
async def on_new_pm(msg):
	print('You got a new private message from {.author} !'.format(msg))

bot.run('Username#0000', 'p455w0rd')
```
/!\ Use `aiohttp` instead of `requests`/`urllib`
