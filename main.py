#!/usr/bin/python3.4

import speech_recognition as sr
import sys
import threading
import time
from tkinter import *
from queue import Queue, Empty

WIDTH = 100
HEIGHT = 100
WALL = "brown"
ITEM = "gray"
ACTIVE = "purple"
LOOP_TIME = 1

stuff = {
    "hammer": (0, 1),
    "mallet": (0, 2),
    "ax": (0, 3),
    "saw": (0, 4),
    "hacksaw": (0, 5),
    "level": (1, 3),
    "screwdriver": (1, 6),
    "Phillips screwdriver": (1, 7),
    "wrench": (1, 9),
    "monkey wrench": (4, 3),
    "pipe wrench": (4, 5),
    "chisel": (4, 6),
    "scraper": (4, 8),
    "wire stripper": (5, 1),
    "hand drill": (5, 2),
    "vise": (5, 4),
    "pliers": (5, 6),
    "toolbox": (5, 7),
    "plane": (7, 1),
    "electric drill": (7, 3),
    "drill bit": (7, 4),
    "circular saw": (7, 5),
    "power saw": (7, 6),
    "pipe": (8, 1),
    "ander": (8, 3),
    "router": (8, 4),
    "wire": (8, 6),
    "nail": (8, 7),
    "washer": (9, 4),
    "nut": (9, 5),
    "wood screw": (9, 7),
    "machine screw": (9, 8),
    "bolt": (9, 9)
}

recog = sr.Recognizer()
mic = sr.Microphone()
recog.energy_threshold = 1000
running = True
queue = Queue()


class WallCanvas(Canvas):
    def __init__(self, master, **args):
        Canvas.__init__(self, master, **args)
        self.bind("<Configure>", self.onResize)
        self.width = master.winfo_reqwidth()
        self.oWidth = self.width
        self.height = master.winfo_reqheight()
        self.oHeight = self.height
        self.first = True

    def onResize(self, event):
        if(self.first):
            self.oWidth = event.width
            self.oHeight = event.height
            self.first = False
            wscale = 1
            hscale = 1
        else:
            wscale = float(event.width) / self.width
            hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, wscale, hscale)

    def getScale(self):
        return (self.width / self.oWidth, self.height / self.oHeight)


class GuiPart:

    def __init__(self, master, endCommand):
        self.master = master
        # Set up the GUI
        self.master.protocol("WM_DELETE_WINDOW", endCommand)
        self.canvas = WallCanvas(
            self.master, width=WIDTH, height=HEIGHT, background="black")
        self.initGUI(master, WIDTH, HEIGHT)
        self.initShelves(10, 10)
        self.canvas.pack(side=TOP, expand=YES, fill=BOTH)
        self.ix = 0
        self.iy = 0

    def initGUI(self, f, w, h):
        '''
        Center the Window on the display
        '''
        ws = f.winfo_screenwidth()
        hs = f.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        f.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def initShelves(self, rows, cols):
        self.shelf = [[0 for i in range(rows)] for i in range(cols)]
        for x in range(0, 10):
            for y in range(0, 10):
                id = self.createShelf(ITEM, (x, y), (10, 10))
                self.shelf[x][y] = id
        print(str(self.shelf))

    def createShelf(self, color, position, size):
        '''
        Initialize item location on shelf
        '''
        x, y = position
        w, h = size
        sx, sy = self.canvas.getScale()
        return self.canvas.create_rectangle(
            x * sx * w, y * sy * h,
            ((x + 1) * sx * w) - 1, ((y + 1) * sy * h) - 1,
            fill=color, outline=WALL, tag="all")

    def processIncoming(self):
        '''
        Process text message from voice recognizer
        '''
        while queue.qsize():
            try:
                message = queue.get(0)
                com = self.getCommand(message)
                self.action(com)
            except Empty:
                # No message to parse
                pass

    def getCommand(self, message):
        command = message.split(' ', 1)
        self.master.title(message)
        if(message in stuff):
            command = stuff[message]
        return command

    def action(self, command):
            if(len(command) == 2):
                self.canvas.itemconfig(
                    self.shelf[int(self.ix)][int(self.iy)], fill=ITEM)
                self.ix = command[0]
                self.iy = command[1]
                self.canvas.itemconfig(
                    self.shelf[int(self.ix)][int(self.iy)], fill=ACTIVE)

    def quit(self):
        '''
        Clean GUI elements and window
        '''
        print('')
        self.master.destroy()


class ThreadedClient:

    def __init__(self, master):
        self.master = master

        # Set up the GUI part
        self.gui = GuiPart(self.master, self.endApplication)

        with mic as source:
            recog.adjust_for_ambient_noise(source)
        self.background = recog.listen_in_background(mic, listener)

        # Set up the worker thread
        self._running = True
        self.thread = threading.Thread(target=self.workerThread)
        self.thread.daemon = True
        self.thread.start()
        self.loop()

    def loop(self):
        '''
        Check every LOOP_TIME ms if there is something new in the queue.
        '''
        self.gui.processIncoming()
        if not self._running:
            self.master.destroy()
            sys.exit(1)
        self.master.after(int(LOOP_TIME * 100), self.loop)

    def workerThread(self):
        '''
        Basic convolution loop
        '''
        while self._running:
            time.sleep(LOOP_TIME)

    def endApplication(self):
        '''
        Graceful exit
        '''
        self.background()
        self._running = False
        self.gui.quit()


def listener(r, audio):
    try:
        message = r.recognize_google(audio)
        queue.put(message)
    except sr.UnknownValueError:
        pass
    except sr.RequestError as ex:
        print(ex)
    except KeyboardInterrupt:
        background()

try:
    window = Tk()
    client = ThreadedClient(window)
    window.mainloop()
except KeyboardInterrupt:
    window.destroy()
