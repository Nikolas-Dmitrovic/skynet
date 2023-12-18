import moviepy.editor as mp
from tiktok import tts,tts_batch #parse this shit to only have needed functions to cute down to run time
import random
import math
#https://github.com/linto-ai/whisper-timestamped
import whisper_timestamped


#my optiziation approch: https://www.youtube.com/watch?v=4K8IEzXnMYk&ab_channel=UgiBugi



textFileLocation = "textfile.txt"
masterText = open(textFileLocation,'r')
content = masterText.read().replace("\n","").rsplit(".")

tts_files = []

#TODO funnel these into a folder
for i,nText in enumerate(content):
    tts_files.append(tts('4edc1d459f309a464fcfdf11e75e55d9', 'en_us_006', nText, f'tts{i}.mp3')["duration"])
'''for i in range(20):
    tts_files.append(tts('4edc1d459f309a464fcfdf11e75e55d9', 'en_us_006', content[i], f'tts{i}.mp3')["duration"]) #duration in seconds?
    '''

#TODO subdivide audio clips into n second duratuins

audioclips = []

for i in range (20):
    audioclips.append(mp.AudioFileClip(f"tts{i}.mp3"))
    #TODO delete mp3s after appending them
audio1 = mp.concatenate_audioclips(audioclips)
new_audioclip = mp.CompositeAudioClip([audio1])
new_audioclip.write_audiofile("audio.mp3", 44100)


videoLocation = "vid.mp4"

video = mp.VideoFileClip(videoLocation)
videoDuration =math.floor(video.duration)

subClipLength = 60 #seconds
subClipStart=random.randint(0,videoDuration - subClipLength)
subClip = video.subclip(subClipStart, subClipLength + subClipStart)


#totaly did not steal this code
client = whisper_timestamped.load_model("base")
results = whisper_timestamped.transcribe(client,"audio.mp3")
print(results["segments"])
subs = []
subs.append(subClip)
for segment in results["segments"]:
    for word in segment["words"]:
        text = word["text"].upper()
        start = word["start"]
        end = word["end"]
        duration = end - start
        text_clip = mp.TextClip(txt=text,fontsize=40,color="white").set_start(start).set_duration(duration).set_position(("center", "center"))
        subs.append(text_clip)

    #subs.append(text_clip)

#final_subs = mp.concatenate(subs)
subClip = mp.CompositeVideoClip(subs)
subClip.audio = new_audioclip
subClip.write_videofile("example.mp4")