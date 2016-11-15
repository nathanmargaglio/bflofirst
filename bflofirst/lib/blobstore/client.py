#!/usr/bin/env python

# This is the client; just a wrapper around calls in the server..

import optparse
import sys

import zerorpc


COMMANDS_HELP = """\
store [<filename>]
    Stores the specified file. If no filename is passed or the filename
    is '-', data will be read from standard input.
    Prints the resulting blob_id on the standard output.

retrieve <blob_id> [<filename>]
    Retrieves the object specified by <blob_id> and stores it inside
    <filename>. If no <filename> was specified or <filename> is '-',
    write the object to standard output instead.

delete <blob_id>
    Silently deletes the object with specified id.

list
    Prints a list of stored objects ids.
"""


def main():
    parser = optparse.OptionParser()
    parser.disable_interspersed_args()
    parser.add_option("--port", action='store', dest='server_port')
    parser.add_option("--address", action='store', dest='server_address')
    opts, args = parser.parse_args()

    from . import DEFAULT_PORT, DEFAULT_ADDR
    server_port = opts.server_port or DEFAULT_PORT
    server_address = opts.server_address or DEFAULT_ADDR

    client = zerorpc.Client()
    client.connect("tcp://{}:{}".format(server_address, server_port))

    command = args[0]

    if command == 'help':
        print COMMANDS_HELP

    elif command == 'store':
        try:
            filename = args[1]
        except IndexError:
            filename = None

        if (filename is None) or (filename == '-'):
            blob = sys.stdin.read()
        else:
            with open(filename, 'rb') as f:
                blob = f.read()

        print client.store(blob)

    elif command == 'retrieve':
        try:
            blob_id = args[1]
        except IndexError:
            sys.stderr.write("Usage: retrieve <blob_id> [<filename>]")
            return 1

        try:
            filename = args[2]
        except IndexError:
            filename = None

        if (filename is None) or (filename == '-'):
            sys.stdout.write(client.retrieve(blob_id))
        else:
            with open(filename, 'wb') as f:
                f.write(client.retrieve(blob_id))

    elif command == 'delete':
        try:
            blob_id = args[1]
        except IndexError:
            sys.stderr.write("Usage: delete <blob_id>")
            return 1

        client.delete(blob_id)

    elif command == 'list':
        for blob_id in client.list():
            print blob_id

    else:
        sys.stderr.write(
            "No such command: {command}\n"
            "See 'help' for more information on commands.\n"
            "".format(command=command))
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
