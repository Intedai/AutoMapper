import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageTk
from os import path, remove
import random
from typing import Callable
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, AudioFileClip, concatenate_audioclips
from globals import ASSETS_PATH, MUSIC_PATH, VIDEO_PATH, WATERMARK_PATH, BG_VIDEO_PATH, IMAGE_PATH, countries
from dictionaries import generate_dictionary
from map_generation import make_text_map_colored
from filters import blur

# Amount of columns for the countries, their input and their color selectors
COLUMN_COUNT = 3

class AutoMapper():

    def __init__(self) -> None:

        self.root = tk.Tk()
        self.root.title("AutoMapper")
        
        # Set icon for the app
        self.icon = tk.PhotoImage(file=path.join(ASSETS_PATH,IMAGE_PATH,"icon.png"))
        self.root.wm_iconphoto(False, self.icon)

        self.top_frame = tk.Frame(self.root)
        self.top_frame.grid(row=0, column=0, columnspan=2, pady=10)


        # Create the top text input field for the video title
        self.top_label = tk.Label(self.top_frame, text="Video Title:")
        self.top_label.pack(side=tk.LEFT, padx=5)

        self.top_input = tk.Entry(self.top_frame, width=90)
        self.top_input.pack(side=tk.LEFT, padx=5)

        self.insert_color_button = tk.Button(self.top_frame, text="Insert Color", command= lambda: self.insert_color(self.top_input))
        self.insert_color_button.pack(side=tk.LEFT, padx=5)

        # Create the file selection frame for choosing bg video, music and credits
        self.file_frame = tk.Frame(self.root)
        self.file_frame.grid(row=1, column=0, columnspan=2, pady=10)


        # Background video file selection
        self.bg_vid_label = tk.Label(self.file_frame, text="Background Video:")
        self.bg_vid_label.pack(side=tk.LEFT, padx=5)

        # Disabled input to show path
        self.bg_vid_input = tk.Entry(self.file_frame, width=30, state=tk.DISABLED)
        self.bg_vid_input.pack(side=tk.LEFT, padx=5)

        # Add a button to open file dialog
        self.create_button(self.file_frame,
                           text="Select File",
                           command=lambda: self.choose_file(self.bg_vid_input,path.join(ASSETS_PATH,BG_VIDEO_PATH))
                          )

        # Add "Blurred" label and checkbox, if on bg vid will be blurred
        self.blurred_var = tk.BooleanVar()
        self.blurred_checkbox = tk.Checkbutton(self.file_frame, text="Blurred", variable=self.blurred_var)
        self.blurred_checkbox.pack(side=tk.LEFT, padx=5)

        # Watermark (Image overlay)
        self.watermark_label = tk.Label(self.file_frame, text="Watermark:")
        self.watermark_label.pack(side=tk.LEFT, padx=5)

        # Disabled input to show path
        self.watermark_input = tk.Entry(self.file_frame, width=30, state=tk.DISABLED)
        self.watermark_input.pack(side=tk.LEFT, padx=5)
        
        self.create_button(self.file_frame,
                           text="Select File",
                           command=lambda: self.choose_file(self.watermark_input,path.join(ASSETS_PATH,WATERMARK_PATH))
                          )

        # Music file selection
        self.music_label = tk.Label(self.file_frame, text="Music:")
        self.music_label.pack(side=tk.LEFT, padx=5)

        self.music_input = tk.Entry(self.file_frame, width=30, state=tk.DISABLED)
        self.music_input.pack(side=tk.LEFT, padx=5)

        self.create_button(self.file_frame,
                           text="Select File",
                           command=lambda: self.choose_file(self.music_input,path.join(ASSETS_PATH,MUSIC_PATH))
                          )
        

        # A frame for the country color selectors
        self.countries_frame = tk.Frame(self.root)
        self.countries_frame.grid(row=2, column=0, padx=10, pady=10)

        # Store buttons and frames of the country color selectors frame
        self.color_buttons = []
        self.input_entries = []

        # Store generated map image
        self.map_image = None

        for index, country in enumerate(countries):
            row = index // COLUMN_COUNT  # Calculate row
            column = (index % 3) * COLUMN_COUNT  # Calculate column index

            label = tk.Label(self.countries_frame, text=country)
            label.grid(row=row, column=column, sticky="w", padx=5, pady=2)

            color_button = tk.Button(self.countries_frame, text="Select Color", bg="#FFFFFF", command=lambda idx=index: self.choose_color(idx))
            color_button.grid(row=row, column=column+1, padx=5, pady=2)
            self.color_buttons.append(color_button)

            entry = tk.Entry(self.countries_frame)
            entry.grid(row=row, column=column+2, padx=5, pady=2)
            
            self.input_entries.append(entry)

        # Preview of the map
        self.preview_label = tk.Label(self.root, text="Image Preview")
        self.preview_label.grid(row=2, column=1, padx=10, pady=10, sticky="n")

        # Create a frame for the buttons to position them together
        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=3, column=0, pady=10, columnspan=2)

        self.create_button(self.button_frame,"Clear Data", self.clear_data)
        self.create_button(self.button_frame,"Random Colors", self.random_colors)
        self.create_button(self.button_frame,"Save Image As...", self.save_image)
        self.create_button(self.button_frame,"Upload Image", self.upload_image)
        self.create_button(self.button_frame,"Generate Image", self.generate_image)
        self.create_button(self.button_frame,"Export Video As...", self.export_video)

        # Show preview image 
        self.update_preview()
        tk.mainloop()

    def insert_color(self, input: str) -> None:
        """
        Insert color code into top text
        :param input: the input that the color will be inserted into
        """
        color = colorchooser.askcolor(title="Choose color to insert")
        if color[1]:  # If a color is selected
            color_code = f"&({color[1]})"
            input.insert(tk.END, color_code)

    
    def choose_file(self,file_input: tk.Entry, initialdir: str) -> None:
        """
        Choose a file from computer files
        :param file_input: input to store the path
        :initialdir: initial directory that opens when choosing file
        """
        file_path = filedialog.askopenfilename(initialdir=initialdir)
        
        # If a file is selected
        if file_path:
            file_input.config(state=tk.NORMAL) # Enable to update text
            file_input.delete(0, tk.END) # Clear text
            file_input.insert(tk.END, file_path) # Insert file path
            file_input.config(state=tk.DISABLED) # Disable entry again so path wont be manually edited

    def create_button(self, frame: tk.Frame, text: str, command: Callable) -> None:
        """
        Creates a button with the desired position and padding
        :param frame: frame that the button will be in
        :param text: text on the button
        :param command: command that will be called when the button is clicked 
        """
        random_button = tk.Button(frame, text=text, command=command)
        random_button.pack(side=tk.LEFT, padx=5)

    def choose_color(self,index: int) -> None:
        """
        Choose a color for a country
        :param index: index in countries list
        """
        color = colorchooser.askcolor(title=f"Choose color for {countries[index]}")
        if color[1]:  # If a color is selected
            self.color_buttons[index].config(bg=color[1]) 
    
    def clear_data(self) -> None:
        """
        Function to clear inputs and colors, gives a warning
        """
        warning = messagebox.askyesno("Warning", "Are you sure you want to clear all the data (Including Colors)?")

        if warning:
            for button in self.color_buttons:
                button.config(bg="#FFFFFF")
            for entry in self.input_entries:
                entry.delete(0, tk.END)

    def random_colors(self) -> None:
        """
        Generate random colors and assign them directly to buttons
        """
        for button in self.color_buttons:
            hex_color = '#%06x' % random.randint(0, 0xFFFFFF)
            button.config(bg=hex_color)

    def generate_image(self) -> None:
        """
        Generates an image and puts in the preview
        """
        title = self.top_input.get()

        # Get text from the country entries
        entries_values = [entry.get() for entry in self.input_entries]

        # Unpack the list to pass to generate_dictionary for years
        years_dict = generate_dictionary(*entries_values)

        # Get color hex values from the color buttons
        color_values = [
            tuple(int(self.color_buttons[i].cget('bg').lstrip('#')[j:j+2], 16) for j in (0, 2, 4))
            for i in range(len(countries))
        ]

        # Use generate_dictionary to create a color dictionary
        color_dictionary = generate_dictionary(*color_values)

        # Generate map image
        self.map_image = make_text_map_colored(title, years_dict, color_dictionary)

        # Make copy so resize wont effect the generated map
        image = self.map_image.copy()

        # Resize image to fit in 383x383 with the desired aspect ratio
        image.thumbnail((383, 383))

        img = ImageTk.PhotoImage(image)
        self.preview_label.config(image=img)
        self.preview_label.image = img # Prevent garbage collection

    def export_video(self) -> None:
        """
        Exports the generated video
        """
        is_bg_blurred = self.blurred_var.get()

        if self.map_image is None:
            tk.messagebox.showerror("Error", "No map image available. Please generate an image first.")
            return
        
        watermark_path = self.watermark_input.get()
        if not watermark_path:
            tk.messagebox.showerror("Error", "No watermark selected.")
            return

        try:
            watermark_image = Image.open(watermark_path).convert("RGBA")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to load credit image: {e}")
            return
        
        # Paste the watermark on the map image and make a composed image
        composed_image = self.map_image.copy()
        watermark_image.thumbnail(composed_image.size, Image.LANCZOS)
        composed_image.paste(watermark_image, (0, 0), watermark_image)
        composed_image_path = "composed_image.png"
        composed_image.save(composed_image_path)

        background_video_path = self.bg_vid_input.get()
        if not background_video_path:
            tk.messagebox.showerror("Error", "No background video selected.")
            remove(composed_image_path)
            return
        
        # Music file doesn't have to be selected, if not selected its the sound of the bg vid
        music_file_path = self.music_input.get()

        try:
            background_clip = VideoFileClip(background_video_path)
            if is_bg_blurred:
                background_clip = background_clip.fl_image(blur)
            image_clip = (
                ImageClip(composed_image_path)
                .set_duration(background_clip.duration)
                .set_position("center")
                .resize(background_clip.size)
            )

            video = CompositeVideoClip([background_clip, image_clip])

            if music_file_path:
                audio_clip = AudioFileClip(music_file_path)
                    
                # Adjust the audio to match the video duration
                if audio_clip.duration > background_clip.duration:
                    audio_clip = audio_clip.subclip(0, background_clip.duration)
                else:
                    # Create a loop when music is shorter
                    audio_clip = concatenate_audioclips([audio_clip] * int(background_clip.duration // audio_clip.duration + 1))
                    audio_clip = audio_clip.subclip(0, background_clip.duration) # Trim to match exactly

                video = video.set_audio(audio_clip)

            # Ask for path to save the video
            output_video_path = filedialog.asksaveasfilename(
                defaultextension=".mp4",
                filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")],
                title="Save Video As",
                initialdir=path.join(ASSETS_PATH,VIDEO_PATH)
            )

            if output_video_path:
                video.write_videofile(output_video_path, codec="libx264", audio_codec="aac", threads=8,fps=background_clip.fps)
                tk.messagebox.showinfo("Success", "Video generated successfully!")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to generate video: {e}")
        finally:
            # Remove composed image generated in the start
            remove(composed_image_path)


    def save_image(self) -> None:
        """
        Save generated image to files
        """
        if self.map_image is not None:
            # Open a "Save As" dialog to save the image
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                title="Save Image As",
                initialdir=IMAGE_PATH
            )
            
            # Save the image if a file path was selected
            if file_path:
                self.map_image.save(file_path)
        else:
            # Show an error message if map_image is None
            tk.messagebox.showerror("Error", "No image to save. Please generate an image first.")

    def upload_image(self) -> None:
        """
        Upload image from files directly into AutoMapper
        """

        # Open a file dialog to select an image file
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All Files", "*.*")],
            initialdir=ASSETS_PATH
        )

        # Check if a file was selected
        if file_path:
            try:
                # Load the image using PIL
                self.map_image = Image.open(file_path)

                # Update the image preview with the uploaded image
                image = self.map_image.copy()
                image.thumbnail((383, 383))  # Resize image maintaining aspect ratio to fit within 383x383
                img = ImageTk.PhotoImage(image)
                self.preview_label.config(image=img)
                self.preview_label.image = img  # Keep a reference to the image to prevent garbage collection

            except Exception as e:
                # Show an error message if the image cannot be opened
                tk.messagebox.showerror("Error", f"Failed to load image: {e}")

    def update_preview(self) -> None:
        """
        Update the preview initially with the preview image
        """
        image = Image.open(path.join(ASSETS_PATH,IMAGE_PATH,"preview.png"))
        image.thumbnail((383, 383)) # Resize image to fit in 383x383 with the desired aspect ratio
        img = ImageTk.PhotoImage(image)
        self.preview_label.config(image=img)
        self.preview_label.image = img # Prevent garbage collection

if __name__ == '__main__':
    try:
        AutoMapper()
    except Exception as e:
        print(e) #prints to the console
        input("\n\nPress enter to quit ...")
