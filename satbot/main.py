# -*- coding: utf-8 -*-

import sys
import serial
import curses
import calibration
import random


def get_channel_data(bytes):
    for index, byte in enumerate(bytes):
        if index % 2:  # if an odd member
            channel_id = last & 0b11111100
            channel_id = channel_id >> 2  # first two bits are for something else
            last = last & 0b00000011  # mask the first 6 bits
            last = last << 8
            position = byte | last  # "append" byte to the last byte
            yield channel_id, position
        last = byte


def normalize_channel_data(data):
    for channel_id, position in data:
        try:
            axis = calibration.data[channel_id]
            yield channel_id, axis.get_normalized_position(position)
        except KeyError:
            print >>sys.stderr, "got unknown channel id: {0}".format(channel_id)


class Handler(object):
    """Should have __call__, setup, and cleanup methods.
    """

    def setup(self):
        """Called before the loop that reads channel data.
        """

    def cleanup(self):
        """Called after the loop that reads channel data.
        """


class CursesVisualizer(Handler):

    def setup(self):
        self.stdscr = curses.initscr()

    def __call__(self, channel_data):
        s = ''
        for channel_id, position in channel_data:
            s += 'cid={0} {1}\t{2}\n'.format(channel_id, calibration.data[channel_id].name, position)
        s += '\n'
        self.stdscr.addstr(0, 0, s)
        self.stdscr.refresh()

    def cleanup(self):
        curses.endwin()


class Visualizer(Handler):

    def __call__(self, channel_data):
        if random.randint(0, 10) != 9:  # crude throttling
            return
        for _, position in channel_data:
            print position,
        print ''


def do_dsm(port, handler=Visualizer()):

    with serial.Serial(port=port, baudrate=115200, bytesize=8, parity='N', stopbits=1) as ser:

        byte = None

        while byte != '\r':  # read, discard first frame
            byte = ser.read(1)
            continue

        handler.setup()

        last_channel_data = None
        while True:
            try:
                bytes = []
                for x in range(16):
                    bytes.append(ser.read(1))

                bytes = bytes[-1:] + bytes[:-1]  # the first byte comes last. rotate. (?!)
                bytes = map(ord, bytes)  # turn them into ints for python

                channel_data = get_channel_data(bytes)
                channel_data = normalize_channel_data(channel_data)
                # take some pressure off of "handler" and only call if changed.
                if channel_data != last_channel_data:
                    handler(channel_data)
                last_channnel_data = channel_data

            except KeyboardInterrupt:
                break

        handler.cleanup()
