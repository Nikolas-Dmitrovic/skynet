import moviepy.editor as mp
import ImageMagic
from tiktok import tts,tts_batch #parse this shit to only have needed functions to cute down to run time
import random
import math
#https://github.com/openai/whisper
import whisper_timestamped


#my optiziation approch: https://www.youtube.com/watch?v=4K8IEzXnMYk&ab_channel=UgiBugi


''' TTS file generations'''

#TODO format the fucking text file, break 200 bits along periods and commas

# defines the location of the text file and opens it
textFileLocation = "textfile.txt"
masterText = open(textFileLocation,'r')
content = masterText.read().replace("\n","").rsplit(".")




#feed text segments into tts
tts_files = []


#for i,nText in enumerate(content):
    #tts('4edc1d459f309a464fcfdf11e75e55d9', 'en_us_006', nText, f'tts{i}.mp3')
    #tts_files.append(tts('4edc1d459f309a464fcfdf11e75e55d9', 'en_us_006', nText, f'tts{i}.mp3')["duration"])
for i in range(20):
    tts_files.append(tts('4edc1d459f309a464fcfdf11e75e55d9', 'en_us_006', content[i], f'tts{i}.mp3')["duration"]) #duration in seconds?

print(tts_files)




videoLocation = "vid.mp4"

video = mp.VideoFileClip(videoLocation)
duration =math.floor(video.duration)


subClipLength = 60 #seconds
subClipStart=random.randint(0,duration - subClipLength)

print(f"start: {subClipStart}, length: {subClipLength}, end: {subClipLength + subClipStart}")

subClip = video.subclip(subClipStart, subClipLength + subClipStart)

#text_clip = mp.TextClip("brrrrrrrrrrrrrrr", fontsize=70, color='white')
#text_clip = text_clip.set_position('center').set_duration(10)

#video = mp.CompositeVideoClip([clip,text_clip])
audioclips = []

#maybe instead of this just combine the audio files or spit one out from this
for i in range (20):
    audioclips.append(mp.AudioFileClip(f"tts{i}.mp3"))
    #TODO delete mp3s after appending them
audio1 = mp.concatenate_audioclips(audioclips)
new_audioclip = mp.CompositeAudioClip([audio1])
#new_audioclip.write_audiofile("audio.mp3", 44100)

#voice to text api calls

"""client = OpenAI(api_key="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")

audio_file= open("export_audio.mp3", "rb")
transcript = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)
print(transcript)"""

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
    '''text = segment["text"].upper()
    start = segment["start"]
    end = segment["end"]
    duration = end - start
    text_clip = mp.TextClip(txt=text,fontsize=40,color="white").set_start(start).set_duration(duration).set_position(("center", "center"))'''

    #subs.append(text_clip)

#final_subs = mp.concatenate(subs)
subClip = mp.CompositeVideoClip(subs)
subClip.audio = new_audioclip
subClip.write_videofile("example.mp4")

# create parser to parse a text file,break it up into readable segments and feed it to the tts

#tts('4edc1d459f309a464fcfdf11e75e55d9', 'en_female_emotional')