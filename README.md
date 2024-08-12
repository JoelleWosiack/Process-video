# Video processing script

### Outputs:
- Text file with the transcription of the video's audio
- Text file with the translation of the video's audio
- Video with new voice-over

### Code execution:
- Save it in the same location as the video to be processed
- Enter the **name of the video in line 63** of the script
- In the terminal, install: `pip install moviepy whisper googletrans==3.1.0a0 gTTS torch`
- In the terminal: `python process_video.py`

### Notes:
At this point, the file is fixed and cannot be parameterized, so if the name of the video is not written in line 63, the file will not run correctly.
In addition, it is fixed that the video is originally in Portuguese and the new voice-over is in English.
