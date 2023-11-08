#This will be the thread where the youtube video download process is happening. Since this takes up an execution point, 

#Imports
from PyQt6.QtCore import QThread, QMutex, QWaitCondition, pyqtSignal
from pytube import YouTube
import ffmpeg
import os
import re
import subprocess
import cv2

#Download Thread
class Downloader(QThread):
    #Signals
    videoInformationSignal = pyqtSignal(list)
    downloadInfo = pyqtSignal(str)
    invalidUrlSignal = pyqtSignal()
    downloadProgressSignal = pyqtSignal(float)
    downloadCompleteSignal = pyqtSignal(int)

    #Constructor
    def __init__(self):
        super().__init__()
        self.videoURL = None
        self.outputDir = None
        self.videoRes = None
        self.fileExtension = None
        self.downloadType = 0

    #Setter Methods
    def setURL(self, url):
        self.videoURL = url

    #Set File Output Path
    def setOutputPath(self, path):
        self.outputDir = path

    #Set the video resolution
    def setVideoRes(self, res):
        self.videoRes = res

    #Set the file extension
    def setFileExt(self, ext):
        self.fileExtension = ext

    #Download function. Set as the threads main function as to create a new execution point for the code so that the code doesn't time out
    def run(self):
        #Reset Progress Bar
        self.downloadProgressSignal.emit(0)
        
        try:        
            url = self.videoURL
            yt = YouTube(url, on_progress_callback=self.downloadProgress, on_complete_callback=self.downloadComplete)
            streams = self.getBestStream(yt)
        except Exception as e:
            print(e)
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

        for i in range(len(streams)):
            #Streams is an audio and video, and the current iteration is for the audio
            if i == 1:
                self.downloadType = 1
                audioTitle = yt.title + ' Audio.mp4'
                audioTitle = self.fixYtTitle(audioTitle)
                self.downloadInfo.emit('Downloading Audio...')
                streams[i].download(self.outputDir, audioTitle)
            else:    
                if len(streams) > 1:
                    self.downloadType = 1
                    mainTitle = yt.title + ' Main.mp4'
                    mainTitle = self.fixYtTitle(mainTitle)
                    streams[i].download(self.outputDir, mainTitle)
                else:
                    self.downloadType = 0
                    streams[i].download(self.outputDir)
        
        #If audio and video files were both downloaded, combine both files
        self.downloadInfo.emit('Connecting video and audio files...')
        if len(streams) > 1:
            self.mendStreams(yt)

    #Progress callback function, emits a float value containing percentage of the video that has been downloaded.
    def downloadProgress(self, stream, rawData, bytesLeft):
        videoSize = stream.filesize
        bytesDownloaded = videoSize - bytesLeft
        percentDownloaded = (bytesDownloaded / videoSize) * 100
        self.downloadProgressSignal.emit(percentDownloaded)
    
    #Download complete callback, plays audio, and sets the download info to complete.
    def downloadComplete(self, stream, fileOutputPath):
        self.downloadInfo.emit('Download Complete!')
        #0: Stream contains audio and vide 1: Stream was video only 2: Stream was audio.
        self.downloadCompleteSignal.emit(self.downloadType)

    #Get the stream with the best possible resolution. 
    def getBestStream(self, ytObj):
        #Get the index of selected resolution
        availableRes = ['1080p', '720p', '480p', '360p', '144p']
        for i in range(len(availableRes)):
            if self.videoRes == availableRes[i]:
                startInd = i
                break
        
        #If the selected res is 1080, both a video and audio stream is needed
        #Get available streams with current res
        found = False
        while not found and startInd < len(availableRes):
            #Search for resolution with audio
            availableStreams = ytObj.streams.filter(res=availableRes[startInd], audio_codec="mp4a.40.2")
            if len(availableStreams) > 0:
                stream = availableStreams[0]
                return [stream]
            else:
                #Search for resolution without audio
                availableStreams = ytObj.streams.filter(res=availableRes[startInd])
                if len(availableStreams) > 0:
                    #Stream is available, without audio. Find audio stream and splice them together
                    allAudios = ytObj.streams.filter(only_audio=True)
                    
                    #Check if there is audio streams
                    if len(allAudios) > 0:
                        audioStream = allAudios[0]
                        videoStream = availableStreams[0]
                        return [videoStream, audioStream]
                    else:
                        startInd += 1 
                    
                else:
                    #There are no available streams with that resolution, so try the next highest available option.   
                    startInd += 1 

    #Mend Video and Audio Files
    def mendStreams(self, yt):
        mainFileTitle = yt.title + ' Main.mp4'
        mainFileTitle = self.fixYtTitle(mainFileTitle)
        audioFileTitle = yt.title + ' Audio.mp4'
        audioFileTitle = self.fixYtTitle(audioFileTitle)  
        finishedVideoTitle = yt.title + ' Complete.mp4'
        finishedVideoTitle = self.fixYtTitle(finishedVideoTitle)

        videoFilePath = os.path.join(self.outputDir, mainFileTitle)
        audioFilePath = os.path.join(self.outputDir, audioFileTitle)
        finishedVideoPath = os.path.join(self.outputDir, finishedVideoTitle)

        #Get total amount of video frames
        video = cv2.VideoCapture(videoFilePath)
        frameCount = video.get(cv2.CAP_PROP_FRAME_COUNT)

        #Define input video and audio streams
        vidInput = ffmpeg.input(videoFilePath)
        audInput = ffmpeg.input(audioFilePath)

        
        #Combine video and audio streams        
        cmd = ffmpeg.concat(vidInput, audInput, v=1, a=1).output(finishedVideoPath).compile()
    
        # Run the command and capture the output
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=1, shell=True)

        prior = 0
        while True:
            output = process.stderr.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                items = output.split()
                print(items)
                try:
                    #Find if the array has the time value, and if so what index of the output line
                    frameInd = self.findFrames(items)
                    if frameInd == 0 or frameInd == 1: #Odd syntax, but necessary
                        if frameInd == 1:
                            frames = int(items[frameInd])
                        else:
                            frameStr = items[frameInd]
                            frames = int(frameStr[6:])
                            
                        percentCompleted = (frames / frameCount) * 100
                        if prior <= percentCompleted:
                            prior = percentCompleted
                            print(percentCompleted, prior)
                            self.downloadProgressSignal.emit(percentCompleted)

                except Exception as e:
                    #This will handle all lines that do not follow the progress update format
                    print(e)

        # Get the return code of the process
        return_code = process.poll()

        if return_code == 0:
            self.downloadCompleteSignal.emit(2)
        else:
            print(f"Error running ffmpeg command. Return code: {return_code}")

        #TODO: Delete audio and video files
        
        self.downloadInfo.emit('Download Complete!')
        
    #Fix the title by removing the characters
    def fixYtTitle(self, title):
        title = re.sub(r'[^\w\-_\. ]', '_', title)
        title = title.replace('|', '_')
        return title 
    
    #Find the time value in the FFmpeg concatenate method
    def findFrames(self, lineArr):
        if not lineArr:
            return False
        

        if lineArr[0] == 'frame=':
            return 1
        if lineArr[0][:6] == 'frame=':
            return 0
        return False





