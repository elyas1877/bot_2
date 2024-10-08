from youtube_dl.utils import preferredencoding
import User
import os,sys
from socket import timeout
# from re import T
#
from urllib.request import urlopen , Request
import urllib.error, urllib.parse
import libtorrent as lt
import youtube_dl
import threading
import time
import pickle
import zipfile
import shutil
import logging
# from pyrogram import Client
import bot
from googleapiclient.discovery import build
import random
import math
from DB import google_drive_DB
import mimetypes
# logging.basicConfig(level=logging.WARNING)
class thread_with_trace(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run	
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
            return self.localtrace

    def kill(self):
        self.killed = True
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
        self.task :thread_with_trace = None
        self.dl_file_size = 0
        self.download_speed = 0
        self.info_ = info
        self.name = None
        self.etas=0
        self.mimtype = None
        
    def __download_with_prograss(self,file_size: int):
        if file_size == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(file_size, 1024)))
        p = math.pow(1024, i)
        s = round(file_size / p, 2)
        return "%s %s" % (s, size_name[i])
    
    def TimeFormatter(self,milliseconds: int) -> str:
        seconds, milliseconds = divmod(int(milliseconds), 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        tmp = ((str(days) + " days, ") if days else "") + \
            ((str(hours) + " hours, ") if hours else "") + \
            ((str(minutes) + " min, ") if minutes else "") + \
            ((str(seconds) + " sec, ") if seconds else "") + \
            ((str(milliseconds) + " millisec, ") if milliseconds else "")
        return tmp[:-2]

    def __convert_etas(self,file_time):
        if file_time == 0:
            return 'No Time!'
        return self.TimeFormatter(file_time)
        

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
        # print('nameeeeeeee : ',self.name)
        # print('statusssssss : ',self.status)
        # print('file_sizeeeeeeeeeeee : ',self.file_size)
        # print('preeeeeeeeeeeeee : ',self.pre)
        # print('persenttttttttt : ',self.persent)
        # print('download_speedddddddd : ',self.download_speed)
        # print('download_iddddddddd : ',self.download_id)
        # print('Name : {}\nStatus : {}\nsize : {}\n{}\n[{} {}]\nspeed :{} \n ID : {}\n'.format(self.name,self.status,self.__download_with_prograss(self.file_size),self.pre,int(self.persent//10)*'#',int(10 - (self.persent//10) ) * '_',self.__download_with_prograss(self.download_speed),self.download_id))
        return 'Name : {}\nStatus : {}\nsize : {}\n{}\n[{}{}]\nspeed :{} \nTime Left :{} \nID :{}\n'.format(self.name,self.status,self.__download_with_prograss(self.file_size),self.pre,int(self.persent//10)*'▓',int(10 - (self.persent//10) ) * '▒',self.__download_with_prograss(self.download_speed),self.__convert_etas(self.etas),self.download_id)
    


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
                self.etas = round(((self.file_size - self.dl_file_size) / self.download_speed)) * 1000
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
    # def log(self,ses):
    #     alert = ses.pop_alert()
    #     while alert:
    #         alert = ses.pop_alert() 
    #         logging.warning("[%s] %s" % (type(alert), alert.__str__()))

    def torrent(self,link):
        counter = 0
        # ses = lt.session()
        # ses.listen_on(6881, 6891)
        # ses.add_extension('ut_metadata')
        # ses.add_extension('ut_pex')
        # ses.add_extension('metadata_transfer')
        # ses.add_dht_router("router.utorrent.com", 6881)
        # ses.add_dht_router("router.bittorrent.com", 6881)
        # ses.add_dht_router("dht.transmissionbt.com", 6881)
        # ses.add_dht_router("dht.aelitis.com", 6881)
        # ses.start_dht()
        # ses.start_lsd()
        # ses.start_upnp()
        # ses.start_natpmp()
        # 'save_path': f'E:\\torrent',
        # yam = lt.storage_mode_t(2)
        ex = os.path.join(self.realpath, self.user,'Download')
        if not os.path.exists(ex):
            os.makedirs(ex)
        params = {
            'save_path' : f'{self.realpath}//{self.user}//Download//',
            'storage_mode': lt.storage_mode_t(2)
            }

        print(link)
        if link is os.path.isfile(link):
            pass
        else:
            ses = bot.Torrent()
            handle = ses.add_magnet_url(link, params)

            # threading.Thread(target=self.log,args=(bot.lib.ses,)).start()

        # begin = time.time()
        # print(datetime.datetime.now())

        print ('Downloading Metadata...')
        self.status = 'Downloading Metadata...'
        while (not handle.has_metadata()):
            time.sleep(1)
            counter+=1
            if self.cancel:
                try:
                    ses.ses.remove_torrent(handle)
                except:
                    pass
                self.complete = True
                return

            if counter == 1200:
                self.status = 'not working...'
                try:
                    ses.ses.remove_torrent(handle)
                except:
                    pass
                self.complete = True
                return
        
        print ('Got Metadata, Starting Torrent Download...')
        if handle.has_metadata():
            

            print("Starting", )
            self.name = handle.name()
            # s = handle.status()
            self.file_size = int(handle.get_torrent_info().total_size())
            print(self.file_size)
            if self.chek():
                try:
                    while (handle.status().state != lt.torrent_status.seeding):
                        s = handle.status()
                        # print(s)
                        state_str = ['queued', 'checking', 'downloading metadata', \
                                'downloading', 'finished', 'seeding', 'allocating']
                        # print ('%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s ' % \
                        #         (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                        #         s.num_peers, state_str[s.state]))
                        if self.cancel:
                            try:
                                ses.ses.remove_torrent(handle)
                                break
                            except:
                                pass
                        # print(s.)
                        self.status = state_str[s.state]
                        self.download_speed = s.download_rate
                        self.persent = float(s.progress * 100)
                        self.dl_file_size = s.total_download
                        try:
                            self.etas = round(((self.file_size - self.dl_file_size) / self.download_speed)) * 1000
                        except:
                            pass
                        self.pre = r"%10d  [%3.2f%%]" % (self.dl_file_size, self.persent)
                        # alerts = ses.pop_alerts()
                        # for a in alerts:
                        #     if a.category() & lt.alert.category_t.error_notification:
                        #         print(a)
                        time.sleep(1)
                except Exception as e:
                    print(e)
                    self.status = 'not working...'
                    # alerts = ses.pop_alerts()
                    # for a in alerts:
                    #     if a.category() & lt.alert.category_t.error_notification:
                    #         print(a)
                    try:
                        ses.ses.remove_torrent(handle)
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
                        ses.ses.remove_torrent(handle)
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
                ses.ses.remove_torrent(handle)
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
                ses.ses.remove_torrent(handle)
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
        self.etas = round(((self.file_size - current) / self.download_speed)) * 1000
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

    def my_hook(self,pro):
            # if self.cancel:
            #     print('error')
            #     raise SystemExit()
            current = int(pro['downloaded_bytes'])
            self.status = pro['status']
            self.download_speed = int(current//(time.perf_counter() - self.start_time))
            self.etas = round(((self.file_size - current) / self.download_speed)) * 1000

            self.persent = (float)(current * 100 / int(pro['total_bytes']) )
            self.pre = r"%10d  [%3.2f%%]" % (current, self.persent)
    def __downloadYouTube(self,url:str):
        yt_url = url
        # Download = 'Download'
        print(yt_url)
        ex = os.path.join(self.realpath, self.user,'Download')
        if not os.path.exists(ex):
            os.makedirs(ex)
        print ("Accessing YouTube URL...")
        save_path = f'{self.realpath}//{self.user}//Download//'
        format = self.url[1]
        # self.name = 
        ydl_opts = {
                    'outtmpl': save_path + '%(title)s-%(id)s.%(ext)s',
                    'format' : format,
                }

        self.name = self.url[3]
        self.file_size = int(self.url[2])
        print(self.file_size)
        if self.chek():
            try:
                time.sleep(3)
                ydl = youtube_dl.YoutubeDL(ydl_opts) 
                self.status = 'Downloading...'
                # self.download_id = -1
                self.start_time = time.perf_counter()
                ydl.add_progress_hook(self.my_hook)
                ie_result = ydl.extract_info(yt_url, True)
                name = ydl.prepare_filename(ie_result)
                if name.endswith('.webm') and '+' in format:
                    name = name.replace('.webm','.mkv')
                print ("Ready to download another video.\n\n")
                self.address = f'{name}'
                # self.name = '33'
                print(self.address)
                self.status = 'Preparing for upload...'
                # ydl.__exit__()
                # return
                print ("comp")
                    # self.mimtype = video_type.mime_type
                    # print(name)
            except:
                print("ERROR. Check your:\n  -connection\n  -url is a YouTube url\n\nTry again.")
                print('error')
                self.status = 'not working...'
                self.complete = True
                return
        else:
            self.complete = True
            self.status = 'free up space...'
            return
        print('compelet')
        self.complete = True
        self.ready = True
    def yt_starter(self):
        try:
            # self.task :thread_with_trace
            self.task=thread_with_trace(target=self.__downloadYouTube,args=(self.url[0],))
            self.task.start()
            # threading.Thread(target=self.wh).start()
            print('elyas')
        except Exception as e:
            print(str(e))
            print('error!')

        # @property
        # def show(self) -> str:
        #     sharp = '#'
        #     under = '_'
        #     return f'{self.name} : is {self.status} \n size : {self.__download_with_prograss(self.file_size)} \n {self.pre} \n [{self.persent//10 * sharp} {((self.persent//10) - 10 )*under}] \n\n '

