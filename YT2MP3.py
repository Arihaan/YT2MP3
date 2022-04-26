from tkinter import *
import requests
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


PATH = os.getcwd() + "/chromedriver"
download_folder = os.getcwd() + '/Downloaded MP3s'
driver = Service(PATH)
options = Options()
options.add_argument('--window-size=1920,1080')
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
chrome_prefs = {"download.default_directory": download_folder}
options.experimental_options["prefs"] = chrome_prefs


bg_color = '#2C2B2B'
font_type = 'Lucida Grande'

all_song_links = []
all_song_names = []

# stores song link and updates display
def add_song():
    link = link_box.get()
    link_box.delete(0, END)
    console.see(END)

    # check if link is empty
    if link == '':
        console.insert(END, '> Please enter a valid YouTube url!\n')
        return

    # check if link has already been added
    if link in all_song_links:
        console.insert(END, "> This song has already been added!\n")
        return

    # getting song details from API
    response = requests.get('https://noembed.com/embed?url=' + link)
    if 'error' in response.json():
        console.insert(END, '> Please enter a valid YouTube url!\n')
    else:
        console.insert(END, f'> Added: {response.json()["title"]} by {response.json()["author_name"]}\n')
        console.see(END)
        all_song_links.append(link)
        all_song_names.append(response.json()["title"])

# downloads the stored songs
def download_songs():
    console.see(END)
    if not len(all_song_links):
        console.insert(END, "> No songs added!\n")
        return
    console.insert(END, f"> Downloading {len(all_song_links)} songs..\n")
    add.config(state='disabled')
    download.config(text="Downloading..", state='disabled')

    browser = webdriver.Chrome(service=driver, options=options)

    # Download each song one by one
    for link in all_song_links:

        # Create downloads folder if it does not already exist
        if not os.path.exists(download_folder):
            console.insert(END, '> Making folder..\n')
            os.mkdir('Downloaded MP3s')
            console.insert(END, '> Folder made!\n')

        # Return download folder size
        def get_folder_size():
            return len(next(os.walk(download_folder))[2])

        # Save initial folder size for later
        initial_size = get_folder_size()

        # Configurations for where mp3 will be saved
        params = {'behavior': 'allow', 'downloadPath': download_folder}
        browser.execute_cdp_cmd('Page.setDownloadBehavior', params)

        # Open an empty new tab
        browser.get('chrome://newtab')
        browser.execute_script(f"window.open('','_blank');")

        # Opens the download url
        tab2 = browser.window_handles[1]
        browser.switch_to.window(tab2)
        browser.get('https://onlinevideoconverter.pro/en20/youtube-converter-mp3')

        # Enter link in search bar
        search_bar = browser.find_element(By.ID, 'texturl')
        search_bar.send_keys(link)
        browser.find_element(By.XPATH, '//*[@id="convert1"]/i').click()

        # Wait while download button is loaded
        while True:
            try:
                download_button = browser.find_element(By.ID, 'download-720-MP4')
                break
            except NoSuchElementException:
                time.sleep(1)

        # Click download button and close pop-up tab
        download_button.click()
        tab3 = browser.window_handles[2]
        browser.switch_to.window(tab3)
        browser.close()
        browser.switch_to.window(tab2)


        # Checks if file has started downloading
        while True:
            if get_folder_size() > initial_size:
                break
            time.sleep(1)

        # Close the second tab
        tab1 = browser.window_handles[0]
        browser.close()
        browser.switch_to.window(tab1)

        # Checks if file is downloaded yet or not
        folder_path = f"{download_folder}"
        os.chdir(folder_path)

        def latest_download_file():
            files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
            newest = files[-1]

            return newest

        file_ends = "crdownload"
        while "crdownload" == file_ends:
            time.sleep(1)
            newest_file = latest_download_file()
            if "crdownload" in newest_file:
                file_ends = "crdownload"
            else:
                file_ends = "none"
                os.chdir('..')

        console.insert(END, f"> Downloaded {all_song_names[all_song_links.index(link)]}\n")

    console.see(END)
    console.insert(END, '> All downloads successfully completed!\n')
    browser.quit()
    add.config(state='normal')
    download.config(text='Download All', state='normal')
    all_song_links.clear()
    all_song_names.clear()

# Tkinter GUI:
root = Tk()
root.title("YT2MP3 - Download Multiple MP3s from YouTube at once")
root.geometry('800x625')
root['bg'] = bg_color

title_label = Label(root, text="YouTube to MP3", font=(font_type, 40), bg='#232222', fg="white", width='50',
                    height='2').pack(pady=(0, 20))

# textbox where youtube link is entered
link_box_label = Label(root, text="Enter YT URL:", font=(font_type, 15), bg=bg_color, fg="white").pack(pady=(0, 5))
link_box = Entry(root, width='60')
link_box.pack()

# add button
add = Button(root, text="Add", height='1', font=(font_type, 15), highlightbackground=bg_color, fg='white',
                command=lambda: add_song())
add.pack(pady=5)

# download button
download = Button(root, text="Download All", height='1', font=(font_type, 20), highlightbackground=bg_color,
                         fg='white', command=lambda: download_songs())
download.pack(pady=5)

# console
console_label = Label(root, text="Console:", font=(font_type, 15), bg=bg_color, fg='white').pack(pady=(50, 5))
console = Text(root, font=('Courier New', 15), width='60', height='15', fg='yellow')
console.bind("<Key>", lambda e: "break")
console.pack()

root.mainloop()



