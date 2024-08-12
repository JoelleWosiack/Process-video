import os
import whisper
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from googletrans import Translator
from gtts import gTTS

# Function to extract audio from a video file
def extract_audio(video_path, audio_path):
    print("Extracting audio from video...")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    video.close()

# Function to transcribe audio to text
def transcribe_audio(audio_path, language='pt'):
    print("Transcribing audio...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language=language)
    return result["text"]

# Function to translate text from one language to another
def translate_text(text, src='pt', dest='en'):
    print("Translating text...")
    translator = Translator()
    # Split the text into smaller chunks to avoid length limits
    chunks = [text[i:i+5000] for i in range(0, len(text), 5000)]
    translated_chunks = []
    for chunk in chunks:
        result = translator.translate(chunk, src=src, dest=dest)
        translated_chunks.append(result.text)
    return ' '.join(translated_chunks)

# Function to convert text to speech
def text_to_speech(text, output_path):
    print("Generating speech...")
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(output_path)

# Function to combine video with a new audio track
def combine_video_audio(video_path, audio_path, output_path):
    print("Combining new audio with video...")
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    
    if audio.duration < video.duration:
        audio = audio.audio_loop(duration=video.duration)
    else:
        audio = audio.subclip(0, video.duration)
    
    final_audio = CompositeAudioClip([audio])
    final_video = video.set_audio(final_audio)
    final_video.write_videofile(output_path, audio_codec='aac')

# Function to create a sample of a given duration from a video
def create_video_sample(input_video, output_video, duration=300):  # 300 seconds = 5 minutes
    print(f"Creating a {duration}-second sample of the video...")
    with VideoFileClip(input_video) as video:
        sample = video.subclip(0, duration)
        sample.write_videofile(output_video)

# Main function that join all together
def main():
    original_video = ""
    audio_path = "extracted_audio.wav"
    transcription_file = "transcription.txt"
    translation_file = "translation.txt"
    sample_video = "sample_video.mp4"
    translated_audio = "translated_audio.mp3"
    output_video = "video_with_english_voiceover.mp4"

    # Step 1: Extract audio and transcribe
    extract_audio(original_video, audio_path)
    transcription = transcribe_audio(audio_path)
    
    with open(transcription_file, 'w', encoding='utf-8') as f:
        f.write(transcription)
    print(f"Transcription saved to {transcription_file}")

    # Step 2: Translate transcription
    english_text = translate_text(transcription)
    
    with open(translation_file, 'w', encoding='utf-8') as f:
        f.write(english_text)
    print(f"Translation saved to {translation_file}")

    # Step 3: Create sample of the video
    create_video_sample(original_video, sample_video)

    # Step 4: Generate English voice-over and combine with sample video
    text_to_speech(english_text, translated_audio)
    combine_video_audio(sample_video, translated_audio, output_video)

    # Clean up temporary files
    print("Cleaning up temporary files...")
    for file in [audio_path, translated_audio]:
        if os.path.exists(file):
            os.remove(file)

    print(f"Process completed. Final video saved as {output_video}")


# Start main function
if __name__ == "__main__":
    main()
