import User
import os
from socket import timeout
# from re import T
from urllib.request import urlopen , Request
import urllib.error, urllib.parse
import libtorrent as lt
from pytube import YouTube,request,streams
import threading
import time
import pickle
import zipfile
import shutil
# from pyrogram import Client
import bot
from googleapiclient.discovery import build
import random
import math
from DB import google_drive_DB
import mimetypes

# import test_2
# app = Client(api_id=5975714,session_name='BACK2gCuzoLPCD1cEBt8xlxdQ0RXnHHiQkzDFlCi_hGRTYJvGchW3jyVdqFQvpSsF4pCXa2UCEkXosrWmlbJ_uA2V-3bU5mM0ep5455ui_LDTxUQvCPdsscNrHNXWmV9XFrux4OSZtu-rcnsDcnZO3ZVmnTzyDd9cqGv00AqQ5xUUX1Q1J8BjDs825JMmohFjlOAJ6qA1Q0o-TtW2KLcQN8EC5w8naV1EA7ZvnG1WTcJdO-t8ILKrtQHMFdxNBlgQ76rQjv82O7kI99AMBWEUo3r_QkVIPr3sUyqKEsrgusm7Ef6g2OoDG6AaeiybU7pS0-sI3Tlv6fRbQ1lXYX8CH5EZ0EVuAA',api_hash='8d1ea6da21f3ddb0426938c3975fb0e7')
    # app.DOWNLOAD_WORKERS = 4
# app.start()

