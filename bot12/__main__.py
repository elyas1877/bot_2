# import asyncio
# import telephon_class
# # from telephon_class import phon
import bot
import threading
# import asyncio

def main():
    bot1 = bot.Bot('225268369:AAGdzjNI9jWrRCz0-7fxXA9nbqAZ4XPo_3k')
        # bot.starter()
    # bot.
    threading.Thread(target=bot1.starter).start()


    bot.loop.run_forever()
    print('1')

# loop = asyncio.get_event_loop()
# tel = telephon_class.phon(loop)
if __name__ == '__main__':
    main()

# futuress = [
#     asyncio.ensure_future(tel.create_session()),
#     asyncio.ensure_future(tel.start_session())

# ]
# #loop
# # loop.run_until_complete(asyncio.gather(*futuress))
# loop.run_forever()