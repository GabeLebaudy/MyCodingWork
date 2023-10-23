#This will be the thread where the youtube video download process is happening. Since this takes up an execution point, 

#Imports
from PyQt6.QtCore import QThread, QMutex, QWaitCondition, pyqtSignal
from pytube import YouTube


#Download Thread
class Downloader(QThread):
    #Signals
    thumbnailUrlSignal = pyqtSignal(str)
    descriptionSignal = pyqtSignal(str)
    videoLoadedSignal = pyqtSignal()

    #Constructor
    def __init__(self):
        self.videoURL = None


    #Setter Methods
    def setURL(self, url):
        self.videoURL = url

    #Download function. Set as the threads main function as to create a new execution point for the code so that the code doesn't time out
    def run(self):
        try:        
            url = self.videoURL
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            self.videoLoadedSignal.emit()
        except:
            self.urlInput.setText('')
            self.openStandardDialog('Error', 'Please enter a valid youtube URL.')
            return None
        
        #Set the thumbnail picture under the current video tab
        thumbnailURL = yt.thumbnail_url
        self.thumbnailUrlSignal.emit(thumbnailURL)
        
        '''
        videoThumbnail = QPixmap()

        sampleUrl = yt.thumbnail_url
        urlResponse = urllib.request.urlopen(sampleUrl).read()
        videoThumbnail.loadFromData(urlResponse)
        videoThumbnail.setDevicePixelRatio(1.75)

        self.thumbnailContainer.setPixmap(videoThumbnail)
        '''

        #Add a description beneath the video thumbnail
        ytDescription = yt.description
        #self.videoDescription.setText(ytDescription)
    

