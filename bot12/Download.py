import os,sys
# from re import T
from urllib.request import urlopen 
import urllib.error, urllib.parse
import libtorrent as lt
from pytube import YouTube
import threading
import time
import zipfile
import shutil
# from pyrogram import Client
import bot
import math
# import test_2
# app = Client(api_id=5975714,session_name='BACK2gCuzoLPCD1cEBt8xlxdQ0RXnHHiQkzDFlCi_hGRTYJvGchW3jyVdqFQvpSsF4pCXa2UCEkXosrWmlbJ_uA2V-3bU5mM0ep5455ui_LDTxUQvCPdsscNrHNXWmV9XFrux4OSZtu-rcnsDcnZO3ZVmnTzyDd9cqGv00AqQ5xUUX1Q1J8BjDs825JMmohFjlOAJ6qA1Q0o-TtW2KLcQN8EC5w8naV1EA7ZvnG1WTcJdO-t8ILKrtQHMFdxNBlgQ76rQjv82O7kI99AMBWEUo3r_QkVIPr3sUyqKEsrgusm7Ef6g2OoDG6AaeiybU7pS0-sI3Tlv6fRbQ1lXYX8CH5EZ0EVuAA',api_hash='8d1ea6da21f3ddb0426938c3975fb0e7')
    # app.DOWNLOAD_WORKERS = 4
# app.start()

