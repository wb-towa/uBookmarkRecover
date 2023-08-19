#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import argparse
import base64
import json
from datetime import datetime


UBOOKMARK = 'ubookmark'
BUCHEN = 'buchen'
HTML = 'html'
FORMATS = [UBOOKMARK, BUCHEN, HTML]

HTML_START = """
<!DOCTYPE NETSCAPE-Bookmark-file-1>
<HTML>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<Title>Bookmarks</Title>
<H1>Bookmarks</H1>
"""

HTML_END = "</DL><p>\n"

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


def toIntTimestamp(ts):
    if ts:
        try:
            int_timestamp = int(float(ts))
            return int_timestamp
        except:
            print("[x] create timestamp is 'now' - could not parse %s" % (ts))
    return int(datetime.now().timestamp())


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


def toHTML(bookmarks):
    """
    An example of a basic, does the job, bookmark.html file.
    This is all that's needed as the uBookmark backup doesn't give collections.
    <!DOCTYPE NETSCAPE-Bookmark-file-1>
    <HTML>
    <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
    <Title>Bookmarks</Title>
    <H1>Bookmarks</H1>
    <DL><p>
        <DT><A HREF="https://1password.com" ADD_DATE="0">1Password</A>
    </DL><p>
    """
    export_fp = "bookmarks.html"

    with open(export_fp, 'w') as export:
        export.write(HTML_START)

        for bookmark in bookmarks:
            url = bookmark.get("url", None)
            title = bookmark.get("title", None)
            timestamp = bookmark.get("timestamp",  None)

            if url:
                url = url.strip()
                title = title.strip().replace("\n", "") if title else url.strip()
                export.write("    <DT><A HREF=\"%s\" ADD_DATE=\"%d\">%s</A>\n" % (url, toIntTimestamp(timestamp), title))
            else:
                print("[x] missing url - skipping %s" % (bookmark))
        export.write(HTML_END)

    print("browser HTML import saved to %s" % (os.path.abspath(export_fp)))


def main():

    parser = argparse.ArgumentParser(description='Converts uBookmark backups into a user friendly format.')
    parser.add_argument(
        'backup_file',
        metavar='backup_file',
        type=str,
        help='the uBookmark file path'
    )

    parser.add_argument('--format', type=str, choices=FORMATS)

    args = parser.parse_args()

    if os.path.exists(args.backup_file):
        with open(args.backup_file, "r") as backup:
            data = json.loads(base64.b64decode(backup.read()))

            if args.format == UBOOKMARK:
                toUBookmark(data)
            elif args.format == BUCHEN:
                bookmarks = data.get("Bookmarks", None)

                if bookmarks:
                    toBuchen(bookmarks)
                else:
                    print("[x] Could not find the bookmarks in this JSON:")
                    print(json.dumps(data, indent=4))
            elif args.format == HTML:

                bookmarks = data.get("Bookmarks", None)

                if bookmarks:
                    toHTML(bookmarks)
                else:
                    print("[x] Could not find the bookmarks in this JSON:")
                    print(json.dumps(data, indent=4))
            else:
                print("[x] I cannot do anything with format %s - how did we get here?" % (args.format))
                parser.print_help()
    else:
        print("[x] cannot access file '%s'" % (args.backup_file))


if __name__ == '__main__':
    main()
