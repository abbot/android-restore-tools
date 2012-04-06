# -*- encoding: utf-8 -*-

import datetime
import locale
import sqlite3
import os

from xml.etree import ElementTree as etree

if os.name == 'posix':
    datefmt = "%b %d, %Y %l:%M:%S %p"
else:
    datefmt = "%c"

def v(x):
    xs = unicode(x)
    if xs == "":
        return "null"
    elif x is None:
        return "null"
    else:
        return xs
    
def read_calls(dbfile):
    locale.setlocale(locale.LC_ALL, "C")
    db = sqlite3.Connection(dbfile)
    
    c = db.cursor()
    c.execute("SELECT COUNT(*) FROM calls")
    count = c.fetchone()[0]

    calls = etree.Element("calls", attrib={"count": str(count)})
    c.execute("SELECT number, duration, date, type FROM calls ORDER BY date DESC")
    while True:
        row = c.fetchone()
        if row is None: break

        number, duration, date, type = row
        call = etree.Element("call", attrib={
            "number": v(number),
            "duration": v(duration),
            "date": v(date),
            "type": v(type),
            })
        calls.append(call)

    c.close()
    db.close()

    return calls
        
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
            "readable_date": datetime.datetime.fromtimestamp(date/1000).strftime(datefmt),
            })
        smses.append(sms)

    c.close()
    db.close()

    return smses
