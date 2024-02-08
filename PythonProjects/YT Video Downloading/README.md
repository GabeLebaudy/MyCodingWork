# Youtube Video Download App

After YouTube implemented a new feature to prevent users from using adblockers on their site, I remembered a video a while back about a library capable of downloading YouTube videos.

I created an app that is able to download an mp4 file of the video given it's URL, however a problem I ran into is that for videos in 1080p, the only way to download in that resolution is to download the video and audio streams separately, and then use FFmpeg to combine them.

This requires FFmpeg to be downloaded and added to the system path. For some videos there are some resolutions that you are able to download with a single stream, which allows you to do it without this extension, but many of the videos I've tried in testing required separate streams.

This app may have many bugs, as I have been planning on using it to automate downloading from specific channels, and haven't gotten around to it yet.
