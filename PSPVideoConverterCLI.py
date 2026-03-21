from pathlib import Path
from PIL import Image
import ffmpeg
import sys
import os

def convertVideo():
    input_video = input("Video path: ")
    input_thumb = input("Thumbnail path (optional): ")
    selected_quality = input("Video quality ([1] 240p/[2] 480p): ")
    output_video = os.path.splitext(input_video)[0] + "_psp.mp4"

    # THumbnail processing
    if input_thumb != "":
        thumb_output = os.path.splitext(output_video)[0] + ".THM"

        # Open the image, resize it and save as JPEG with .THM extension
        image = Image.open(input_thumb)
        image = image.resize((160, 120))
        image.save(thumb_output, format="JPEG")

    ffmpeg_executable = "ffmpeg"
    try:
        if selected_quality == "1":
            (
                ffmpeg
                .input(input_video)
                .filter("fps", fps=29.97, round="up")
                .filter("scale", 320, 240)
                .output(
                    output_video,
                    vcodec="mpeg4",
                    video_bitrate="672k",
                    acodec="aac",
                    ar="24000",
                    audio_bitrate="128k",
                    movflags="faststart",
                    strict="experimental",
                    map="0:a"
                )
                .run(cmd=ffmpeg_executable)
            )
            print("\033[32mConversion done!\033[m")

        elif selected_quality == "2":
            (
                ffmpeg
                .input(input_video)
                .filter("fps", fps=29.97, round="up")
                .filter("scale", 480, 272)
                .output(
                    output_video,
                    vcodec="libx264",
                    video_bitrate="672k",
                    acodec="aac",
                    ar="24000",
                    audio_bitrate="128k",
                    movflags="faststart",
                    pix_fmt="yuv420p",
                    profile="baseline",
                    level="1.3",
                    strict="experimental",
                    map="0:a"
                )
                .run(cmd=ffmpeg_executable)
            )
            print("\033[32mConversion done!\033[m")

    except Exception as e:
        print(f"\033[31mError: {e}\033[m")

convertVideo()
