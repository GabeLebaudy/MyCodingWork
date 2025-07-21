#For temporary download of youtube videos

#Imports
import os
from pytubefix import YouTube

def main():
    youtube_vid = YouTube("https://www.youtube.com/watch?v=OqPxaKs8xrk&t=1s")
    stream = youtube_vid.streams.get_by_itag(399)
    o_path = os.path.join(os.path.dirname(__file__), "parkour_output")
    stream.download(output_path=o_path)

if __name__ == "__main__":
    main()