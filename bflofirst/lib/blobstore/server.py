#!/usr/bin/env python

import hashlib
import optparse
import os
import sys

import zerorpc

DEBUG = False


def _log(message):
    if not DEBUG:
        return
    sys.stderr.write(message)
    sys.stderr.write("\n")


class NotFound(Exception):
    pass


class StorageRPC(object):
    def __init__(self, storage_dir):
        self.storage_dir = storage_dir

    def store(self, blob):
        blob_id = hashlib.sha1(blob).hexdigest()
        _log("STORE {}".format(blob_id))
        blob_path = self._get_blob_path(blob_id)
        if not os.path.exists(blob_path):
            with self._open(blob_path, 'wb') as f:
                f.write(blob)
        return blob_id

    def retrieve(self, blob_id):
        _log("RETRIEVE {}".format(blob_id))
        blob_path = self._get_blob_path(blob_id)
        try:
            with self._open(blob_path, 'rb') as f:
                return f.read()
        except IOError:
            raise NotFound(
                "Unable to retrieve blob with id: {}".format(blob_id))

    def delete(self, blob_id):
        _log("DELETE {}".format(blob_id))
        try:
            os.remove(self._get_blob_path(blob_id))
        except OSError:
            raise NotFound(
                "Unable to retrieve blob with id: {}".format(blob_id))

    @zerorpc.stream
    def list(self):
        _log("LIST")
        ## ok, now go and figure out the list of stored blobs :P
        for l1dir in os.listdir(self.storage_dir):
            l1dir_path = os.path.join(self.storage_dir, l1dir)
            for blobfile in os.listdir(l1dir_path):
                yield l1dir + blobfile

    def _get_blob_path(self, blob_id):
        return os.path.join(self.storage_dir, blob_id[:2], blob_id[2:])

    def _open(self, name, mode='rb'):
        _basedir = os.path.dirname(name)
        if 'b' not in mode:
            mode += 'b' # We always want binary mode!
        if not os.path.exists(_basedir):
            os.makedirs(_basedir)
        return open(name, mode)


def main():
    from . import DEFAULT_PORT, DEFAULT_ADDR

    parser = optparse.OptionParser(
        usage="%prog [options] <command> [args..]"
    )
    parser.disable_interspersed_args()
    parser.add_option("--storage", action='store', dest='storage_dir',
                      metavar="DIRECTORY",
                      help="Base directory for the blobs storage. If it does"
                           "not exist, it will be created. Required.")
    parser.add_option("--port", action='store', dest='listen_port',
                      metavar="PORT",
                      help="TCP port on which to listen for connections. "
                           "Defaults to {port}".format(port=DEFAULT_PORT))
    parser.add_option("--address", action='store', dest='listen_address',
                      metavar="ADDRESS",
                      help="IP address on which to listen for connections. "
                           "Defaults to {addr}".format(addr=DEFAULT_ADDR))
    parser.add_option("--debug", action='store_true', dest='enable_debug',
                      default=False,
                      help="Whether to enable debugging output.")
    opts, args = parser.parse_args()

    if opts.storage_dir is None:
        sys.stderr.write(
            "You must specify a storage directory using the --storage "
            "argument.\n"
            "See --help for more information.")
        return 1

    listen_port = opts.listen_port or DEFAULT_PORT
    listen_address = opts.listen_address or DEFAULT_ADDR

    s = zerorpc.Server(StorageRPC(opts.storage_dir))
    s.bind("tcp://{}:{}".format(listen_address, listen_port))

    print "Listening on {}:{}".format(listen_address, listen_port)

    try:
        s.run()
    except KeyboardInterrupt:
        print "Server terminated."

    return 0


if __name__ == '__main__':
    sys.exit(main())
