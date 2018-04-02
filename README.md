# GeohashingBot

## What is this?

This is a [telegram bot](https://telegram.org/blog/bot-revolution), which allows you to inspect the current [geohash](http://wiki.xkcd.com/geohashing) in your coordinate sector. However, currently only [inline queries](https://core.telegram.org/bots/inline) are supported. Instead of messaging [the bot](https://t.me/GeohashingBot) (or adding it to a group), you should mention the bot in a conversation by typing `@GeohashingBot <latitude prefix> <longitude prefix>` into the chat window, with `<latitude prefix>` representing the pre-commas of your latitude and `<longitude prefix>` representing the pre-commas of your longitude. The bot will then guess your timezone and current date based on your location and calculate the geohash (taking into account the [30W Time Zone Rule](http://wiki.xkcd.com/geohashing/30W)).

## Installation

If you want to host the bot yourself, you need to install some dependencies first. Obviously, you need `python3` and `pip`, what you probably already have installed. Then install `pipenv` by typing

	pip install pipenv

`pipenv` will handle all dependencies and virtual python environments. Now type

	pipenv install

to finish the installation.

## Usage

	pipenv shell
	python bot.py

## Credits

The bot’s implementation of the geohashing algorithm is based on the [reference implementation](http://wiki.xkcd.com/geohashing/Implementations/Libraries/Python) from the [geohashing wiki](http://wiki.xkcd.com/geohashing).