class Downloade:
    def __init__(self,user:int,url :str,info:User,id:int):
        self.user = str(user)
        self.realpath = os.path.split(os.path.abspath(__file__))[0]
        self.status = None
        self.file_size = 0
        self.download_id = id
        self.pre = None
        self.complete = False
        self.ready = False
        self.url = url
        self.persent = 0
        self.start_time = None
        self.address = None
        self.cancel = False
        self.task = None
        self.dl_file_size = 0
        self.download_speed = 0
        self.info_ = info
        self.name = None
        # if url[0] is not None: 
        #     if 'youtube' in url[0] or 'youtu' in url[0]:
        #         video = YouTube(url[0])
        #         video_type = video.streams.get_highest_resolution()
        #         self.file_size = int(video_type.filesize)
        #     else:
        #         try:
        #             self.name = str(url[0]).split('/')[-1]
        #             # print('#####################')
        #             # print(self.name)
        #             # print('#####################')
        #             r1=urlopen(url[0])
        #             meta = r1.info()
        #             # print(meta)
        #             self.file_size = int(meta['Content-Length'])
        #             print(self.file_size)
        #         except:
        #             print('error')
        # else:
        #     self.name = url[1].document.file_name
        #     self.file_size = int(url[1].document.file_size)

        self.previousprogress = 0
        self.mimtype = None
        # self.tgaccount = Client(api_id=5975714,session_name='BACK2gCuzoLPCD1cEBt8xlxdQ0RXnHHiQkzDFlCi_hGRTYJvGchW3jyVdqFQvpSsF4pCXa2UCEkXosrWmlbJ_uA2V-3bU5mM0ep5455ui_LDTxUQvCPdsscNrHNXWmV9XFrux4OSZtu-rcnsDcnZO3ZVmnTzyDd9cqGv00AqQ5xUUX1Q1J8BjDs825JMmohFjlOAJ6qA1Q0o-TtW2KLcQN8EC5w8naV1EA7ZvnG1WTcJdO-t8ILKrtQHMFdxNBlgQ76rQjv82O7kI99AMBWEUo3r_QkVIPr3sUyqKEsrgusm7Ef6g2OoDG6AaeiybU7pS0-sI3Tlv6fRbQ1lXYX8CH5EZ0EVuAA',api_hash='8d1ea6da21f3ddb0426938c3975fb0e7')
        
    def __download_with_prograss(self,file_size: int):
        if file_size == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(file_size, 1024)))
        p = math.pow(1024, i)
        s = round(file_size / p, 2)
        return "%s %s" % (s, size_name[i])

    def info(self):
        # ad = os.path.split(os.path.abspath(__file__))[0]
        # print(f'{self.realpath}//{self.user}//auth//token.pickle')
        #os.path.exists(f'{self.realpath}//{self.user}//auth//token.pickle')
        
        if google_drive_DB._chek(int(self.user)):
            # with open(f'{self.realpath}//{self.user}//auth//token.pickle', 'rb') as token:
            #     creds = pickle.load(token)
            creds = google_drive_DB.search(int(self.user))
            service = build('drive', 'v3', credentials=creds,cache_discovery=False)
            li = service.about().get(fields = 'storageQuota').execute()
            # token.close()
            return int(li['storageQuota']['limit']) , int(li['storageQuota']['usage'])
        else:
            return


    def chek(self):
        on_prossess = 0
        on_prossess += int(self.file_size)
        print('insert size : ',on_prossess)
        print(self.file_size)
        limit , storage = self.info()
        on_prossess += storage
        print('storage + insert sizs : ',on_prossess)

        for prossess in self.info_.downloads:
            print(self.info_.user_name)
            if prossess.download_id == self.download_id:
                continue
            on_prossess += prossess.file_size
        
        # print(downloads on_prossess)

        try:
            on_prossess += self.info_.uploads.size
            print(on_prossess)

        except:
            print('upload error')
            pass
        al = limit - on_prossess
        # print('size : ',self.__download_with_prograss(al * -1))
        if al >= 0 :
            print('size : ',al)
            return True
        return False



    def founder(self):
        if self.url[0] is not None:
            return True
        return False
                                                                                                                                            #,self.download_speed//1024
    @property
    def show(self) -> str:

        return 'Name : {}\nStatus : {}\nsize : {}\n{}\n[{} {}]\nspeed :{} \n ID : {}\n'.format(self.name,self.status,self.__download_with_prograss(self.file_size),self.pre,int(self.persent//10)*'#',int(10 - (self.persent//10) ) * '_',self.__download_with_prograss(self.download_speed),self.download_id)
    


    def get_random_useragent(self):
        '''
        Returns a random popular user-agent.
        Taken from `here <http://techblog.willshouse.com/2012/01/03/most-common-user-agents/>`_, last updated on 2020/09/19.
        
        :returns: user-agent
        :rtype: string
        '''
        l = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15"
        ]
        return random.choice(l)

    def __direct_link(self,url):
        try:
            print(url,'link')
            req = Request(url,data=None,headers={'User-Agent':f'{self.get_random_useragent()}'})
            r1=urlopen(req,timeout=20)
        except urllib.error.HTTPError as e:
            if e.code == 416 or e.code == 404 or e.code == 403 :
                self.status = 'not working...'
                print(self.status,'1')
                self.complete = True
                return
        except timeout: 
            self.status = 'not working...'
            self.complete = True
            return
        Download = 'Download'
        self.name = str(url).split('/')[-1]
        fullname = self.name

        if '%' in fullname:
            self.name = fullname.replace('%','')

        ex = os.path.join(self.realpath, self.user,'Download')
        if not os.path.exists(ex):
            os.makedirs(ex)

        f = open(f'{self.realpath}//{self.user}//{Download}//{fullname}', 'wb')
        self.start_time = time.perf_counter()
        try:
            meta = r1.info()
            self.file_size = int(meta['Content-Length'])
            print (f"Downloading: {fullname} size: {self.__download_with_prograss(self.file_size)}")
        except (IndexError, KeyError, TypeError):
            print('error')
            self.status = 'not working...'
            print(self.status,'2')
            self.complete = True
            return
        if self.chek():
            block_sz = 1024
            self.status = 'Downloading...'
            print('########@@@@@@@@@@@@@@@@@')
            print(self.name)
            print('########@@@@@@@@@@@@@@@@@')
            while True:
                try:
                    buffer = r1.read(block_sz)
                except Exception as e:
                    print(str(e))
                    print('err!!!')
                    self.__direct_link(url)
                if not buffer:
                    break
                if self.cancel:
                    f.close()
                    r1.close()
                    os.remove(f'{self.realpath}//{self.user}//{Download}//{fullname}')
                    break
                self.dl_file_size += len(buffer)
                # print(self.dl_file_size)
                f.write(buffer)
                self.download_speed = self.dl_file_size//(time.perf_counter() - self.start_time)
                # print(self.download_speed)
                self.persent =  self.dl_file_size * 100. / self.file_size
                status = r"%10d  [%3.2f%%]" % (self.dl_file_size, self.persent)
                self.pre = status + chr(8)*(len(status)+1)
                # time.sleep(1)
                # print(self.pre)
                # print(self.show)
            if self.cancel:
                self.complete = True 
                return

            self.complete = True 
            self.ready = True
            self.address = f'{self.realpath}//{self.user}//{Download}//{fullname}'
            self.status = 'Preparing for upload...'
            r1.close()
            f.close()
        else:
            self.status = 'free up space...'
            self.complete = True
            r1.close()
            f.close()
            return

    def starter(self):
        try:
            threading.Thread(target=self.__direct_link,args=(self.url[0],)).start()
            print('elyas')
        except:
            print('error!')

    def zipdir(self,path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file), 
                        os.path.relpath(os.path.join(root, file), 
                                        os.path.join(path, '..')))

    def torrent(self,link):
        counter = 0
        ses = lt.session()
        ses.listen_on(6881, 6891)
        # 'save_path': f'E:\\torrent',
        # yam = lt.storage_mode_t(2)
        ex = os.path.join(self.realpath, self.user,'Download')
        if not os.path.exists(ex):
            os.makedirs(ex)
        params = {
            'save_path' : f'{self.realpath}//{self.user}//Download//',
            'storage_mode': lt.storage_mode_t(2),
            'paused': False,
            'auto_managed': True,
            'duplicate_is_error': True}

        print(link)

        handle = lt.add_magnet_uri(ses, link, params)
        ses.start_dht()

        # begin = time.time()
        # print(datetime.datetime.now())

        print ('Downloading Metadata...')
        self.status = 'Downloading Metadata...'
        while (not handle.has_metadata()):
            time.sleep(1)
            counter+=1
            if self.cancel:
                try:
                    ses.remove_torrent(handle)
                except:
                    pass
                self.complete = True
                return

            if counter == 1200:
                self.status = 'not working...'
                try:
                    ses.remove_torrent(handle)
                except:
                    pass
                self.complete = True
                return
        
        print ('Got Metadata, Starting Torrent Download...')
        if handle.has_metadata():
            

            print("Starting", )
            self.name = handle.name()
            self.file_size = int(handle.get_torrent_info().total_size())
            print(self.file_size)
            if self.chek():
                try:
                    while (handle.status().state != lt.torrent_status.seeding):
                        s = handle.status()
                        state_str = ['queued', 'checking', 'downloading metadata', \
                                'downloading', 'finished', 'seeding', 'allocating']
                        # print ('%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s ' % \
                        #         (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                        #         s.num_peers, state_str[s.state]))
                        if self.cancel:
                            try:
                                ses.remove_torrent(handle)
                                break
                            except:
                                pass
                        self.status = state_str[s.state]
                        self.download_speed = s.download_rate
                        self.persent = float(s.progress * 100)
                        self.pre = r"%10d  [%3.2f%%]" % (0, self.persent)
                        time.sleep(1)
                except:
                    self.status = 'not working...'
                    try:
                        ses.remove_torrent(handle)
                    except:
                        pass
                    time.sleep(3)
                    if os.path.isdir(f'{self.realpath}//{self.user}//Download//{self.name}'):
                        shutil.rmtree(f'{self.realpath}//{self.user}//Download//{self.name}')
                        self.complete = True
                        print(1)
                        return
                    else:
                        os.remove(f'{self.realpath}//{self.user}//Download//{self.name}')
                        self.complete = True
                        return
                    # pass
                # end = time.time()
                # zer = '.zip'
                if self.cancel:
                    try:
                        ses.remove_torrent(handle)
                    except:
                        pass
                    time.sleep(3)
                    if os.path.isdir(f'{self.realpath}//{self.user}//Download//{self.name}'):
                        shutil.rmtree(f'{self.realpath}//{self.user}//Download//{self.name}')
                        self.complete = True
                        print(2)
                        return
                    else:
                        os.remove(f'{self.realpath}//{self.user}//Download//{self.name}')
                        self.complete = True
                        return

                time.sleep(5)
                ses.remove_torrent(handle)
                self.address = f'{self.realpath}//{self.user}//Download//{self.name}'
                if os.path.isdir(self.address):
                        self.status = 'comperssing...'
                        zipf = zipfile.ZipFile(f'{self.address}.zip', 'w', zipfile.ZIP_DEFLATED)
                        self.zipdir(self.address, zipf)
                        try:
                            shutil.rmtree(self.address)
                        except:
                            pass
                        zipf.close()
                        self.address = f'{self.address}.zip'

                self.complete = True
                self.ready = True
                self.status = 'Preparing for upload...'
                print(handle.name(), "COMPLETE")
            else:
                print('here handle!')
                ses.remove_torrent(handle)
                print('here handle2!')
                self.status = 'free up space...'
                time.sleep(5)
                ad = f'{self.realpath}//{self.user}//Download//{self.name}'
                print(ad)
                print('is dir : ',os.path.isdir(ad))
                if os.path.isdir(ad):
                    try:
                        print('removing!')
                        shutil.rmtree(self.address)
                        print('removing2!')
                    except:
                        pass
                else:
                    try:
                        print('removing 2!')
                        os.remove(ad)
                    except:
                        pass
                self.complete = True
                return
                


        # print("Elapsed Time: ",int((end-begin)//60),"min :", int((end-begin)%60), "sec")
        # print(datetime.datetime.now())  

    def tor_starter(self):
        try:
            threading.Thread(target=self.torrent,args=(self.url[0],)).start()
            print('elyas')
        except:
            print('error!')

    def __progress(self , current, total):
        # self.file_size
        # print('downloading..s.')
        # self.dl_file_size +=current
        # print(current)
        # print(self.dl_file_size)
        self.download_speed = current//(time.perf_counter() - self.start_time)
        self.persent = (float)(current * 100 / self.file_size )
        self.pre = r"%10d  [%3.2f%%]" % (current, self.persent)
        # print(self.pre)
        # print('elyas ... 11')

    async def tgdownload(self):
        # print(file_info)
        print('first')
        ex = os.path.join(self.realpath, self.user,'Download')
        if not os.path.exists(ex):
            os.makedirs(ex)
        # with Client(api_id=5975714,session_name='BACK2gCuzoLPCD1cEBt8xlxdQ0RXnHHiQkzDFlCi_hGRTYJvGchW3jyVdqFQvpSsF4pCXa2UCEkXosrWmlbJ_uA2V-3bU5mM0ep5455ui_LDTxUQvCPdsscNrHNXWmV9XFrux4OSZtu-rcnsDcnZO3ZVmnTzyDd9cqGv00AqQ5xUUX1Q1J8BjDs825JMmohFjlOAJ6qA1Q0o-TtW2KLcQN8EC5w8naV1EA7ZvnG1WTcJdO-t8ILKrtQHMFdxNBlgQ76rQjv82O7kI99AMBWEUo3r_QkVIPr3sUyqKEsrgusm7Ef6g2OoDG6AaeiybU7pS0-sI3Tlv6fRbQ1lXYX8CH5EZ0EVuAA',api_hash='8d1ea6da21f3ddb0426938c3975fb0e7') as app:
        #    app.start()
        #    app.send_message('me','hello')
        file_info = self.url[1]
        if file_info.document is None:
            self.mimtype=file_info.video.mime_type
            print(self.mimtype)
            self.name = file_info.video.file_name
            if self.name == None:

                self.name = f'VID-{file_info.from_user.id}-{file_info.message_id}{mimetypes.guess_extension(self.mimtype)}'
            self.file_size = int(file_info.video.file_size)
        else:
            self.name = file_info.document.file_name
            self.file_size = int(file_info.document.file_size)
            self.mimtype=file_info.document.mime_type

        # self.tgaccount.connect()
        # ()
        # user_bot.main(file_info.message_id)
        # user_bot.downloader(file_info.message_id,self.__progress)
        # trd.start()
        # app.start()
        print('second')
        print(file_info.message_id)
        # self.name = file_info.document.file_name
        # self.file_size = int(file_info.document.file_size)
        # print(file_info.document.file_size)
        # print(self.name)
        if self.chek():
            self.address = f'{self.realpath}//{self.user}//Download//{self.name}'
            print(self.address)
            self.status = 'Downloading...'
            # try:
            print('stert download media')
            self.start_time = time.perf_counter()
            try:
                mess = await bot.tel.Client.get_messages(-1001172803610,file_info.message_id)
                print(mess)
                await bot.tel.Client.download_media(message=mess,file_name=self.address,progress=self.__progress)
            except:
                self.complete = True
                return
                # pass
                # await app.send_message('me','hello')
                # print(mess)
            
            # except Exception as e:
            #     print(str(e))
            #     print('error')
            #     self.status = 'not working...'
            #     time.sleep(4000)
            #     self.tgdownload()
            if self.cancel:
                self.complete = True
                return
            
            self.ready = True
            self.complete = True
            print('complete')
            self.status = 'Preparing for upload...'
        else:
            self.complete = True
            self.status = 'free up space...'
            return

        # app.stop()

    # def tg_starter(self):
    #     try:
    #         threading.Thread(target=self.__tgdownload,args=(self.url[1],)).start()
    #         print('start tg downloader')
    #         # threading.Thread(target=self.tgaccount.start()).start()
    #         # threading.Thread(target=self.tgaccount.start).start()
    #     except Exception as e:
    #         print(str(e))
    #         print('error!')


    # def __on_progress(self,stream, chunk, bytes_remaining):
    #     bytes_downloaded = self.file_size - bytes_remaining 
    #     self.persent = (float)(bytes_downloaded / self.file_size * 100)
    #     if self.persent > self.previousprogress:
    #         self.previousprogress = self.persent
    #         #print("{:00.0f}% downloaded".format(self.persent))
    #         #self.pre = "{:00.0f}% downloaded".format(self.persent)
    #         self.pre = r"%10d  [%3.2f%%]" % (bytes_downloaded, self.persent)
    #         print(self.pre)

       
    def __downloadYouTube(self,url:str):
        yt_url = url
        Download = 'Download'
        print(yt_url)
        ex = os.path.join(self.realpath, self.user,'Download')
        if not os.path.exists(ex):
            os.makedirs(ex)
        print ("Accessing YouTube URL...")
        try:
            video = YouTube(yt_url)
        except:
            print("ERROR. Check your:\n  -connection\n  -url is a YouTube url\n\nTry again.")
            print('error')
            self.status = 'not working...'
            self.complete = True
            return
