import platform
import os

if (platform.system() == 'Windows'):    
    try:
        print('Installing Audio Drivers for Windows ...')    
        os.system('pip3 install pypiwin32')
    except BaseException as e:  
        print(str(e))      
elif (platform.system() == 'Darwin'):
    try:
        print('Installing Audio Drivers for iOS ...')    
        os.system('ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" < /dev/null 2> /dev/null')
    except BaseException as e:  
        print(str(e))      
    try:
        os.system('brew install espeak')
    except BaseException as e:  
        print(str(e))                 
elif (platform.system() == 'Linux'):
    try:
        print('Installing Audio Drivers for Debian ...')    
        os.system('sudo apt update && sudo apt install espeak ffmpeg libespeak1')
        
        #TODO: Add for Feodora and other flavors of Linux
        #os.system('sudo dnf upgrade && sudo dnf install espeak ffmpeg libespeak1')
    except BaseException as e:  
        print(str(e))        