import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import moviepy.editor as mp


def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
    return file_path


def clip_video(file_path, duration):
    video = mp.VideoFileClip(file_path)
    n_clips = int(video.duration / duration)
    progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
    progress.grid(column=0, row=3, padx=10, pady=10, sticky="W")
    for i in range(n_clips):
        start = i * duration
        end = (i + 1) * duration
        clip = video.subclip(start, end)
        clip.write_videofile(f"video_clips/clip_{i}.mp4", verbose=False, logger=None)
        progress["value"] = (i + 1) / n_clips * 100
        progress.update()
    if video.duration % duration != 0:
        start = n_clips * duration
        end = video.duration
        clip = video.subclip(start, end)
        clip.write_videofile(f"video_clips/clip_{n_clips}.mp4", verbose=False, logger=None)
        progress["value"] = 100
        progress.update()
    progress.destroy()


root = tk.Tk()
root.title("VideoCut")

file_path = tk.StringVar()
duration = tk.DoubleVar()
duration.set(30.0)

file_entry = tk.Entry(root, textvariable=file_path, state="readonly")
file_entry.grid(column=0, row=0, padx=10, pady=10, sticky="W")

duration_entry = tk.Entry(root, textvariable=duration)
duration_entry.grid(column=0, row=1, padx=10, pady=10, sticky="W")

select_button = ttk.Button(root, text="Select file", command=lambda: file_path.set(select_file()))
select_button.grid(column=0, row=2, padx=10, pady=10, sticky="W")

progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress.grid(column=0, row=3, padx=10, pady=10, sticky="W")

start_button = ttk.Button(root, text="Start", command=lambda: clip_video(file_path.get(), duration.get()))
start_button.grid(column=0, row=4, padx=10, pady=10, sticky="W")

root.mainloop()
