# uBookmark Recover

For users of the Mac app uBookmark to convert their backup files to a useable format.


uBookmark provides back-ups as base64 encoded JSON. If you just want your data, paste the contents of your back up file into a site like https://www.base64decode.org/ and get your JSON data.

This file will extract your data in various formats

1. A plain uBookmark JSON file (i.e. it will just base64 decode it)
2. The Buchen JSON import format ( [Buchen for iOS, iPad and macOS](https://apps.apple.com/app/buchen-bookmark-manager/id1549093588?platform=iphone))
3. **TODO** The bookmark html format - this is the one you want to import your data into any browser including [Buchen](https://apps.apple.com/app/buchen-bookmark-manager/id1549093588?platform=iphone)

## Usage

`python export.py <backup file> --format <buchen or ubookmark>`

Example:

`python export.py ~/Downloads/uBookmark_Backup.json --format ubookmark`

## Caveats

1. This has only been tested on uBookmark version 2.2.1.
2. The back-up files appear to only have your bookmarks and **NOT** your collections. You can cannot recover your collections
3. Tested under Python 3 but attempts to keep Python 2 compatibility.
4. The initial version is a rough and quick first pass. When in doubt just use the format `ubookmark` and manually do whatever you want with the raw JSON.

# Testing

There is a test backup file under `test` for any experimenting you may want to do.
