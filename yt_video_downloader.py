from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
import threading
from PIL import Image, ImageTk
import yt_dlp
from pytube import YouTube

#function for searching resolution
def searchResolution():
    vid_link = url_entry.get()

    if vid_link == '':
        showerror(title="Error!", message='Provide the video link!')
    else:
        try:
            ydl_opts = {}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(vid_link, download=False)

            res = []
            for f in info['formats']:
                if f.get("acodec") != "none" and f.get("vcodec") != "none":
                    if f.get("resolution"):
                        res.append(f["resolution"])


            res = list(sorted(set(res)))
            video_res['values'] = res

            showinfo(title='search is complete', message='Check the Combobox for the available video resolutions')

        except Exception as e:
            showerror("Error", f"An error occurred:\n{e}")

#function for searching resolution as a thread
def searchThread():
    t1 = threading.Thread(target=searchResolution)
    t1.start()

#function for download the video
def download_video():
    try:
        vid_link = url_entry.get()
        res = video_res.get()

        if res == '' and vid_link == '':
            showerror(title='Error', message='Enter both the video URL and resolution')
        elif res == '':
            showerror(title='Error!', message='select the resolution')
        elif res == 'None':
            showerror(title='Error', message='None is an invalid video resolution!!\n'
                    'Please select a valid video resolution')
        else:
            try:

                height_val = res.replace("p", "")
                ffmpeg_path = r"YOUR_FFMEG_PATH"
                # yt-dlp download options
                ydl_opts = {
                    "ffmpeg_location": ffmpeg_path,   # REQUIRED 
                    "format": f"bestvideo[resolution={res}]+bestaudio/best",
                    "progress_hooks": [progress_hook],
                    "outtmpl": "%(title)s.%(ext)s"
                }


                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([vid_link])

                showinfo(title='Download completed!', message='Video has been downloaded successfully.')
                progress_label.config(text='')
                progress_bar['value'] = 0

            except Exception as e:
                showerror("Error", f"An error occurred:\n{e}")
                progress_label.config(text='')
                progress_bar['value'] = 0

    except Exception as e:
        showerror("Error", f"An error occurred:\n{e}")

# progress handler
def progress_hook(d):
    print(d)
    if d['status'] == 'downloading':

        downloaded = d.get("downloaded_bytes", 0)
        total = d.get("total_bytes", 1)

        percent = (downloaded / total) * 100

        progress_label.config(text=f"{percent:.1f}%")
        progress_bar['value'] = percent

        frame.update_idletasks()


# the function to run the download_video function as a thread   
def downloadThread():
    t2 = threading.Thread(target=download_video)
    t2.start()



#create the pop-up Gui window using the tkinter
frame = Tk()
frame.title('Youtube Video Downloader')
frame.geometry('500x460+430+180')
frame.resizable(height=FALSE, width=FALSE)


canvas = Canvas(frame, width=600, height=500)
canvas.pack()

# loading the logo
logo = PhotoImage(file='YOUR_IMG_PATH')#paste your image path here
# creates dimensions of the logo
logo = logo.subsample(10, 10)
# adding the logo to the canvas
canvas.create_image(250, 80, image=logo)

'''Styles for widgets'''
#style for the label
label_style = ttk.Style()
label_style.configure('TLabel', foreground='#000000', font=('arial', 15))

#style for the entry
entry_style = ttk.Style()
entry_style.configure('TEntry', font=('Dotum', 15))

#style for button
btn_style = ttk.Style()
btn_style.configure('TButton', foreground="#7F0D0D", font='DotumChe')

#creting a label
url_label = ttk.Label(frame, text='Enter the video link: ', style='TLabel')

#creting a input box
url_entry = ttk.Entry(frame, width=80)

#adding the label to the canvas
canvas.create_window(114, 200, window=url_label)

#adding the input box
canvas.create_window(250, 230, window=url_entry)

#resolution section
res_label = ttk.Label(frame, text='Resolution')
canvas.create_window(50, 260, window=res_label)

video_res = ttk.Combobox(frame, width=12)
canvas.create_window(60, 280, window=video_res)

#search resolution button
search_res = ttk.Button(frame, text='Search', command=searchThread)
canvas.create_window(85, 315, window=search_res)

#create an empty label to indicating the progress
progress_label = Label(frame, text='')
canvas.create_window(240, 360, window=progress_label)

#progress bar
progress_bar = ttk.Progressbar(frame, orient=HORIZONTAL, length=450, mode='determinate')
canvas.create_window(250, 380, window=progress_bar)

#download button
download_btn = ttk.Button(frame, text='download', style='TButton', command=downloadThread)
canvas.create_window(240, 410, window=download_btn)

#run the window
frame.mainloop()