class Downloade:
    def __init__(self,user:int,url :str):
        self.user = str(user)
        self.realpath = os.path.split(os.path.abspath(__file__))[0]
        self.status = None
        self.file_size = 0
        self.pre = None
        self.complete = False
        self.ready = False
        self.url = url
        self.persent = 0
        self.start_time = None
        self.address = None
        self.cancel = False
        self.dl_file_size = 0
        self.download_speed = 0
        if url[0] is not None: 
            if 'youtube' in url[0] or 'youtu' in url[0]:
                video = YouTube(url[0])
                video_type = video.streams.get_highest_resolution()
                self.file_size = int(video_type.filesize)
            else:
                try:
                    self.name = str(url[0]).split('/')[-1]
                    # print('#####################')
                    # print(self.name)
                    # print('#####################')
                    r1=urlopen(url[0])
                    meta = r1.info()
                    # print(meta)
                    self.file_size = int(meta['Content-Length'])
                    print(self.file_size)
                except:
                    print('error')
        else:
            self.name = url[1].document.file_name
            self.file_size = int(url[1].document.file_size)

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

    def founder(self):
        if self.url[0] is not None:
            return True
        return False
                                                                                                                                            #,self.download_speed//1024
    @property
    def show(self) -> str:

        return '{} : is {}\nsize : {}\n{}\n[{} {}]\nspeed :{} \n'.format(self.name,self.status,self.__download_with_prograss(self.file_size),self.pre,int(self.persent//10)*'#',int(10 - (self.persent//10) ) * '_',self.__download_with_prograss(self.download_speed))
    
    def __direct_link(self,url):
        try:
            print(url,'link')
            r1=urlopen(url)
        except urllib.error.HTTPError as e:
            if e.code == 416 or e.code == 404:
                self.status = 'not working...'
                print(self.status,'1')
                self.complete = True
                return
        Download = 'Download'
        fullname = self.name
        if '%' in fullname:
            self.name = fullname.replace('%','')
        else:
            self.name = fullname
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
        self.complete = True 
        self.ready = True
        self.address = f'{self.realpath}//{self.user}//{Download}//{fullname}'

        r1.close()
        f.close()

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
        while (not handle.has_metadata()):
            time.sleep(1)
            counter+=1
            if counter == 60:
                self.status = 'not working...'
                self.complete = True
                return
            
        print ('Got Metadata, Starting Torrent Download...')
        if handle.has_metadata():

            print("Starting", )
            self.name = handle.name()
            self.file_size = int(handle.get_torrent_info().total_size())

            while (handle.status().state != lt.torrent_status.seeding):
                s = handle.status()
                state_str = ['queued', 'checking', 'downloading metadata', \
                        'downloading', 'finished', 'seeding', 'allocating']
                # print ('%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s ' % \
                #         (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                #         s.num_peers, state_str[s.state]))
                self.status = state_str[s.state]
                self.download_speed = s.download_rate
                self.persent = float(s.progress * 100)
                self.pre = r"%10d  [%3.2f%%]" % (0, self.persent)
                time.sleep(1)
            # end = time.time()
            # zer = '.zip'

            self.address = f'{self.realpath}//{self.user}//Download//{self.name}'
            if os.path.isdir(self.address):
                    self.status = 'comperssing...'
                    zipf = zipfile.ZipFile(f'{self.address}.zip', 'w', zipfile.ZIP_DEFLATED)
                    self.zipdir(self.address, zipf)
                    shutil.rmtree(self.address)
                    zipf.close()
                    self.address = f'{self.address}.zip'

            self.complete = True
            self.ready = True
            print(handle.name(), "COMPLETE")

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
        print('downloading..s.')
        self.dl_file_size +=current
        # print(current)
        # print(self.dl_file_size)
        self.download_speed = current//(time.perf_counter() - self.start_time)
        self.persent = (float)(current * 100 / self.file_size )
        self.pre = r"%10d  [%3.2f%%]" % (current, self.persent)
        print(self.pre)
        print('elyas ... 11')

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
        # self.tgaccount.connect()
        # ()
        # user_bot.main(file_info.message_id)
        # user_bot.downloader(file_info.message_id,self.__progress)
        # trd.start()
        # app.start()
        print('second')
        print(file_info.message_id)
        self.name = file_info.document.file_name
        self.file_size = int(file_info.document.file_size)
        # print(file_info.document.file_size)
        # print(self.name)
        self.address = f'{self.realpath}//{self.user}//Download//{self.name}'
        print(self.address)
        self.status = 'Downloading...'
        # try:
        print('stert download media')
        self.start_time = time.perf_counter()
        try:
            mess = await bot.tel.Client.get_messages(-1001172803610,file_info.message_id)
            print(mess)
            await bot.tel.Client.download_media(message=mess,file_name=self.address,progress=self.__progress,)
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
        
        self.mimtype=file_info.document.mime_type
        self.ready = True
        self.complete = True
        print('complete')
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


    def __on_progress(self,stream, chunk, bytes_remaining):
        bytes_downloaded = self.file_size - bytes_remaining 
        self.persent = (float)(bytes_downloaded / self.file_size * 100)
        if self.persent > self.previousprogress:
            self.previousprogress = self.persent
            #print("{:00.0f}% downloaded".format(self.persent))
            #self.pre = "{:00.0f}% downloaded".format(self.persent)
            self.pre = r"%10d  [%3.2f%%]" % (bytes_downloaded, self.persent)
            print(self.pre)

       
    def __downloadYouTube(self,url:str):
        yt_url = url
        Download = 'Download'
        print(yt_url)
        ex = os.path.join(self.realpath, self.user,'Download')
        if not os.path.exists(ex):
            os.makedirs(ex)
        print ("Accessing YouTube URL...")
        try:
            video = YouTube(yt_url, on_progress_callback=self.__on_progress)
        except:
            print("ERROR. Check your:\n  -connection\n  -url is a YouTube url\n\nTry again.")
            print('error')
            self.status = 'not working...'
            self.complete = True
            return
 
        #Get the first video type - usually the best quality.
        video_type = video.streams.get_highest_resolution()
        print(video_type.filesize)
        self.file_size = int(video_type.filesize)
        #Gets the title of the video
        title = video.title
        #Prepares the file for download
        print ("Fetching: {}...".format(title))
        print(title)
        self.name = title
        #Starts the download process
        try:
            self.status = 'Downloading...'
            pt = video_type.download(f'{self.realpath}//{self.user}//{Download}',title)
            print(pt)
        except Exception as e:
            print(str(e))
            print('error...!')
            self.status = 'not working...'
            time.sleep(4000)
            self.__downloadYouTube(url)

        print ("Ready to download another video.\n\n")
        self.previousprogress = 0
        self.complete = True
        self.ready = True
        self.address = pt
        self.mimtype = video_type.mime_type
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

