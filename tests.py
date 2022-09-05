from email.mime import image
from detect import run

if __name__ =='__main__':
   potato =  run(weights=r"best.pt", source='test')
   print(potato)