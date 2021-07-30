from __future__ import print_function
import pickle
from googleapiclient.http import MediaFileUpload
from pytube import YouTube
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
import os,sys
import magic
import threading
import math
import time
class Upload:

    def __init__(self,id :str ,path :str , mimtype = None):
        self.realpath1 = os.path.split(os.path.abspath(__file__))[0]
        self.SCOPE = ['https://www.googleapis.com/auth/drive']
        self.size = 0  
        self.address = None
        self.cancel = False
        self.status = None
        self.name = path.split('//')[-1]
        self.complete = False
        self.pre = None
        self.id = id
        self.upload_speed = 0
        self.path = path
        self.mimtype = mimtype
        self.persent = 0
        self.start_time = None
        self.up =0

    def __download_with_prograss(self,file_size: int):
        if file_size == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(file_size, 1024)))
        p = math.pow(1024, i)
        s = round(file_size / p, 2)
        return "%s %s" % (s, size_name[i])



    def authorization(self):
        try:
            creds = None
            auth = 'auth'
            print(self.realpath1)
            if os.path.exists(f'{self.realpath1}//{str(self.id)}//{auth}//token.pickle'):
                with open(f'{self.realpath1}//{str(self.id)}//{auth}//token.pickle', 'rb') as token:
                    creds = pickle.load(token)
        except:
            print('not auth!')
            return None
        return build('drive', 'v3', credentials=creds,cache_discovery=False)



    @staticmethod
    def check(id) -> bool:
        ad = os.path.split(os.path.abspath(__file__))[0]
        if os.path.exists(f'{ad}//{str(id)}//auth//token.pickle'):
            return True

        return False

    @staticmethod
    def revoke(id):
        try:
            ad = os.path.split(os.path.abspath(__file__))[0]
            os.remove(f'{ad}//{str(id)}//auth//token.pickle')
        except:
            pass

    @property
    def show(self) -> str:
        # print(self.size,'elyas')
        return 'Name : {}\nStatus : {}\nsize : {}\n{}\n[{} {}]\nspeed: {}\n'.format(self.name,self.status,self.__download_with_prograss(self.size),self.pre,int(self.persent//10)*'#',int(10 - (self.persent//10) ) * '_',self.__download_with_prograss(self.upload_speed))

    def Upload(self,path:str,mimtype = None):
        try:
            size :int = os.path.getsize(path)
        except:
            return
        
        self.size = size
        name = self.name
        print(name)
        if mimtype is None:
            mime = magic.Magic(mime=True)

            if(size>0):
                file_metadata = {'name': name ,'mimeType': f'{mime.from_file(path)}'}
            print('File Is None!')
        else:
            if(size>0):
                file_metadata = {'name': name ,'mimeType': mimtype}
            print('File Is None!')

        drive_service = self.authorization()
        if drive_service is None:
            return
        media = MediaFileUpload(path,
                                resumable=True, 
                                mimetype='image/jpeg',
                                chunksize=256*1024)
            
        file = drive_service.files().create(supportsTeamDrives=True,body=file_metadata,media_body=media)
        resp = None
        print(self.__download_with_prograss(size))
        print(self.size)
        self.status = 'uploading...'
        self.up =0
        self.start_time = time.perf_counter()
        while resp is None:
            try:
                status, resp = file.next_chunk()
                if(size>=256*1024):
                    self.up +=256*1024
                    self.upload_speed = self.up//(time.perf_counter() - self.start_time)
                    size-=256*1024
                    # size=self.__download_with_prograss(size)
                if self.cancel:
                    self.complete = True
                    self.address = path
                    return
                if status:
                    self.pre = r'%10d [%3.2f%%]' % (size,status.progress()*100)

                    self.persent = int(status.progress()*100)
                    # print(self.show)
                    # print(self.status)
            except HttpError as err:
                print(err)
                self.Upload(path,self.mimtype)
        print('Done!')
        
        self.address = path
        self.complete = True
        
    
    def uploader(self):
        try:
            threading.Thread(target=self.Upload,args=(self.path,self.mimtype)).start()
        except:
            print('not upload...!')


'''
help
'[####______]'
'''