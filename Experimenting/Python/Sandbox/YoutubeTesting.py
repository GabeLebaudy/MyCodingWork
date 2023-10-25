from pytube import YouTube

#yt = YouTube('https://www.youtube.com/watch?v=bv6fypgX0Pg')
#yt = YouTube('https://www.youtube.com/watch?v=wzdCpJY6Y4c')
yt = YouTube('https://www.youtube.com/watch?v=Pbk__JC-NLc&t=18s')
print(yt.streams.filter(res='480p'))
print(yt.streams.filter(only_audio=True))
stream = yt.streams.get_by_itag(22)