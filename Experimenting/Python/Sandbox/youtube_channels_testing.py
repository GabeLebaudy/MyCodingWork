#This file will be used to test out the channel object of the pytube library

#Imports
from pytube import Channel

#Main method
if __name__ == "__main__":
    channel_id = "UCxcTeAKWJca6XyJ37_ZoKIQ"
    channel_url = f"https://www.youtube.com/channel/{channel_id}"
    c = Channel(channel_url)
    print(c.channel_name)
    print(c.videos)

    #Directly replacing '@' with '%40' from channel URL: Produces original error:
    """ channelName = "https://www.youtube.com/%40ThePatMcAfeeShow"
    d = Channel(channelName)
    print(c.channel_name)
    print(c.videos) """

    channel_name = 'https://www.youtube.com/c/ThePatMcAfeeShow'
    pc = Channel(channel_name)
    print(pc.channel_name)
    print(pc.video_urls)