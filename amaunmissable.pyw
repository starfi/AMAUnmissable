import praw
import webbrowser
import time
from Tkinter import *
import threading

REFRESH_RATE = 30
LIMIT = 5
watch_words = []
run = False
SUBREDDIT = "iama"

def go():
    global watch_words, REFRESH_RATE, run
    watch_words = words_entry.get("0.0", END).split("\n")
    REFRESH_RATE = int(refresh_entry.get())
    run = True
    root.destroy()

 
def validate(action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
    if text in '0123456789.-+':
        try:
            if value_if_allowed:
                float(value_if_allowed)
                return True
            else:
                return True
        except ValueError:
            return False
    else:
        return False

def words_entry_clicked(event):
    if words_entry.get("0.0", END) == "Enter list of phrases to look out for, seperated by new lines...\n":
        words_entry.delete("0.0", END)
    
root = Tk()
root.geometry("600x500")
root.title("AMA AutoOpen")
Label(root, text="Key Words").grid(row=0, column=0, pady=8, padx=8, sticky=(N,S,E,W))
Label(root, text="Refresh Interval").grid(row=0, column=1,pady=8, padx=8,sticky=(N,S,E,W))
Label(root, text="Subreddit").grid(row=2, column=1, pady=8, padx=8, sticky=(N,E,W))

ltext = """
Enter words (like the name of a person doing an AMA) in the Key Words section. The program will
automatically detect when the AMA is posted, and will open the link for you in your web browser."""

Label(root, text=ltext).grid(row=6, column=0, columnspan=2,pady=0, padx=8, sticky=(N,E,W))

words_entry = Text(root, bd=3, font=("Helvetica",9))
words_entry.bind("<Button-1>", words_entry_clicked)
words_entry.insert("0.0", "Enter list of phrases to look out for, seperated by new lines...")
words_entry.grid(row=1, column=0, rowspan=5, padx=8, pady=0, sticky=(N,S,E,W))

vcmd = (root.register(validate), 
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
refresh_entry = Entry(root, bd=3,
                      validate="key", validatecommand=vcmd)

refresh_entry.grid(row=1, column=1, padx=8, pady=0, sticky=(N,S,E,W))

sub_entry = Entry(root, bd=3)

sub_entry.grid(row=3, column=1, padx=8, pady=0, sticky=(N))
sub_entry.insert(0, "iama")

go_button = Button(root, command=go, text="            Go!            ")
go_button.grid(row = 5, column=1, sticky=(S,E), padx=8, pady=0)


root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=0, minsize=100)
root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=0)
root.rowconfigure(2, weight=0)
root.rowconfigure(3, weight=0)
root.rowconfigure(4, weight=0)
root.rowconfigure(5, weight=1)


refresh_entry.insert(0, "3")
refresh_entry.insert(1, "0")

root.mainloop()

r = praw.Reddit(user_agent="AMA Checker by /u/JWStarfish")
def run():
    global watch_words
    watch_words = [w for w in watch_words if not w == "\n" and not w == ""]
    submissions = r.get_subreddit("iama").get_new(limit=LIMIT)
    
    keepalive = True
    for i in range(LIMIT):
        sub = next(submissions)
        title = sub.title.lower()
        if not "request" in title:
            for w in watch_words:
                if w.lower() in title and w != "":
                    webbrowser.open_new_tab(sub.url)
                    watch_words.remove(w)
                    
                    if watch_words == []:
                        keepalive = False

    if keepalive:
        threading.Timer(30, run).start()
    
if run:
    run()

