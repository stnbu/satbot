# -*- coding: utf-8 -*-

import os
import sys
import imp


class Axis(object):

    _defaults = {
        'name': None,
        'min': 0,
        'max': 0,
        'center': None,
        'reversed': False,
    }

    def __init__(self, **kwargs):
        if set(kwargs) - set(self._defaults):
            raise ValueError('Unsupported argument(s): {}'.format(', '.join(set(kwargs) - set(self._defaults))))
        for name, value in self._defaults.iteritems():
            setattr(self, name, value)
        for name, value in kwargs.iteritems():
            setattr(self, name, value)

    @property
    def range(self):
        return self.max - self.min

    def get_normalized_position(self, raw_position):
        # return value between -1 and +1
        return 2 * (float(raw_position - self.min) / float(self.max - self.min)) - 1

_default_data = {
    0: Axis(name='throttle', min=159, max=869, center=516),
    1: Axis(name='aileron', min=174, max=755, center=499, reversed=True),
    2: Axis(name='elevator', min=191, max=844, center=511, reversed=True),
    3: Axis(name='rudder', min=175, max=857, center=511),
    4: Axis(name='gear', min=173, max=869),
    5: Axis(name='flaps', min=164, max=725),
    6: Axis(name='UNUSED', min=164, max=725),
}


def get_user_data():
    user_calibration_path = os.path.expanduser(os.path.join('~', '.dsm', 'calibration.py'))
    if os.path.exists(user_calibration_path):
        user_calibration_module = imp.new_module('user_calibration_module')
        user_calibration_module.__dict__.update({'Axis': Axis})
        execfile(user_calibration_path, user_calibration_module.__dict__)
        return user_calibration_module.data
    else:
        return None


_user_data = get_user_data()
if _user_data is not None:
    data = _user_data
else:
    data = _default_data
