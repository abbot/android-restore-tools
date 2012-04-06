#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import datetime
import optparse
import os
import sys
from Tkinter import Tk, Text, Label, Button, Frame, END
import tkFileDialog
from xml.etree import ElementTree as etree
import webbrowser

from convert import read_calls

def cli():
    parser = optparse.OptionParser(usage="%prog [options...] contacts2.db")
    parser.add_option("-o", "--output", help="Output file name (default: generated from the date of the newest call)")
    opts, args = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    calls = read_calls(args[0])
    print "Read %s calls" % calls.attrib["count"]
    newest = datetime.datetime.fromtimestamp(int(calls.getchildren()[0].attrib["date"])/1000)
    if opts.output is None:
        opts.output = newest.strftime("calls-%Y%m%d%H%M%S.xml")

    try:
        os.stat(opts.output)
        ans = raw_input("Warning: file %s already exists, overwrite? " % opts.output)
        if ans.lower()[0] != 'y':
            sys.exit(0)
    except OSError:
        pass
    etree.ElementTree(calls).write(
        opts.output, encoding="utf-8", xml_declaration=True)

    print "Call logs saved to %s." % opts.output
    print "Now copy this file to your SD Card into "
    print "CallLogBackupRestore folder and use Call Logs Backup & Restore by Ritesh Sahu"
    print "to restore your call logs."
    print "Google Play store link to the app (free version): http://goo.gl/ZO5cy"

class Gui(Frame):
    def open_file(self):
        filename = tkFileDialog.askopenfilename(parent=self, filetypes=[("Database Files", "*.db"),
                                                                        ("All files", "*.*")])
        try:
            os.stat(filename)
            self.calls = read_calls(filename)
            self.save["state"] = "normal"
        except OSError:
            pass

    def save_results(self):
        newest = datetime.datetime.fromtimestamp(int(self.calls.getchildren()[0].attrib["date"])/1000)
        output = newest.strftime("calls-%Y%m%d%H%M%S.xml")
        
        filename = tkFileDialog.asksaveasfilename(parent=self,
                                                  filetypes=[("XML Files", "*.xml"),
                                                             ("All files", "*.*")],
                                                  initialfile=output)
        if len(filename) == 0:
            return
        etree.ElementTree(self.calls).write(filename, encoding="utf-8", xml_declaration=True)
        self.save["state"] = "disabled"
        self.msg["width"]=50
        self.msg["height"]=6
        self.msg["state"] = "normal"
        self.msg.insert(END, "Now you should Use Call Logs Backup & Restore by  Ritesh Sahu to restore your calls.\n\nGoogle Play store link to the app (free version): ")
        URL = "http://goo.gl/MOKKJ"
        self.msg.insert(END, URL, ('link',))
        self.msg.tag_config('link', foreground="blue", underline=True)
        self.msg.tag_bind('link', '<Button-1>', lambda x: webbrowser.open(URL, new=True))
        self.msg["state"] = "disabled"

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

        Label(self, text="Click open to select contacts2.db file:").pack(side="top")
        Button(self, text="Open contacts2.db", command=self.open_file).pack(side="top")
        Label(self, text="After that click Save to save the result:").pack(side="top")
        self.save = Button(self, text="Save results", command=self.save_results, state="disabled")
        self.save.pack(side="top")
        self.msg = Text(self, height=0, width=10, relief="flat", bg=self["bg"], wrap="word")
        self.msg.pack(expand=True, fill="both")
        self.msg["state"] = "disabled"        
        

        
def gui():
    root = Tk()
    root.title("Convert contacts2.db to xml...")
    app = Gui(root)
    app.mainloop()

if __name__ == '__main__':
    if os.name == 'posix':
        if len(sys.argv) == 1 and "DISPLAY" in os.environ:
            gui()
        else:
            cli()
    else:
        gui()
