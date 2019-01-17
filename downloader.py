# Online Photo Album Downloder 0.1.0
# -*- coding: utf-8 -*-
import requests, os, re, config, datetime
from bs4 import BeautifulSoup
from os.path import join, getsize
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
 
#import json  - to replace eval() later


# Configuration # Declarations?? Within same filer as class/def??

# Functions
        
def sqlalchemy_wrapper(type, table, values):
    '''Wraps SQLAlchemy commands.

    Type of operation and Command must be provided as an argument.'''
    
    Session = sessionmaker(bind=config.engine)
    session = Session()
    if type=="add":
        update = table(*values)
        session.add(update)
    if type=="query":
        values = session.query(table).first()
        return values
    session.commit()
        
def albums_list(username):
    '''Retrives list of albums for a given user.

    Username must be provided as an argument.'''
    
    #pageCount
   
    pass

def album_details(user_name, album_name):
    '''Retrives various details of a given album.

    User name and Album name must be provided as an argument.'''
 
    album_name = "https://" + user_name + ".rajce.idnes.cz/" + album_name
    print ("album_name: ", album_name)
    f = requests.get(album_name)
    soup = BeautifulSoup(f.text, "html.parser")
    soup = "".join(soup.script.contents)
    current_album_details = dict()
    
    for detail in config.RajceConstants.detail_name:
        #print ('Currently checking value for "{0}"'.format(detail))
        detail_value = find_between(soup, (config.RajceConstants.detail_start + detail + config.RajceConstants.detail_mid), config.RajceConstants.detail_end)
        #print ('Value of "{0}" equals "{1}"'.format(detail, detail_value))
        current_album_details.update({detail:detail_value})
    return current_album_details
    
def photos_list(photos):
    '''Retrives list of photos for a given album.

    Album link must be provided as an argument.'''
    false = False
    true = True
    g = eval(photos['photos'])
    for g in g: 
        photoID = g['photoID']  
        print("photoID :",photoID)
        fileName = g['fileName']  
        print("fileName :",fileName)    
        
def library_scan (mode, service, path):
    '''Scans local library either in "full" or "user" modes. 
    
    Mode and path link must be provided as an arguments.'''
    path = r"{0}".format(path)

    if mode=="full":
        print ("Performing full library scan")
        userlist = list()
        for username in os.listdir(path):
            if os.path.isdir(os.path.join(path,username)):
                userlist.append(username)
            albumlist = list()
            for albumname in os.listdir(os.path.join(path,username)):
                if os.path.isdir(os.path.join(path,username,albumname)):
                    albumlist.append(albumname)
            print (albumlist)
            # for root, dirs, files in os.walk(path, topdown = True, followlinks = False):
            # for dirname in dirs:
                # print("Album:", dirname, end=" ")
                # dirname_path = os.path.join(root, dirname)
                #dirname = os.path.join(root, dirName)
                # #print("Size:",os.stat(dirname_path).st_size, end=" ") 
                # timestamp = os.stat(dirname_path).st_ctime
                # print("Created:",datetime.datetime.fromtimestamp(timestamp))
                # for files in os.walk(dirname_path, topdown = True, followlinks = False):
                    # for name in files:
                        # print("File: ", name)
            #for name in files:
                #print(os.path.join(name), end=" ")
                #name = os.path.join(root, name)
                #print("Size:",os.stat(name).st_size, end=" ") 
                #timestamp = os.stat(name).st_ctime
                #print("Created:",datetime.datetime.fromtimestamp(timestamp))
                #values = download_dir, rajce_sub_dir
                #sqlalchemy_wrapper("add", config.PathConfig, values)

    if mode=="user":
        print ("Performing library scan for current user")

    

def library_update (username, album_name):
    '''Checks for local copy of user albums or photos within the album.

    Username or album link must be provided as an argument. Function will check following items:
    - which albums/photos were downloaded before;
    - if size of a photo or number of photos in the album changed; 
    - which albums/photos were deleted/modified/protected on the server, lable affected items with a corresponding flag;
    - add changes to the report.'''
    pass
    
def detect_tags(name):
    '''Detect tags in file or directory name.

    File or directory name must be provided as an argument. Function will detect tags in the provided name (both prefixes and suffixes). "-" is considered as tag identifier.
    TODO - find out how to work with complex file names including "-" in the name. Use "~"? "="?
    Function returns list of prefixes, suffixes and clean filenames.
    '''
    pass
    
def path_sanity_check(path):
    '''Checks if directory exists and either cerates it ("mkdir" parameter) or returns details ("ls" parameter), such as file list, file sizes, file dates, file tags etc.
    
    TODO 
    - how to work with tags? Both for dir name and file names. 
    - how to present data? List of lists? List of dictionaries?

    Path must be provided as an argument.'''
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)    

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
        
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
    
def yes_no_question(question):
    '''Warap Yes/No question and returns selected value.

    Question must be provided as an argument.'''
    
    answer = None
    while answer not in ("yes", "no", "y", "n"):
        answer = input("{0} (please enter yes or no): ".format(question)).lower()
        if answer in ("yes", "y"):
            answer = "yes" 
        elif answer in ("no", "n"):
            answer = "no"
        else:
            print("Please enter yes or no.")
    return answer

# Main program
def main():
    '''The main module of the Online Photo Album Downloader.

    No arguments needed.'''
    
    #print ("Save path:", join(config.download_dir,config.rajce_sub_dir))
    #albums = ("Lenka_na_terase", "soulad_rukou_a_tela")
    #for album in albums:
    #    d = album_details("standa-werba", album)
    #    photos_list(d)
    
if __name__== "__main__":
    main()


