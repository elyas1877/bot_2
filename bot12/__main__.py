# import asyncio
# import telephon_class
# # from telephon_class import phon
import bot
import threading
import os
# import asyncio
# from dotenv import load_dotenv

def main():
    # load_dotenv()
    bot1 = bot.Bot(os.getenv('bot_token'))
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