from customtkinter import filedialog
from pathlib import Path
from PIL import Image
import customtkinter
import ffmpeg
import sys
import os

# Function to load images on exe file (More compatibility with the auto-py-to-exe)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Function to open file selector dialog
def selectFile(app, row):
    file_selector = filedialog.askopenfilename()
    if row == 0:
        app.video_entry.delete(0, customtkinter.END)
        app.video_entry.insert(0, file_selector)
        app.selected_file = file_selector
    elif row == 1:
        app.thumb_entry.delete(0, customtkinter.END)
        app.thumb_entry.insert(0, file_selector)
    app.label.configure(text="Press the button to start", text_color="white")


# Convert selected video to PSP format
def convertVideo(app):
    if app.video_entry.get() == "":
        app.label.configure(text="Select a file before convert!", text_color="red")
    else:
        try:
            input_video = app.selected_file
            output_video = os.path.splitext(input_video)[0] + "_psp.mp4"
            
            # Thumbnail processing
            if app.thumb_entry.get() != "":
                thumb_file = app.thumb_entry.get()
                thumb_output = os.path.splitext(output_video)[0] + ".THM"

                # Open the image, resize it, and save as JPEG with .THM extension
                image = Image.open(thumb_file)
                image = image.resize((160, 120))
                image.save(thumb_output, format="JPEG")

            ffmpeg_executable = resource_path("ffmpeg/ffmpeg.exe")
            selected_quality = app.combo_box.get()      

            if selected_quality == "240p":
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
                app.label.configure(text="Conversion done!", text_color="green")
                
            elif selected_quality == "480p":
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
                app.label.configure(text="Conversion done!", text_color="green")

            else:
                app.label.configure(text="Selected video quality unsupported!", text_color="red")

        except Exception as e:
            app.label.configure(text=f"ERROR: {e}.", text_color="red")


# CustomTkinter GUI
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("450x500")
        self.title("PSP Video Converter")
        self.iconbitmap(resource_path("assets/icon.ico"))

        logo = customtkinter.CTkImage(light_image=Image.open(resource_path("assets/icon.png")), size=(150, 150))
        self.label = customtkinter.CTkLabel(master=self, text="", image=logo)
        self.label.grid(row=0, column=0,columnspan=2, sticky="n")

        self.video_entry = customtkinter.CTkEntry(master=self, placeholder_text="Video file", width=300)
        self.video_entry.grid(row=1, column=0, padx=30, pady=15)

        self.thumb_entry = customtkinter.CTkEntry(master=self, placeholder_text="Thumbnail file (optional)", width=300)
        self.thumb_entry.grid(row=2, column=0, padx=30, pady=15)

        self.quality_label = customtkinter.CTkLabel(master=self, text="Video quality:", font=("Arial", 18))
        self.quality_label.grid(row=3, column=0, padx=(50, 0), pady=15, sticky="w")

        self.combo_box = customtkinter.CTkComboBox(master=self, values=["480p", "240p"])
        self.combo_box.grid(row=3, column=0, padx=(0, 50), pady=15, sticky="e")

        image_button = customtkinter.CTkImage(Image.open(resource_path("assets/folder.png")))

        for c in range(0, 2):

            self.file_button = customtkinter.CTkButton(master=self, text="", width=50, image=image_button, fg_color="#2E4057", command=lambda row=c: selectFile(self, row))
            self.file_button.grid(row=c+1, column=1, pady=5)

        self.label = customtkinter.CTkLabel(master=self, text="", font=("Arial", 18, "bold"))
        self.label.grid(row=4, column=0, columnspan=2, pady=5, sticky="n")

        self.start_button = customtkinter.CTkButton(master=self, text="Convert", font=("Arial", 30), width=200, height=100, fg_color="#2E4057", command=lambda: convertVideo(self))
        self.start_button.grid(row=4, column=0, columnspan=2, pady=50, sticky="n")

        self.selected_file = ""
        

customtkinter.set_appearance_mode("dark")
app = App()
app.mainloop()
