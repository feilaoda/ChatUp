import sys
import libtorrent

# get the input torrent file
import sys
import libtorrent

# get the input torrent file
if (len(sys.argv) > 1):
    torrent = sys.argv[1]
else:
    print "Missing param: torrent filename"
    sys.exit()
# get names of files in the torrent file

info = libtorrent.torrent_info(torrent);

for f in info.files():
    print "%s - %s" % (f.path, f.size)

info_hash = info.info_hash()
hexadecimal = str(info_hash)
print hexadecimal

