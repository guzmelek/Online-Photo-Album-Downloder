# Config for Online Photo Album Downloder 0.1.0
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from downloader import path_sanity_check, sqlalchemy_wrapper, cls, yes_no_question, library_scan


cls() 
Base = declarative_base()

script_path = os.path.dirname(os.path.realpath(__file__))
global db_file
db_file = os.path.join(script_path, 'downloader.db')
os.remove(db_file)

class UserVariables:
    """User defined variables."""
    SECRET_KEY = 'you-will-never-guess'
  
class RajceConstants:
    """Constants for rajce.idnes.cz."""
 
    #Album details section
    detail_start = "var "
    detail_mid = " = "
    detail_end = ";"
    detail_name = [
        "albumID",
        "albumServerDir",
        "storage",
        "albumSecurityCode",
        "albumSecTicket",
        "photos"
        ]
        
    #   photos - dictionary? https://stackoverflow.com/questions/6388187/what-is-the-proper-way-to-format-a-multi-line-dict-in-python
        
    #	<meta name="description" content="10 fotek na Rajčeti, pořízeno 28. 5. 2018"/>
    
# Creating tables and updating config table. Extra block to be added for each service (only Rajce for now)
class PathConfig(Base):
    __tablename__ = 'config'
    id = Column(Integer, primary_key=True)
    DownloadDir = Column(String(250), nullable=True)
    rajceSubDir = Column(String(250), nullable=True)
    
    def __init__(self, DownloadDir, rajceSubDir):
        self.DownloadDir = DownloadDir
        self.rajceSubDir = rajceSubDir
    
class User(Base):
    __tablename__ = 'user'
    albumUserID = Column(Integer, primary_key=True)
    albumUserName = Column(String(250))
    serviceName = Column(String(250)) #Only Rajce for now
    localTags = Column(String(250), nullable=True)
    lastUpdated = Column(String(250), nullable=True)
    lastDownloaded = Column(String(250), nullable=True)
    NumberOfLocalAlbums = Column(Integer, nullable=True)
    NumberOfRemoteAlbums = Column(Integer, nullable=True)

class Album(Base):
    __tablename__ = 'album'
    albumID = Column(Integer, primary_key=True)
    albumName = Column(String(250))
    localPrefix = Column(String(250), nullable=True)
    localTags = Column(String(250), nullable=True)
    lastUpdated = Column(String(250), nullable=True)
    lastDownloaded = Column(String(250), nullable=True)
    NumberOfLocalPhotos = Column(Integer, nullable=True)
    NumberOfRemotePhotos = Column(Integer, nullable=True)
    albumUserID_id = Column(Integer, ForeignKey('user.albumUserID'))
    albumUserID = relationship(User)

class Photo(Base):
    __tablename__ = 'photo'
    photoID = Column(Integer, primary_key=True)
    photoName = Column(String(250))
    localPrefix = Column(String(250), nullable=True)
    localTags = Column(String(250), nullable=True)
    lastUpdated = Column(String(250), nullable=True)
    lastDownloaded = Column(String(250), nullable=True)
    RemoteFileSize = Column(Integer, nullable=True)
    LocalFileSize = Column(Integer, nullable=True)
    albumID_id = Column(Integer, ForeignKey('album.albumID'))
    albumID = relationship(Album)
    
engine = create_engine('sqlite:///{0}'.format(db_file))
    
#Regular config 
if os.path.exists(db_file):
    print ("Regular config being used")
    print ()

    Base.metadata.create_all(engine)
    #download_dir = sqlalchemy_wrapper("query", PathConfig,"").DownloadDir
    #rajce_sub_dir = sqlalchemy_wrapper("query", PathConfig,"").rajceSubDir

#Initial config    
else:
    print ("It looks like this is the first time you are using Online Photo Album Downloder.")
    print ("We will now ask you a few questions to configure the script.")
    print ()
    
    #Setting up parameters
    #Download folder aka local library
    download_dir = input("Please select Download Folder aka Local Library (default 'Downloads' in script working directory): ") or "Downloads"
    path_sanity_check(download_dir)
    
    #Setting up subfolders for services. Extra block to be added for each service
    #Rajce subfolder (default rajce.idnes.cz)
    rajce_sub_dir = input("Please select Rajce subfolder (default 'rajce.idnes.cz'): ") or "rajce.idnes.cz"
    rajce_path = os.path.join(script_path, download_dir, rajce_sub_dir)
    path_sanity_check(rajce_path)
    
    Base.metadata.create_all(engine)
    values = download_dir, rajce_sub_dir
    sqlalchemy_wrapper("add", PathConfig, values)
    
    #Would you like to scan your local library?
    library_scan_trigger = yes_no_question("Would you like to scan your local library?")
    if library_scan_trigger == "yes":
        redownload_flag = yes_no_question("Would you like to download missing, untagged photos or consider these deleted as not intertesting?")
        #Scanning ligrary for supported services. Extra line to be added for each service
        library_scan("full", "rajce", rajce_path)
    #cls() 

