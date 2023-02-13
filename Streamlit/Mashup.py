from pytube import YouTube
import pydub 
import urllib.request
import re
import os
import sys

import streamlit as st
import time
import os
st.title('Mashup using Python:musical_note:')
st.write('Samarjot Singh')
artist=st.text_input("Name of the artist")
n=int(st.number_input("No. of songs",step=1))
y=int(st.number_input("Duration(in seconds)",step=1))
output_name=st.text_input("Output file name")

flag=0
if st.button('Submit'):
    delete_after_use = True                              
    if len(sys.argv) == 5:
        x = artist
        x = x.replace(' ','') + "songs"
    else:
        sys.exit('Insufficient arguments passed in CLI. Exiting!!!')

    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(x))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                                                      
    for i in range(n):
        yt = YouTube("https://www.youtube.com/watch?v=" + video_ids[i]) 
        print("File "+str(i+1)+" downloading...")
        mp4files = yt.streams.filter(only_audio=True).first().download(filename='audio_'+str(i)+'.mp3')

    print("All files are downloaded.\nNow creating the mashup...")

    if os.path.isfile(str(os.getcwd())+"\\audio_0.mp3"):
        pydub.AudioSegment.converter = 'C:\\ffmpeg\\bin\\ffmpeg.exe'
        try:
            fin_sound = pydub.AudioSegment.from_file(
                str(os.getcwd())+"\\audio_0.mp3", format='mp3')[20000:(y*1000+20000)]
        except:
            fin_sound = pydub.AudioSegment.from_file(
                str(os.getcwd())+"\\audio_0.mp3", format='mp4')[20000:(y*1000+20000)]
        for i in range(1, n):
            aud_file = str(os.getcwd())+"\\audio_"+str(i)+".mp3"
            fin_sound = fin_sound.append(pydub.AudioSegment.from_file(aud_file)[20000:(y*1000+20000)], crossfade=1000)
  
    try:
        fin_sound.export(output_name, format="mp3")
        print("Mashup created successfuly as " + str(output_name))
    except:
        sys.exit("Error while saving the file. Try a differrent file name.")
        
    if delete_after_use:
        for i in range(n):
            os.remove("audio_"+str(i)+".mp3")
    flag=1

    
    progress_text = "Please wait for your magic mashup."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1, text=progress_text)
    
    if(flag==1):
        with open(output_name, "rb") as fp:
    
            btn = st.download_button(
            label="Download Mashup mp3",
            data=fp,
            file_name=output_name,
            mime="audio/mpeg"
            )


if __name__ == '__main__':
    main()