import moviepy.editor as mp
from tiktok import tts,tts_batch #TODO parse this shit to only have needed functions to cute down to run time
import random
import math
#https://github.com/linto-ai/whisper-timestamped
import whisper_timestamped




textFileLocation = "textfile.txt" 
masterText = open(textFileLocation,'r') #possible error if file not found
content = masterText.read().replace("\n","").replace("?",".").rsplit(".") #possible error if non text/assci charecters


centoSecondCount = 0
start = 0
end = 0
count = 60*100 #seconds to centoseconds conversion
audiocliplib = []

audioclips = []


#TODO funnel these into a folder
for i,nText in enumerate(list(filter(str.strip, content))):
    #TODO add error handling for bad files
    
    audioDuration = tts('4edc1d459f309a464fcfdf11e75e55d9', 'en_us_006', nText, f'tts{i}.mp3')["duration"] #duration in centoseconds which is stupid
    #TODO see if you can feed a 64bit encoded audiofile into audiofileclip below
    audioclips.append(mp.AudioFileClip(f"tts{i}.mp3"))
    #TODO delete mp3s after appending them

    if centoSecondCount + int(audioDuration) < count:
        centoSecondCount += int(audioDuration)
    else:
        end += centoSecondCount
        audiocliplib.append({"start": start, "end": end}) #TODO maybe read file locations from this
        start=end
        centoSecondCount = 0

#addes last clip if less than n seconds
end += centoSecondCount
audiocliplib.append({"start": start, "end": end})

audio1 = mp.concatenate_audioclips(audioclips)
new_audioclip = mp.CompositeAudioClip([audio1])
new_audioclip.write_audiofile("audio.mp3", 44100)

# the length of this is undregulated
# check if audio file is longer than video

videoLocation = "vid.mp4"

video = mp.VideoFileClip(videoLocation)
videoDuration =math.floor(video.duration)

if new_audioclip.duration > videoDuration:
    pass
    #TODO something

#totaly did not steal this code
#TODO this may need to be its own fucntion
client = whisper_timestamped.load_model("base")
results = whisper_timestamped.transcribe(client,"audio.mp3")
print(results["segments"])
subs = []
subs.append(video)
for segment in results["segments"]:
    for word in segment["words"]:
        text = word["text"].upper()
        start = word["start"]
        end = word["end"]
        duration = end - start
        text_clip = mp.TextClip(txt=text,fontsize=40,color="white").set_start(start).set_duration(duration).set_position(("center", "center"))
        subs.append(text_clip)


subs.append(text_clip)

#TODO naming may be confusing
subClip = mp.CompositeVideoClip(subs)
subClip.audio = new_audioclip

#break up example.mp4 
for i,info in enumerate(audiocliplib):
    subClip.subclip(info["start"], info["end"]).write_videofile(f"example{i}.mp4")