#  video_type
        #Get the first video type - usually the best quality.
        try:
            strm = video.streams
        except:
            self.status = 'not working...'
            self.complete = True
            return
        tag = int(self.url[1])
        for i in strm:
            if  tag == i.itag:
                video_type = i
        self.name = video_type.default_filename
        if self.name is None:
            title = video_type.title
            self.name = f'{title}[yt]{mimetypes.guess_extension(video_type.mime_type)}'
        
        print(self.name)
        print(video_type.filesize)
        self.file_size = int(video_type.filesize)
        if self.chek():
            print(self.download_id)
        #Gets the title of the video
            # title = video.title
            #Prepares the file for download
            print ("Fetching: {}...".format(title))
            print(title)
            #Starts the download process
            self.start_time = time.perf_counter()
            try:
                self.status = 'Downloading...'
                with open(f'{self.realpath}//{self.user}//Download//{self.name}', 'wb') as f:
                    stream = request.stream(video_type.url)
                    while True:
                        if self.cancel:
                            f.close()
                            os.remove(f'{self.realpath}//{self.user}//{Download}//{self.name}')
                            self.status = 'Canceld...'
                            self.complete = True
                            return
                        chunk = next(stream, None)
                        if chunk:
                            f.write(chunk)
                            self.dl_file_size += len(chunk)
                            self.download_speed = self.dl_file_size//(time.perf_counter() - self.start_time)
                            self.persent =  self.dl_file_size * 100. / self.file_size
                            status = r"%10d  [%3.2f%%]" % (self.dl_file_size, self.persent)
                            self.pre = status + chr(8)*(len(status)+1)
                        else:
                            break
                # pt = video_type.download(f'{self.realpath}//{self.user}//{Download}',title)
                # print(pt)
            except Exception as e:
                # f.close()
                self.status = 'Downloading...'
                try:
                    with open(f'{self.realpath}//{self.user}//Download//{self.name}', 'wb') as f:
                        stream = request.seq_stream(video_type.url)
                        while True:
                            if self.cancel:
                                f.close()
                                os.remove(f'{self.realpath}//{self.user}//{Download}//{self.name}')
                                self.status = 'Canceld...'
                                self.complete = True
                                return
                            chunk = next(stream, None)
                            if chunk:
                                f.write(chunk)
                                self.dl_file_size += len(chunk)
                                self.download_speed = self.dl_file_size//(time.perf_counter() - self.start_time)
                                self.persent =  self.dl_file_size * 100. / self.file_size
                                status = r"%10d  [%3.2f%%]" % (self.dl_file_size, self.persent)
                                self.pre = status + chr(8)*(len(status)+1)
                            else:
                                break
                except:
                    self.status = 'not working...'
                    self.complete = True
                    return
                # print(str(e))
                # print('error...!')
                # self.status = 'not working...'

                # self.complete = True
                # time.sleep(4000)
                # return
                # self.__downloadYouTube(url)

            print ("Ready to download another video.\n\n")
            self.complete = True
            self.ready = True
            self.status = 'Preparing for upload...'
            self.address = f'{self.realpath}//{self.user}//Download//{self.name}'
            self.mimtype = video_type.mime_type
        else:
            self.complete = True
            self.status = 'free up space...'
            return
    def yt_starter(self):
        try:
            threading.Thread(target=self.__downloadYouTube,args=(self.url[0],)).start()
            print('elyas')
        except Exception as e:
            print(str(e))
            print('error!')

        # @property
        # def show(self) -> str:
        #     sharp = '#'
        #     under = '_'
        #     return f'{self.name} : is {self.status} \n size : {self.__download_with_prograss(self.file_size)} \n {self.pre} \n [{self.persent//10 * sharp} {((self.persent//10) - 10 )*under}] \n\n '

