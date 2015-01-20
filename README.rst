
``satbot`` allows you to read and use the serial data output by common hobby R/C satellite receivers. It is possible to
simply get the relative "stick" and switch positions, which is very convenient for embedded/robotic projects.

Note that only Spektrum brand DSMX satellite receivers have been tested to-date, but Futaba and off-brand DSM2/DSMX
receivers should work, possibly with additional fiddling.

``satbot`` was created with embedded systems like the `Raspberry Pi <http://www.raspberrypi.org/>`_ in mind, but all
that is really needed is a TTL serial-usb cable (such as `this one <http://www.adafruit.com/product/954>`_.)

Assuming your satellite receiver is already bound to your transmitter and you've connected it via a USB dongle it
should be possible to simply:

    satbot start --foreground /dev/ttysXXX

At the command line, where ``/tmp/ttysXXX`` is the serial device associated with your receiver.
