# import os,sys
# import shutil
# from urllib.request import urlopen
from pytube import YouTube,streams,request
# import mimetypes
# import re
# # print(os.path.dirname(sys.argv[0]).replace('/','\\'))
# # # wd = os.getcwd()
# # os.path.split(os.path.abspath(__file__))[0]

# # r1 = urlopen('https://dl6.downloadha.com/hosein/animation/June2021/The.Owl.House.S02/720p.x264/The.Owl.House.S02E07.720p.HULU.WEBRip.x264-DLHA_www.Downloadha.com_.mkv')

# # print(r1.info())
# # el = '/help 123'.removeprefix('/help ')
# # print(el)
yt = YouTube('https://youtu.be/vKYF84UXQGI')
stream = yt.streams.get_highest_resolution()
name = stream.default_filename
filename_prefix = stream.filename_prefix
print(name)
# with open('C:\\Users\\Elyas\\Documents\\1.mp4', 'wb') as f:
#     stream = request.stream(stream.url)
#     while True:
#         chunk = next(stream, None)
#         if chunk:
#             f.write(chunk)
#         else:
#             break
# # print(stream.resolution ,stream.abr , stream.filesize)
# for i in stream:
#     print(i)
    # if i.resolution and i.abr:
    #     print(i.resolution ,i.abr , i.filesize)
    # if  i.abr and i.resolution is None :
    #     print(i.abr , i.filesize)
# # name = yt.title
# # print(name,mimetypes.guess_extension(stream.mime_type))
# # # print(yt.views)
# # # for i in range(8):
# # #     if i == 4:
# # #         continue
# # #     print(i)
# # url = 'https://www.youtube.com/watch?v=KHnX8ItCZL4&pp=sAQA'
# # print(re.match('^(https?\:\/\/)?((www\.)?youtube\.com|youtu\.?be)\/.+$',url))

# def youtube_url_validation(url):
#     youtube_regex = (
#         r'(https?://)?(www\.)?'
#         '(youtube|youtu)\.(com|be)/'
#         '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

#     youtube_regex_match = re.match(youtube_regex, url)
#     if youtube_regex_match:
#         return youtube_regex_match

#     return youtube_regex_match

# youtube_urls_test = [
#     'http://www.youtube.com/watch?v=5Y6HSHwhVlY',
#     'http://youtube.com/watch?v=5Y6HSHwhVlY',
#     'http://youtu.be/5Y6HSHwhVlY', 
#     'http://www.youtube.com/embed/5Y6HSHwhVlY?rel=0" frameborder="0"',
#     'https://www.youtube-nocookie.com/v/5Y6HSHwhVlY?version=3&amp;hl=en_US',
#     'http://www.youtube.com/',
#     'http://www.youtube.com/?feature=ytca']


# for url in youtube_urls_test:
#     m = youtube_url_validation(url)
#     if m:
#         print('OK {}'.format(url))
#         print(True)
#         print(m.group())
#         # print(m.group(6))
#     else:
#         print(False)

#         print('FAIL {}'.format(url))
# #   postgres://wfjhajuqtgqoas:c42d169cacfc005ef1d88eae9c674423d57ba535c2aafeecf77ef7f7ad93b699@ec2-3-226-134-153.compute-1.amazonaws.com:5432/d9leiaac4kshrh




