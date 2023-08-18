#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import argparse
import base64
import json
from enum import Enum
from datetime import datetime

class Format(Enum):
    uBookmark = 'ubookmark'
    buchen = 'buchen'
    html = 'html'

    def __str__(self):
        return self.value


def toUBookmark(data):

    export_fp = "decoded_ubookmark.json"

    with open(export_fp, 'w') as export:
        json.dump(data, export, indent=4)

    print("base64 decoded uBookmarks saved to %s" % (os.path.abspath(export_fp)))



def toISO8601(ts):
    if ts:
        try:
            isodate = datetime.fromtimestamp(float(ts)).strftime('%Y-%m-%dT%H:%M:%SZ')
            return isodate
        except:
            print("[x] create date is 'now' - could not parse %s" % (ts))
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')


def toBuchen(bookmarks):

    export_fp = "buchen_import.json"

    buchenized = []

    for bookmark in bookmarks:
        b = {}
        url = bookmark.get("url", None)
        name = bookmark.get("title", None)
        timestamp = bookmark.get("timestamp",  None)

        if url is None:
            print("[x] missing url - skipping %s" % (bookmark))
        else:
            b["url"] = url.strip()
            # randomly found a site with a title with newlines everywhere
            b["name"] = name.strip().replace("\n", "") if name else url.strip()
            b["created"] = toISO8601(timestamp)
        buchenized.append(b)

    if buchenized:
        with open(export_fp, 'w') as export:
            json.dump({"folders": [], "bookmarks": buchenized}, export, indent=4)

        print("buchen compatible import saved to %s" % (os.path.abspath(export_fp)))
    else:
        print("[x] bookmarks found to convert")

def main():

    parser = argparse.ArgumentParser(description='Converts uBookmark backups into a user friendly format.')
    parser.add_argument(
        'backup_file',
        metavar='backup_file',
        type=str,
        help='the uBookmark file path'
    )

    parser.add_argument('--format', type=Format, choices=list(Format))

    args = parser.parse_args()

    if args.format == Format.html:
        print("[x] bookmark HTML format support is not ready")
        sys.exit(1)

    if os.path.exists(args.backup_file):
        with open(args.backup_file, "r") as backup:
            data = json.loads(base64.b64decode(backup.read()))

            if args.format == Format.uBookmark:
                toUBookmark(data)
            elif args.format == Format.buchen:
                bookmarks = data.get("Bookmarks", None)

                if bookmarks:
                    toBuchen(bookmarks)
                else:
                    print("[x] Could not find the bookmarks in this JSON:")
                    print(json.dumps(data, indent=4))
    else:
        print("[x] cannot access file '%s'" % (args.backup_file))


if __name__ == '__main__':
    main()
