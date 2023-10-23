#This will be the thread where the youtube video download process is happening. Since this takes up an execution point, 

#Imports
from PyQt6.QtCore import QThread, QMutex, QWaitCondition, pyqtSignal
from pytube import YouTube


#Download Thread
class Downloader(QThread):
    #Signals
    videoInformationSignal = pyqtSignal(list)
    downloadInfo = pyqtSignal(str)
    invalidUrlSignal = pyqtSignal()

    #Constructor
    def __init__(self):
        super().__init__()
        self.videoURL = None
        self.outputDir = None

    #Setter Methods
    def setURL(self, url):
        self.videoURL = url

    #Set File Output Path
    def setOutputPath(self, path):
        self.outputDir = path

    #Download function. Set as the threads main function as to create a new execution point for the code so that the code doesn't time out
    def run(self):
        try:        
            url = self.videoURL
            yt = YouTube(url)
            stream = yt.streams.get_by_itag(22)
        except:
            self.invalidUrlSignal.emit()
            return None
        
        #Get Information about the video
        vidTitle = yt.title
        thumbnailURL = yt.thumbnail_url
        ytDescription = yt.description
        publishDate = yt.publish_date
        publishDate = publishDate.strftime("%m/%d/%Y")

        self.videoInformationSignal.emit([vidTitle, thumbnailURL, ytDescription, publishDate])

        self.downloadInfo.emit('Downloading Video...')

        stream.download(self.outputDir)

