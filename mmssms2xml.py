#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import datetime
import locale
import optparse
import os
import sqlite3
import sys
from Tkinter import *
import tkFileDialog
from xml.etree import ElementTree as etree
import webbrowser

def v(x):
    xs = unicode(x)
    if xs == "":
        return "null"
    elif x is None:
        return "null"
    else:
        return xs
    
def read_messages(dbfile):
    locale.setlocale(locale.LC_ALL, "C")
    db = sqlite3.Connection(dbfile)
    
    c = db.cursor()
    c.execute("SELECT COUNT(*) FROM sms")
    count = c.fetchone()[0]

    smses = etree.Element("smses", attrib={"count": str(count)})
    c.execute("SELECT _id, thread_id, address, person, date, protocol, read, priority, status, type, callback_number, reply_path_present, subject, body, service_center, failure_cause, locked, error_code, stack_type, seen, sort_index FROM sms ORDER BY date DESC")
    while True:
        row = c.fetchone()
        if row is None: break

        rec_id, thread_id, address, person, date, protocol, read, priority, status, type, callback_number, reply_path_present, subject, body, service_center, failure_cause, locked, error_code, stack_type, seen, sort_index = row

        if protocol is None:
            protocol = 0

        sms = etree.Element("sms", attrib={
            "protocol": v(protocol),
            "address": v(address),
            "date": v(date),
            "type": v(type),
            "subject": v(subject),
            "body": v(body),
            # toa
            # sc_toa
            "service_center": v(service_center),
            "read": v(read),
            "status": v(status),
            "locked": v(locked),
            "readable_date": datetime.datetime.fromtimestamp(date/1000).strftime("%b %d, %Y %l:%M:%S %p"),
            })
        smses.append(sms)

    return smses
        
def cli():
    parser = optparse.OptionParser(usage="%prog [options...] mmssms.db")
    parser.add_option("-o", "--output", help="Output file name (default: generated from the date of the newest SMS message)")
    opts, args = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    messages = read_messages(args[0])
    print "Read %s messages" % messages.attrib["count"]
    newest = datetime.datetime.fromtimestamp(int(messages.getchildren()[0].attrib["date"])/1000)
    if opts.output is None:
        opts.output = newest.strftime("sms-%Y%m%d%H%M%S.xml")

    try:
        os.stat(opts.output)
        ans = raw_input("Warning: file %s already exists, overwrite? " % opts.output)
        if ans.lower()[0] != 'y':
            sys.exit(0)
    except OSError:
        pass
    etree.ElementTree(messages).write(
        opts.output, encoding="utf-8", xml_declaration=True)

    print "Messages saved to %s." % opts.output
    print "Now copy this file to your SD Card into "
    print "SMSBackupRestore folder and use SMS Backup & Restore by Ritesh Sahu"
    print "to restore your messages."
    print "Google Play store link to the app (free version): http://goo.gl/ZO5cy"

class Gui(Frame):
    def open_file(self):
        filename = tkFileDialog.askopenfilename(parent=self, filetypes=[("Database Files", "*.db"),
                                                                        ("All files", "*.*")])
        try:
            os.stat(filename)
            self.messages = read_messages(filename)
            self.save["state"] = "normal"
        except OSError:
            pass

    def save_results(self):
        newest = datetime.datetime.fromtimestamp(int(self.messages.getchildren()[0].attrib["date"])/1000)
        output = newest.strftime("sms-%Y%m%d%H%M%S.xml")
        
        filename = tkFileDialog.asksaveasfilename(parent=self,
                                                  filetypes=[("XML Files", "*.xml"),
                                                             ("All files", "*.*")],
                                                  initialfile=output)
        if len(filename) == 0:
            return
        etree.ElementTree(self.messages).write(filename, encoding="utf-8", xml_declaration=True)
        self.save["state"] = "disabled"
        self.msg["width"]=50
        self.msg["height"]=6
        self.msg["state"] = "normal"
        self.msg.insert(END, "Now you should Use SMS Backup and Restore by  Ritesh Sahu to restore your messages.\n\nGoogle Play store link to the app (free version): ")
        URL = "http://goo.gl/ZO5cy"
        self.msg.insert(END, URL, ('link',))
        self.msg.tag_config('link', foreground="blue", underline=True)
        self.msg.tag_bind('link', '<Button-1>', lambda x: webbrowser.open(URL, new=True))
        self.msg["state"] = "disabled"

    def show_link(self, event):
        idx = 1

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

        Label(self, text="Click open to select mmssms.db file:").pack(side="top")
        Button(self, text="Open mmssms.db", command=self.open_file).pack(side="top")
        Label(self, text="After that click Save to save the result:").pack(side="top")
        self.save = Button(self, text="Save results", command=self.save_results, state="disabled")
        self.save.pack(side="top")
        self.msg = Text(self, height=0, width=10, relief="flat", bg=self["bg"], wrap="word")
        self.msg.pack(expand=True, fill="both")
        self.msg["state"] = "disabled"        
        

        
def gui():
    root = Tk()
    root.title("Convert mmssms.db to xml...")
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
