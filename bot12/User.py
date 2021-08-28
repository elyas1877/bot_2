import os
from googleapiclient.discovery import build
# import threading
# import Download
from Download import Downloade
import Upload
import asyncio
import shutil
import re
# loope = asyncio.new_event_loop()
# looper :bool = True
# print('run')
# threading.Thread(target=loope.run_forever,args=())
# print('for ever')
class User:
    def __init__(self,loop,id:int,user_name = None):
        self.id = id
        self.paths = []
        self.uploads = None
        self.downloads = []
        self.queue_links = []
        self.user_name = user_name
        self.passe = False
        # self.tg_download = []
        self.tasks = []
        # self.loo
        self.loop = loop
    # def chek(self,size):
    #     if self.passe :
    #         return True
    #     on_prossess = 0
    #     on_prossess += int(size)
    #     limit , storage = self.info()
    #     on_prossess += storage
    #     for prossess in self.downloads:
    #         on_prossess += prossess.file_size
    #     try:
    #         on_prossess += self.uploads.size
    #     except:
    #         pass
    #     al = limit - on_prossess
    #     if al >= 0 :
    #         print('size : ',al)
    #         return True
    #     return False
    def __youtube_url_validation(self,url):
        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

        youtube_regex_match = re.match(youtube_regex, url)
        if youtube_regex_match:
            return youtube_regex_match

        return youtube_regex_match
    def __is_youtubelink(self,url):
        m = self.__youtube_url_validation(url)
        if m:
            return True
        return False

    def __is_magnet(self,url: str):
        MAGNET_REGEX = r"magnet:\?xt=urn:btih:[a-zA-Z0-9]*"
        magnet = re.findall(MAGNET_REGEX, url)
        if magnet:
            return True
        return False
    # def info(self):
    #     ad = os.path.split(os.path.abspath(__file__))[0]
    #     if os.path.exists(f'{ad}//{str(self.id)}//auth//token.pickle'):
    #         with open(f'{ad}//{str(self.id)}//auth//token.pickle', 'rb') as token:
    #             creds = pickle.load(token)
    #     service = build('drive', 'v3', credentials=creds,cache_discovery=False)
    #     li = service.about().get(fields = 'storageQuota').execute()
    #     # service = self.authorization().about().get(fields = 'storageQuota').execute()
        
        
    #     return int(li['storageQuota']['limit']) , int(li['storageQuota']['usage'])
    def download(self,link,id):
        self.queue_links.append(Downloade(self.id,link,self,id))
    
    
    
    def downloader(self):
        if len(self.downloads) < 2 and len(self.queue_links) > 0:
            print(len(self.downloads))
            down = self.queue_links.pop(0)

            # if self.chek(down.file_size):
            #     print(down.founder())
            if down.founder():
                #'youtube' in down.url[0] or 'youtu' in down.url[0]
                # self.__youtube_url_validation()
                if self.__is_youtubelink(down.url[0]):
                    down.yt_starter()
                    print('youtubeeeeeeeeeeeeeeeeee')
                    self.downloads.append(down)
                    #'magnet' in down.url[0]
                elif self.__is_magnet(down.url[0]):
                    print('magnet')

                    down.tor_starter()
                    self.downloads.append(down)
                    self.passe = True

                else:
                    down.starter()
                    self.downloads.append(down)
                    print(self.downloads)
            else:
                    # bot.loop.create_task()
                    task = asyncio.ensure_future(down.tgdownload(),loop=self.loop)
                    self.downloads.append(down)
                    # self.tg_download.append(down)
                    self.tasks.append((task,down.download_id))

                # pass
                    # await asyncio.ensure_future(down.tgdownload(),loop=loope)
                    # looper = False
                    # loop.run_until_complete(loop.create_task(down.tgdownload()))
                    # loop.run_until_complete(self.create_task(down))
                # else:
                    # print('tg old download')
                    # self.downloads.append(down)
                    # asyncio.ensure_future(down.tgdownload(), loop=loop)
                    #######################################################
                    # f1 = loop.create_task()

                    # loop.run_until_complete(await asyncio.wait([f1,]))
                    
                # print(self.downloads)

    # def add_link(self):
    #     if len(self.downloads) <= 2 and len(self.queue_links) > 0 :
    #         self.download(self.queue_links.pop(0))
    # async def create_task(self,down):
    #     global loop
    #     f1 = loop.create_task(down.tgdownload())

    #     await asyncio.wait([f1,])

    def cancel_download(self,id:int):
        down = None
        if id == -1:
            print('can\'t cancel this...' )
            return
        # print()
        for i in self.downloads:
            if i.download_id == id:
                # time.sleep(4)
                i.cancel = True
                print('ca')
                down = i
                break

        for j in self.tasks:
            if j[1] == id:
                # time.sleep(4)
                j[0].cancel()
                down.complete = True
                print('eu')
                return
        # for i in self.downloads:
        #     if i.download_id == id:
        #         i.cancel = True
        #         return

    def uploader(self):
        if self.uploads is None and len(self.paths) > 0:
            self.uploads = self.paths.pop(0)
            self.uploads.uploader()

    # def __deleter(self, user):
    #     os.remove(f'{self.realpath1}\\{user}\\Download')
    
    def user_deleter(self):
        if len(self.downloads)==0 and len(self.queue_links)==0 and len(self.paths)==0 and self.uploads is None:
            ad = os.path.split(os.path.abspath(__file__))[0]
            shutil.rmtree(f'{ad}//{str(self.id)}//Download')
            return True
        return False
    
    def deleter(self):
        if not self.uploads is None:
            if self.uploads.complete:
                try:
                    os.remove(self.uploads.address)
                except Exception as e:
                    print(str(e))
                finally:
                    self.uploads = None
    # @staticmethod

    @property
    def showe_downloads(self):
            text = ''
            for i in self.downloads:
                text+= i.show
                if i.complete and i.ready:
                    self.paths.append(Upload.Upload(i.user,i.address,i.mimtype))
                    self.downloads.remove(i)
                elif i.complete :
                    self.downloads.remove(i)
            text+=f'CC: @{self.user_name}\n'
            return text

    @property
    def show_uploads(self):
        text = ''
        if not self.uploads is None:
            text = self.uploads.show
            text += f'CC: @{self.user_name}\n'
            return text
        return text

    @property
    def show_in_queue_downloads(self):
        if len(self.downloads)>0:
            text = ''
            for i in self.queue_links:
                text += f'{i.name}\n'
                text += f'CC: @{self.user_name}\n'
                # print(text)
            return text
        return ''
    
    @property
    def show_in_queue_uploads(self):
        if len(self.paths)>0:
            text = ''
            for i in self.paths:
                text += f'{i.name}\n'
                text += f'CC: @{self.user_name}\n'
                # print(text)
            return text
        return ''

    
    


