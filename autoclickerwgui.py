import tkinter as tk
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key as KBButton, Listener
import pynput
from tkinter import messagebox
import time
import threading

timeInBetweenClicks = 0.00001
click = Button.left
startAndStopKey = KBButton.f6
listener_stop:bool = False
root:object = tk.Tk()
guiApp = None

class MouseClicker(threading.Thread):
    def __init__(self, timeInBetweenClicks, click):
        super(MouseClicker, self).__init__()
        self.delay = timeInBetweenClicks
        self.button = click
        self.running = False
        self.program_running = True
    def start_autoclicker(self):
        self.running = True
    def stop_autoclicker(self):
        self.running = False
    def exit(self): 
        self.stop_autoclicker() 
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(self.delay)
            time.sleep(0.1)

mouse = MouseController()
clickingThread = MouseClicker(timeInBetweenClicks, click)
clickingThread.start()

class Keyboard:
    @staticmethod
    def Pressed(key) -> bool:
        global guiApp
        if listener_stop: print("Keyboard Events are stoped!"); return False
        else:
            if guiApp: 
                if key == startAndStopKey:
                    if clickingThread.running:
                        clickingThread.stop_autoclicker()
                        guiApp.update_title()
                        print('clicking stopped')
                    else:
                        clickingThread.start_autoclicker()
                        guiApp.update_title()
                        print('clicking started')

    @staticmethod
    def Listener() -> None:
        k_listen = pynput.keyboard.Listener(on_press=Keyboard.Pressed,
                                            )
        k_listen.start()

class MainApp:
    def __init__(self, master):
        self.master = master

        self.master.wm_title("Ben's Auto Clicker")
        self.master.wm_geometry('400x250')
        self.master.attributes('-topmost', True)

        self.Screen(self.master)
        self.InputEvents()

    def Screen(self, root) -> None:
        self.frm_main = tk.Frame(root)
        self.frm_main.pack(expand=True, fill="x", side="top")

        self.title = tk.Label(self.frm_main, text="Ben's Auto Clicker", font=("Roboto", 18, "bold"), fg="tomato")
        self.title.pack(expand=False, fill="x")
        self.instructionLabel = tk.Label(self.frm_main, text="Press F6 to turn the autoclicker on and off.", font=12)
        self.instructionLabel.pack()
        self.autoClickingState = tk.Label(self.frm_main, text="Currently not clicking.", font=9)
        self.autoClickingState.pack()

        

    def InputEvents(self) -> None:
        Keyboard.Listener()

    def SafeQuit(self, master:object = root) -> None:
        global listener_stop
        if messagebox.askokcancel("Ben's Autoclicker Quit", "Are you sure you want to quit the autoclicker?"):
            if listener_stop == False:
                listener_stop = True
                print("Events Listening are stoped!")
            master.destroy()
            clickingThread.exit()
    def update_title(self):
        if clickingThread.running:
            self.autoClickingState.config(text="Currently clicking.")
        else:
            self.autoClickingState.config(text="Currently not clicking.")



if __name__ == "__main__":
    guiApp = MainApp(root)
    root.protocol("WM_DELETE_WINDOW", guiApp.SafeQuit)
    root.mainloop()
