from __future__ import print_function
# import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update 
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext,run_async
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import sys,os
import pickle
from googleapiclient.http import MediaFileUpload
# from pytube import YouTube
from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
# from queue import Queue
# from datetime import datetime
# import Download
import threading
import time
import asyncio
import User
from Upload import Upload
import shutil
from pyrogram import Client
import math
from urllib.parse import urlparse
loop = asyncio.get_event_loop()

class Bot:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    def __init__(self,TOKEN :str):
        self.TOKEN=TOKEN
        self.realpath1 = os.path.split(os.path.abspath(__file__))[0]
        self.SCOPE = ['https://www.googleapis.com/auth/drive'] 
        self.list = []
        self.download_status = None
        self.users = []
        self.chat_id = -1001172803610
        self.threads = None
        # self.event_loop = loop
        #self.ss = []
        self.text = ''

    def __download_with_prograss(self,file_size: int):
        if file_size == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(file_size, 1024)))
        p = math.pow(1024, i)
        s = round(file_size / p, 2)
        return "%s %s" % (s, size_name[i])


    def help_command(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /help is issued."""

        update.message.reply_text('Help!')
        # update.message.reply_text(update)
        # print(update)
        # print(update.message.reply_to_message)
        print(update.message.text.removeprefix('/help '))

        print(update.message.message_id)

    
    def __info(self,id_):
        # ad = os.path.split(os.path.abspath(__file__))[0]
            if os.path.exists(f'{self.realpath1}//{id_}//auth//token.pickle'):
                with open(f'{self.realpath1}//{id_}//auth//token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            service = build('drive', 'v3', credentials=creds,cache_discovery=False)
            li = service.about().get(fields = 'storageQuota').execute()
            # service = self.authorization().about().get(fields = 'storageQuota').execute()
            return int(li['storageQuota']['limit']) , int(li['storageQuota']['usage'])


    def storage(self, update: Update, context: CallbackContext) -> None:
        Id = update.message.from_user.id
        if Upload.check(Id):
            # user = User.User(Id)
            limit , storage = self.__info(Id)
            free = limit - storage
            text = f'limit : {self.__download_with_prograss(limit)}\nstorage : {self.__download_with_prograss(storage)}\nfree : {self.__download_with_prograss(free)}'
            update.message.reply_text(text)
        else:
            update.message.reply_text('First Auth !')
        # pass
    def revoke(self, update: Update, context: CallbackContext) -> None:
        # print(update.message.from_user.id)
        Id = update.message.from_user.id
        if Upload.check(Id):
            try:
                Upload.revoke(Id)
                update.message.reply_text('revoked !')
            except:
                update.message.reply_text('not revoked !')
        else:
            update.message.reply_text('First Auth !')
        # pass
    def ls(self, update: Update, context: CallbackContext) -> None:
        id_ = update.message.from_user.id
        ad = f'{self.realpath1}//{str(id_)}//Download'
        text =''
        try:
            onlyfiles = [f for f in os.listdir(ad) if os.path.isfile(os.path.join(ad, f))]
            for i in onlyfiles:
                text += i
                text +='\n'
        
            update.message.reply_text(text)
        except:
            update.message.reply_text('no files in here')

        
    def start(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Start!')
        print(update.message.chat_id)
        print('\n',update.message.from_user.username)
        print(self.users)
        # while True :
        #     print(1)
        # update.message.reply_text
    def send_auth(self, update: Update, context: CallbackContext) -> None:
        # print(update.message)
        has : bool = True
        auth = 'auth'
        user_id = update.message.from_user.id
        for users in self.list:
            if users[0] == user_id:
                has = False
                break
        if os.path.exists(f'{self.realpath1}/{str(user_id)}/{auth}//token.pickle'):
            has = False
            update.message.reply_text('Already Auth...!')

        if has :
            creds = None
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        f'{self.realpath1}//Elyas.json', self.SCOPE)
                    # print(flow.authorization_url()[0])
                    print('############################################')
                    print(flow.return_url())
                    print('############################################')
                    
            keyboard = [
                
                [InlineKeyboardButton("authorization", callback_data=update.message.from_user.id,url=flow.return_url())]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            update.message.reply_text('Send Me Code!:', reply_markup=reply_markup)

            self.list.append((update.message.from_user.id,flow))
            print(self.list)
        print(self.list)
    # def usersw(self):
    #         for u,i in enumerate(self.users):
    #             for k,j in enumerate(i.downloads) :
    #                 print(f'{j.user} -------- {j.status}')
    #                 self.text += f'new is downloding -> {j.user} ---> {j.status} \n ----------\n'
    #                 if j.complete :
    #                     i.uploads.append(j.address)
    #                     self.ss.append(j.address)
    #                     del i.downloads[k]



    def auto_message(self, update: Update, context: CallbackContext):
        while len(self.users) > 0:
            text = ''
            time.sleep(4)
            for i in self.users:

                

                try:
                    text += i.showe_downloads
                except:
                    print('not download')
                # text += f'CC: @{i.user_name}\n' 
                # print(text)
                # for k,j in enumerate(i.downloads) :
                #     print(f'{j.user} -------- {j.status}')
                #     text += f'downloding -> {j.user} ---> {j.status} \n ----------\n'
                #     if j.complete :
                #         i.paths.append((j.address,j.mimtype))
                #         del i.downloads[k]
                i.downloader()

                i.uploader()
                
                # if len(i.paths) > 0 and i.uploads is None:
                #     i.uploader()



                
                # if len(i.downloads) <= 2 and len(i.queue_links) > 0 :
                #     i.download(i.queue_links.pop(0))
                #     #

                if i.user_deleter():
                    self.users.remove(i)
                # if len(i.downloads)==0 and len(i.queue_links)==0 and len(i.paths)==0 and i.uploads is None:
                #     try:
                #         self.deleter(self.users[u])
                #     except Exception as e:
                #         print(e)
                #     finally:
                #         del self.users[u]
                # print(i.queue_links)
                i.deleter()
                # print(len(i.downloads))
                try:
                    text+=i.show_uploads
                except:
                    print('not upload')
                # text += f'CC: @{i.user_name}\n' 
                # print(text)
                # if not i.uploads is None:
                #     text += f'uploading {i.uploads.status}\n'
                #     print(i.uploads.status)

                    # if i.uploads.complete:
                    #     i.uploads = None
                        
                text += i.show_in_queue_downloads
                # text += f'CC: @{i.user_name}\n' 
                # print(text)
                # for h in i.queue_links:
                #     text += f'in queue for download -> {h}\n'
                text += i.show_in_queue_uploads
                # text += f'CC: @{i.user_name}\n' 
                # print(text)
                # for h in i.paths:
                #     text += f'in queue for upload -> {h}\n'
            try:
                context.bot.edit_message_text(text=text,chat_id=self.chat_id,message_id=self.download_status)
            except:
                print('not edited!')
            # time.sleep(4)
        self.threads = None
        time.sleep(2)
        context.bot.edit_message_text(text='end',chat_id=self.chat_id,message_id=self.download_status)
            # # print(self.users[0].status)
            # for i in self.users:
            #     text += f'{i.user} is downloading {i.status}\n ##################################### \n'
            # context.bot.edit_message_text(text=text,chat_id=self.chat_id,message_id=self.download_status)
            # # print(text)
    def __file_validetor(self,update: Update):
        doc = update.message.reply_to_message.document
        if doc is None:
            return False
        return True


    def __uri_validator(self,x):
        try:
            result = urlparse(x)
            return all([result.scheme, result.netloc])
        except:
            return False

    def __extracer(self,text, prefix):

        if text.startswith(prefix):
            return text[len(prefix):]

    def cancel(self, update: Update, context: CallbackContext) -> None:
        id_ =  update.message.from_user.id
        download_id = self.__extracer(update.message.text,'/cancel ')
        user = None
        for i in self.users:
            if i.id == id_:
                user = i
                print(user.id)
        if user is not None:
            print(user.downloads)
            user.cancel_download(int(download_id))
            update.message.reply_text('canceled')
        else:
            update.message.reply_text('not canceled')

    def dele(self, update: Update, context: CallbackContext) -> None:
        id_ =  update.message.from_user.id
        ad = f'{self.realpath1}//{str(id_)}//Download'
        try:
            shutil.rmtree(ad)
            update.message.reply_text('removed...')
        except:
            update.message.reply_text('not removed...')
        # user = None
        
        # for i in self.users:
        #     if i.id == id_:
        #         user = i

        # if user is None:
        #     update.message.reply_text('not in download...')
        # else:
        #     self.users.remove(user)
        # update.message.reply_text('removed...')

    def down(self, update: Update, context: CallbackContext) -> None:
        id_ =  update.message.from_user.id
        link_text = update.message.reply_to_message.text


        # duc_id = update.message.reply_to_message.document
        if update.message.reply_to_message is None:
            return
                                                                                                                #todo
        if Upload.check(id_):
            if self.__uri_validator(update.message.reply_to_message.text) or self.__file_validetor(update) or ('magnet' in link_text)  :
                print('yes...')
            
                link = update.message.reply_to_message.text
                ducumet_tg = update.message.reply_to_message
                print(link)

                # if ducumet_tg is None:
                links = (link,ducumet_tg)
                print('############################')
                print(links[1])
                print('############################')
                user = None

                try:
                    context.bot.delete_message(chat_id=self.chat_id,message_id=self.download_status)
                except:
                        
                    print('error!...')
                self.download_status = update.message.reply_text('Downloading... !').message_id

                for i in self.users:
                    if i.id == id_:
                        user = i
                
                
                if user is None :
                    global loop
                    user = User.User(loop,id_,update.message.from_user.username)
                    print('new user link append')
                    self.users.append(user)
                    user.download(links,update.message.message_id)
                            
                else:
                    print('old user link added download')
                    user.download(links,update.message.message_id)
                # else:
                #     if user is None :
                #         user = User.User(id_,update.message.from_user.username)
                #         print('new user tg append')
                #         self.users.append(user)
                #         user.tgdownloader()
                #     else:
                #         print('old user tg added download')
                #         user.download(link)

                if self.threads is None:
                    try:
                        self.threads = threading.Thread(target=self.auto_message,args=(update,context,))
                        self.threads.start()
                    except:
                        print('error...')
        else:
            update.message.reply_text('First Auth!')
    
    def auth_get(self, update: Update, context: CallbackContext) -> None:
        id_ =  update.message.from_user.id
        auth = 'auth'
        flow = None
        print(self.list)
        for cont,us in enumerate(self.list):
            if us[0] == id_:
                flow = us[1]
                break
        if not flow is None:    
            query = update.message.text
            try:
                creds = flow.set_code(query)
                print(query)
                path1=os.path.join(os.path.dirname(sys.argv[0]),f'{id_}','auth')    
                if not os.path.exists(path1):
                    os.makedirs(path1)
  
                with open(f'{self.realpath1}/{str(id_)}/{auth}//token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
                del self.list[cont]
                print(self.list)
            except :
                update.message.reply_text('not Correct !')

    def starter(self):
        updater = Updater(self.TOKEN)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("help", self.help_command))
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("auth", self.send_auth))
        dispatcher.add_handler(CommandHandler("down", self.down))
        dispatcher.add_handler(CommandHandler("del", self.dele))
        dispatcher.add_handler(CommandHandler("ls", self.ls))
        dispatcher.add_handler(CommandHandler("cancel", self.cancel))
        # revoke
        # storage
        dispatcher.add_handler(CommandHandler("storage", self.storage))
        dispatcher.add_handler(CommandHandler("revoke", self.revoke))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.auth_get))
        updater.start_polling()
        # updater.idle()
class user_bot:
    def __init__(self,loop) -> None:
        # pass
        self.api_id = 5975714
        self.api_hash = '8d1ea6da21f3ddb0426938c3975fb0e7'
        self.session_name = 'BACK2gCuzoLPCD1cEBt8xlxdQ0RXnHHiQkzDFlCi_hGRTYJvGchW3jyVdqFQvpSsF4pCXa2UCEkXosrWmlbJ_uA2V-3bU5mM0ep5455ui_LDTxUQvCPdsscNrHNXWmV9XFrux4OSZtu-rcnsDcnZO3ZVmnTzyDd9cqGv00AqQ5xUUX1Q1J8BjDs825JMmohFjlOAJ6qA1Q0o-TtW2KLcQN8EC5w8naV1EA7ZvnG1WTcJdO-t8ILKrtQHMFdxNBlgQ76rQjv82O7kI99AMBWEUo3r_QkVIPr3sUyqKEsrgusm7Ef6g2OoDG6AaeiybU7pS0-sI3Tlv6fRbQ1lXYX8CH5EZ0EVuAA'
        self.workers = 2
        # self.workdir = 'session/'
        self.chat_id=-1001172803610

        self.Client: Client
        self.event_loop = loop
    async def create_session(self):
        self.Client = Client(
            self.session_name,
            api_id=self.api_id,
            api_hash=self.api_hash,
            workers=self.workers,
            workdir='sessions/'
        )
        instence = self
        # @self.Client.on_message()
        # def messag_handler(self,message):
        #     print(message)
        #     # loop = asyncio.get_event_loop()
        #     instence.event_loop.create_task(instence.down(message.message_id))
            # loop

        @self.Client.on_disconnect()
        async def disconnect_handler(self,message = None):
            while not self.is_connected:
                time.sleep(10)
                if self.is_connected:
                    break
                try:
                   await self.connect()
                except:
                    pass

        # @self.Client.on_deleted_messages()
        # def deleted_message_handler(self,message=None):
        #     pass

        # @self.Client.on_user_status()
        # def user_statuse_handler(self,statuse = None):
        #     pass

    async def start_session(self):
        if self.Client:
            await self.Client.start()
    
    # async def down(self,id):
    #     print('elllll')
    #     # self.arr.append(self.down)
    #     mess = await self.Client.get_messages(-1001172803610,id)
    #     # self.Client.get
    #     print(mess)
    #     await self.Client.download_media(message=mess,progress=self.__prograss)


# if __name__=='__main__':

tel = user_bot(loop)
asyncio.ensure_future(tel.create_session())
asyncio.ensure_future(tel.start_session())
