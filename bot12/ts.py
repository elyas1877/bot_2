import os,sys
import shutil
from urllib.request import urlopen
from pytube import YouTube
# print(os.path.dirname(sys.argv[0]).replace('/','\\'))
# # wd = os.getcwd()
# os.path.split(os.path.abspath(__file__))[0]

# r1 = urlopen('https://dl6.downloadha.com/hosein/animation/June2021/The.Owl.House.S02/720p.x264/The.Owl.House.S02E07.720p.HULU.WEBRip.x264-DLHA_www.Downloadha.com_.mkv')

# print(r1.info())
# el = '/help 123'.removeprefix('/help ')
# print(el)
yt = YouTube('https://www.youtube.com/watch?v=KHnX8ItCZL4&pp=sAQA')
print(yt.views)
# # print(yt.views)
# # for i in range(8):
# #     if i == 4:
# #         continue
# #     print(i)


#   postgres://wfjhajuqtgqoas:c42d169cacfc005ef1d88eae9c674423d57ba535c2aafeecf77ef7f7ad93b699@ec2-3-226-134-153.compute-1.amazonaws.com:5432/d9leiaac4kshrh




