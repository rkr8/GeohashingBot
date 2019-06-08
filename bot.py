#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from secrets import token_urlsafe
from datetime import datetime
from uuid import uuid4
from telegram import InlineQueryResultLocation, InlineKeyboardMarkup, \
        InlineKeyboardButton
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from parse import compile
from pytz import timezone
from tzwhere.tzwhere import tzwhere
from geohash import calculate
import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

parser = compile('{:d} {:d}')

tzw = tzwhere()

webhook_token = token_urlsafe(config.webhook_token_length)

def inlinequery(bot, update):
    loc = parser.parse(update.inline_query.query).fixed
    if len(loc) != 2:
        return
    if abs(loc[0]) >= 90:
        return
    if abs(loc[1]) >= 180:
        return
    date = datetime.now(timezone(tzw.tzNameAt(loc[0], loc[1]))).date()
    hash = calculate(loc, date)
    results = [
            InlineQueryResultLocation(
                id=uuid4(),
                latitude=hash[0],
                longitude=hash[1],
                title=str(date),
                reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton('Open Street Map',
                            url=config.osm_url.format(hash[0], hash[1])),
                          InlineKeyboardButton('Google Maps',
                            url=config.maps_url.format(hash[0], hash[1])),
                          InlineKeyboardButton('Geohashing Wiki',
                            url=config.wiki_url.format(date, loc[0], loc[1]))]]
                    )
                )
            ]
    update.inline_query.answer(results)

def main():
    updater = Updater(config.token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(InlineQueryHandler(inlinequery, pattern='^-?[0-9]{1,2} -?[0-9]{1,3}$'))

    updater.start_webhook(listen=config.webhook_listen,
                          port=config.webhook_port,
                          url_path=webhook_token)
    updater.bot.set_webhook(config.webhook_url.format(webhook_token))
    updater.idle()

if __name__ == '__main__':
    main()
