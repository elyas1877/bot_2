import os,sys

print(os.path.dirname(sys.argv[0]).replace('/','\\'))
# wd = os.getcwd()
os.path.split(os.path.abspath(__file__))[0]