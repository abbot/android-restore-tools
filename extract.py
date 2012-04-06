#!/usr/bin/env python

import ctypes
import optparse
import os
import sys

import yaffs

def read_chunk(fd, size):
    s = fd.read(size)
    if len(s) > 0 and len(s) != size:
        raise IOError("Broken image file")
    return s

def read_segment(fd):
    chunk_data = read_chunk(fd, yaffs.CHUNK_SIZE)
    spare_data = read_chunk(fd, yaffs.SPARE_SIZE)
    if len(chunk_data) == 0 and len(spare_data) == 0:
        return None, None
    elif len(chunk_data) == 0 or len(spare_data) == 0:
        raise IOError("Broken image file")
    return chunk_data, yaffs.PackedTags2.from_buffer_copy(spare_data)

def extract(filename):
    fd = open(filename, "rb")
    yaffs_objects = {yaffs.OBJECTID_ROOT: "."}

    while True:
        chunk_data, tags = read_segment(fd)
        if chunk_data is None:
            break

        if tags.t.byteCount == 0xffff:
            header = yaffs.ObjectHeader.from_buffer_copy(chunk_data)
            full_path_name = os.path.join(yaffs_objects[header.parentObjectId], header.name)
            yaffs_objects[tags.t.objectId] = full_path_name

            if header.type == yaffs.FILE:
                remaining = header.fileSize
                out = open(full_path_name, "wb")
                os.fchmod(out.fileno(), header.yst_mode)
                while remaining > 0:
                    chunk_data, tags = read_segment(fd)
                    if remaining < tags.t.byteCount:
                        s = chunk_data[:remain]
                    else:
                        s = chunk_data[:tags.t.byteCount]
                    out.write(s)
                    remaining -= len(s)
                print "wrote", full_path_name
            elif header.type == yaffs.SYMLINK:
                os.symlink(header.alias, full_path_name)
                print "symlink %s -> %s" % (header.alias, full_path_name)
            elif header.type == yaffs.DIRECTORY:
                try:
                    os.mkdir(full_path_name, 0777)
                    print "created directory %s" % full_path_name
                except OSError, exc:
                    if "File exists" in str(exc):
                        pass
                    else:
                        print str(exc)
                        raise
            elif header.type == yaffs.HARDLINK:
                os.link(yaffs_objects[header.equivalentObjectId], full_path_name)
                print "hardlink %s -> %s" % (yaffs_objects[header.equivalentObjectId], full_path_name)
            else:
                print "skipping unknown object"
                

def get_files(filename, filenames, callback=None):
    fd = open(filename, "rb")
    yaffs_objects = {yaffs.OBJECTID_ROOT: "."}

    rc = {}

    while True:
        chunk_data, tags = read_segment(fd)
        if chunk_data is None:
            break

        if tags.t.byteCount == 0xffff:
            header = yaffs.ObjectHeader.from_buffer_copy(chunk_data)
            full_path_name = os.path.join(yaffs_objects[header.parentObjectId], header.name)
            yaffs_objects[tags.t.objectId] = full_path_name
            if callback is not None:
                callback(header)

            if header.type == yaffs.FILE:
                remaining = header.fileSize
                contents = ""
                if header.name in filenames:
                    while remaining > 0:
                        chunk_data, tags = read_segment(fd)
                        if remaining < tags.t.byteCount:
                            s = chunk_data[:remain]
                        else:
                            s = chunk_data[:tags.t.byteCount]
                        contents += s
                        remaining -= len(s)

                    rc[full_path_name] = contents
                else:
                    blocks = (remaining + yaffs.CHUNK_SIZE - 1) / yaffs.CHUNK_SIZE
                    fd.seek(blocks*(yaffs.CHUNK_SIZE+yaffs.SPARE_SIZE), 1)
                
    return rc

def dotty(header):
    if header.name.endswith(".db"):
        sys.stdout.write("+")
    else:
        sys.stdout.write(".")
    sys.stdout.flush()

def main():
    parser = optparse.OptionParser(usage="%prog [options...] data.img")
    parser.add_option("-x", "--extract", action="store_true",
                      help="Don't search for required databases, just extract the filesystem")
    opts, args = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    if opts.extract:
        extract(args[0])
    else:
        print "Scanning and reading image (this may take some time)"
        r = get_files(args[0], ["mmssms.db", "contacts2.db"], dotty)
        print ""
        print "Found files:"
        names = r.keys()
        for i, n in enumerate(names):
            print "[%d] %s" % (i+1, n)

        while True:
            n = int(raw_input("Enter file number to extract (0 to quit): ")) - 1
            if n < 0 or n >= len(names):
                break
            name = names[n]
            t = raw_input("File type (1=mmssms.db, 2=contacts2.db): ")
            if t[0] == "1":
                open("mmssms.db", "wb").write(r[names[n]])
            elif t[0] == "2":
                open("contacts2.db", "wb").write(r[names[n]])
            else:
                break

if __name__ == '__main__':
    main()
