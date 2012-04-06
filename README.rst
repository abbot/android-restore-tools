===============================
 Android backup recovery tools
===============================

This package contains utilities which can be used to convert android
SMS/MMS database and android contacts database to XML dumps, readable
by popular android backup/restore tools.

extract
=======

This program can extract yaffs filesystem images (usually produced by
recovery backups) or just search for contacts and SMS databases in
images.

callog2xml
==========

This program converts contacts2.db into XML Call Log readable by `Call
Logs Backup & Restore <http://goo.gl/MOKKJ>`_ by Ritesh Sahu. Convert
your contacts2.db, copy resulting xml file to phone sdcard and use
that program to restore call logs.

mmssms2xml
==========

This program converts mmssms.db into XML SMS Log readable by `SMS
Backup & Restore <http://goo.gl/ZO5cy>`_ by Ritesh Sahu. Convert your
mmssms.db, copy resulting xml file to phone sdcard and use that
program to restore SMS messages.


Copying
=======

Copyright (C) 2012 Lev Shamardin.
