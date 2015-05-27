#!/usr/bin/python


from Tkinter import *


class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background='white')
        self.parent = parent
        self.initUI()

    def initUI(self):
        colours = ['red','green','orange','white','yellow','blue']

        '''
        r = 0
        for c in colours:
            Label(text=c, relief=RIDGE,width=15).grid(row=r,column=0)
            Entry(bg=c, relief=SUNKEN,width=10).grid(row=r,column=1)
            r = r + 1
        '''

        Button(text="Quit", command=self.quit, width=50).grid(row=0, column=0)
        Label(text='LOLZA', relief=RIDGE,width=15).grid(row=1,column=0)


def main():
    root = Tk()
    root.geometry("640x480+300+300")
    app = Example(root)
    root.mainloop()


main()
