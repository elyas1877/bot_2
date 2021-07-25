import os,sys
import shutil
from urllib.request import urlopen
# print(os.path.dirname(sys.argv[0]).replace('/','\\'))
# # wd = os.getcwd()
# os.path.split(os.path.abspath(__file__))[0]

r1 = urlopen('https://dl6.downloadha.com/hosein/animation/June2021/The.Owl.House.S02/720p.x264/The.Owl.House.S02E07.720p.HULU.WEBRip.x264-DLHA_www.Downloadha.com_.mkv')

print(r1.info())



