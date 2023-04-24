#!-*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2014 Joshua Banton and PyTimeCode developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__name__ = "timecode"
__version__ = "1.3.1"
__description__ = "SMPTE Time Code Manipulation Library"
__author__ = "Erkan Ozgur Yilmaz"
__author_email__ = "eoyilmaz@gmail.com"
__url__ = "https://github.com/eoyilmaz/timecode"

from timecode import Timecode, TimecodeError

class STimecode(Timecode):
    """Signed timecode class.

    Does all the calculation over frames, so the main data it holds is
    frames, then when required it converts the frames to a timecode by
    using the frame rate setting.

    :param framerate: The frame rate of the STimecode instance. It
      should be one of ['23.976', '23.98', '24', '25', '29.97', '30', '50',
      '59.94', '60', 'NUMERATOR/DENOMINATOR', ms'] where "ms" equals to
      1000 fps.
      Can not be skipped.
      Setting the framerate will automatically set the :attr:`.drop_frame`
      attribute to correct value.
    :param start_timecode: The start timecode. Use this to be able to
      set the timecode of this STimecode instance. It can be skipped and
      then the frames attribute will define the timecode, and if it is also
      skipped then the start_second attribute will define the start
      timecode, and if start_seconds is also skipped then the default value
      of '00:00:00:00' will be used.
      When using 'ms' frame rate, timecodes like '00:11:01.040' use '.040'
      as frame number. When used with other frame rates, '.040' represents
      a fraction of a second. So '00:00:00.040'@25fps is 1 frame.
    :type framerate: str or int or float or tuple
    :type start_timecode: str or None
    :param start_seconds: A float or integer value showing the seconds.
    :param int frame_number: STimecode objects can be initialized with an
      integer number showing the frame position, including zero or negative.
    :param force_non_drop_frame: If True, uses Non-Dropframe calculation for
      29.97 or 59.94 only. Has no meaning for any other framerate.
    """

    def __init__(self, framerate, start_timecode=None, frame_number=None,
                 start_seconds=None, force_non_drop_frame=False):

        self.force_non_drop_frame = force_non_drop_frame

        self.drop_frame = False

        self.ms_frame = False
        self.fraction_frame = False
        self._int_framerate = None
        self._framerate = None
        self.framerate = framerate

        self._frame_number = None

        # attribute override order
        # start_timecode > frame_number > start_seconds
        if start_timecode:
            self.frame_number = self.tc_to_frame_number(start_timecode)
        elif frame_number is not None:
            self.frame_number = frame_number
        elif start_seconds is not None:
            self.frame_number = self.float_to_frame_number(start_seconds)
        else:
            # use default value of 00:00:00:00
            self.frame_number = 0

    @property
    def frames(self):
        """getter for the frames attribute
        """
        return abs(self._frame_number) + 1

    @frames.setter
    def frames(self, frames):
        """setter for the frames attribute
        """
        if not isinstance(frames, int):
            raise TypeError(
                "%s.frames should be an integer greater than 0, "
                "not a %s" % (self.__class__.__name__, frames.__class__.__name__)
            )
        if frames < 1:
            raise TimecodeError(
                "%s.frames should be an integer greater than 0, "
                "but is %d" % (self.__class__.__name__, frames)
            )
        self.frame_number = frames - 1

    @property
    def frame_number(self):
        """getter for the _frame_number attribute
        """
        return self._frame_number
    
    @frame_number.setter
    def frame_number(self, frame_number):
        """setter for the _frame_number attribute

        :param int frame_number: An int showing the time that this TimeCode represents.
        :return:
        """
    
        if not isinstance(frame_number, int):
            raise TypeError(
                "%s.frame_number should be an integer, "
                "not a %s" % (self.__class__.__name__, frame_number.__class__.__name__)
            )
        self._frame_number = frame_number

    @property
    def framerate(self):
        """getter for _framerate attribute
        """
        return self._framerate

    @framerate.setter
    def framerate(self, framerate):  # lint:ok
        """setter for the framerate attribute
        :param framerate:
        :return:
        """
        # Convert rational frame rate to float
        numerator = None
        denominator = None

        try:
            if '/' in framerate:
                numerator, denominator = framerate.split('/')
        except TypeError:
            # not a string
            pass

        if isinstance(framerate, tuple):
            numerator, denominator = framerate

        try:
            from fractions import Fraction
            if isinstance(framerate, Fraction):
                numerator = framerate.numerator
                denominator = framerate.denominator
        except ImportError:
            pass

        if numerator and denominator:
            framerate = round(float(numerator) / float(denominator), 2)
            if framerate.is_integer():
                framerate = int(framerate)

        # check if number is passed and if so convert it to a string
        if isinstance(framerate, (int, float)):
            framerate = str(framerate)

        # set the int_frame_rate
        if framerate == '29.97':
            self._int_framerate = 30
            if self.force_non_drop_frame is True:
                self.drop_frame = False
            else:
                self.drop_frame = True
        elif framerate == '59.94':
            self._int_framerate = 60
            if self.force_non_drop_frame is True:
                self.drop_frame = False
            else:
                self.drop_frame = True
        elif any(map(lambda x: framerate.startswith(x), ['23.976', '23.98'])):
            self._int_framerate = 24
        elif framerate in ['ms', '1000']:
            self._int_framerate = 1000
            self.ms_frame = True
            framerate = 1000
        elif framerate == 'frames':
            self._int_framerate = 1
        else:
            self._int_framerate = int(float(framerate))

        self._framerate = framerate

    def set_fractional(self, state):
        """Set or unset timecode to be represented with fractional seconds
        :param bool state:
        """
        self.fraction_frame = state

    def set_timecode(self, timecode):
        """Sets the frame_number by using the given timecode
        """
        self.frame_number = self.tc_to_frame_number(timecode)

    def float_to_frame_number(self, seconds):
        """return the frame_number from the given seconds
        """
        return int(seconds * self._int_framerate)

    def tc_to_frame_number(self, timecode):
        """Converts the given timecode to frame_number
        """
        # timecode could be a STimecode instance
        if isinstance(timecode, Timecode):
            return timecode.frame_number

        hrs, mins, secs, frs, sign = map(int, STimecode.parse_timecode(timecode))
        if isinstance(timecode, int):
            time_tokens = [hrs, mins, secs, frs]
            timecode = ':'.join(str(t) for t in time_tokens)
            if sign == -1:
                timecode = '-' + timecode

            if self.drop_frame:
                timecode = ';'.join(timecode.rsplit(':', 1))

        if self.framerate != 'frames':
            ffps = float(self.framerate)
        else:
            ffps = float(self._int_framerate)

        if self.drop_frame:
            # Number of drop frames is 6% of framerate rounded to nearest
            # integer
            drop_frames = int(round(ffps * .066666))
        else:
            drop_frames = 0

        # We don't need the exact framerate anymore, we just need it rounded to
        # nearest integer
        ifps = self._int_framerate

        # Number of frames per hour (non-drop)
        hour_frames = ifps * 60 * 60

        # Number of frames per minute (non-drop)
        minute_frames = ifps * 60

        # Total number of minutes
        total_minutes = (60 * hrs) + mins

        # Handle case where frs are fractions of a second
        if len(timecode.split('.')) == 2 and not self.ms_frame:
            self.fraction_frame = True
            fraction = timecode.rsplit('.', 1)[1]

            frs = int(round(float('.' + fraction) * ffps))

        frame_number = \
            (hour_frames * hrs) + (minute_frames * mins) + \
            (ifps * secs) + frs - \
            (drop_frames * (total_minutes - (total_minutes // 10)))
        
        return frame_number * sign

    def frame_number_to_tc(self, frame_number):
        """Converts frame_number back to timecode

        :returns str: the string representation of the current time code
        """

        sign = 1
        if frame_number < 0:
            sign = -1
            frame_number = - frame_number
        if self.drop_frame:
            # Number of frames to drop on the minute marks is the nearest
            # integer to 6% of the framerate
            ffps = float(self.framerate)
            drop_frames = int(round(ffps * .066666))
        else:
            ffps = float(self._int_framerate)
            drop_frames = 0

        # Number of frames per ten minutes
        frames_per_10_minutes = int(round(ffps * 60 * 10))

        # Number of frames in a day - timecode rolls over after 24 hours
        frames_per_24_hours = int(round(ffps * 60 * 60 * 24))

        # Number of frames per minute is the round of the framerate * 60 minus
        # the number of dropped frames
        frames_per_minute = int(round(ffps) * 60) - drop_frames

        # If frame_number is greater than 24 hrs, next operation will rollover
        # clock
        frame_number %= frames_per_24_hours

        if self.drop_frame:
            d = frame_number // frames_per_10_minutes
            m = frame_number % frames_per_10_minutes
            if m > drop_frames:
                frame_number += (drop_frames * 9 * d) + drop_frames * ((m - drop_frames) // frames_per_minute)
            else:
                frame_number += drop_frames * 9 * d

        ifps = self._int_framerate

        frs = frame_number % ifps

        if self.fraction_frame:
            frs = round(frs / float(ifps), 3)

        secs = int((frame_number // ifps) % 60)
        mins = int(((frame_number // ifps) // 60) % 60)
        hrs = int((((frame_number // ifps) // 60) // 60))

        if hrs == mins == secs == frs == 0:
            sign = 1
        
        return hrs, mins, secs, frs, sign

    def tc_to_string(self, hrs, mins, secs, frs, sign):
        sign = '-' if sign < 0 else ''

        if self.fraction_frame:
            return "{sign}{hh:02d}:{mm:02d}:{ss:06.3f}".format(
                sign=sign, hh=hrs, mm=mins, ss=secs + frs
            )

        ff = "%02d"
        if self.ms_frame:
            ff = "%03d"
        
        return ("%s%02d:%02d:%02d%s" + ff) % (
            sign, hrs, mins, secs, self.frame_delimiter, frs
        )

    @classmethod
    def parse_timecode(cls, timecode):
        """parses timecode string NDF '00:00:00:00' or DF '00:00:00;00' or
        milliseconds/fractionofseconds '00:00:00.000'
        """
        sign = 1
        if isinstance(timecode, int):
            if timecode < 0:
                sign = -1
                timecode = - timecode
            hex_repr = hex(timecode)
            # fix short string
            hex_repr = '0x%s' % (hex_repr[2:].zfill(8))
            hrs, mins, secs, frs = tuple(map(int, [hex_repr[i:i + 2] for i in range(2, 10, 2)]))
        elif isinstance(timecode, str):
            if timecode.startswith('-'):
                sign = -1
                timecode = timecode[1:]
            bfr = timecode.replace(';', ':').replace('.', ':').split(':')
            hrs = int(bfr[0])
            mins = int(bfr[1])
            secs = int(bfr[2])
            frs = int(bfr[3])
        else:
            raise TimecodeError(
                'Type %s not supported as timecode.' %
                timecode.__class__.__name__
            )

        if hrs == 0 and mins == 0 and secs == 0 and frs == 0:
            sign = 1
            
        return hrs, mins, secs, frs, sign

    @property
    def frame_delimiter(self):
        """Return correct symbol based on framerate."""
        if self.drop_frame:
            return ';'

        elif self.ms_frame or self.fraction_frame:
            return '.'

        else:
            return ':'

    def __iter__(self):
        yield self

    def next(self):
        self.add_frame_number(1)
        return self

    def back(self):
        self.sub_frame_number(1)
        return self

    def add_frame_number(self, frames):
        """adds/subtracts frames to/from frame_number
        """
        self.frame_number += frames

    def sub_frame_number(self, frames):
        """adds/subtracts frames to/from frame_number
        """
        self.add_frame_number(-frames)

    def mult_frame_number(self, frames):
        """multiply frame_number by frames
        """
        self.frame_number *= frames

    def div_frame_number(self, frames):
        """devide frame_number by frames"""
        self.frame_number = int(self.frame_number / frames)

    def add_frames(self, frames):
        """adds/subtracts frames to/from frames
        """
        self.add_frame_number(frames)

    def sub_frames(self, frames):
        """adds/subtracts frames to/from frames
        """
        self.sub_frame_number(frames)

    def mult_frames(self, frames):
        """multiply frames by frames
        """
        self.frames = (self.frame_number + self.sign) * frames

    def div_frames(self, frames):
        """devide frames by frames"""
        self.frames = int((self.frame_number + self.sign) / frames)

    def __eq__(self, other):
        """the overridden equality operator
        """
        if isinstance(other, Timecode):
            return self.framerate == other.framerate and self.frame_number == other.frame_number
        elif isinstance(other, str):
            new_tc = STimecode(self.framerate, other)
            return self.__eq__(new_tc)
        elif isinstance(other, int):
            return self.frame_number == other
        else:
            raise TimecodeError(
                'Type %s not supported for comparison.' %
                other.__class__.__name__
            )

    def __ge__(self, other):
        """override greater or equal to operator"""
        if isinstance(other, Timecode):
            return self.framerate == other.framerate and self.frame_number >= other.frame_number
        elif isinstance(other, str):
            new_tc = STimecode(self.framerate, other)
            return self.frame_number >= new_tc.frame_number
        elif isinstance(other, int):
            return self.frame_number >= other
        else:
            raise TimecodeError(
                'Type %s not supported for comparison.' %
                other.__class__.__name__
            )

    def __gt__(self, other):
        """override greater operator"""
        if isinstance(other, Timecode):
            return self.framerate == other.framerate and self.frame_number > other.frame_number
        elif isinstance(other, str):
            new_tc = STimecode(self.framerate, other)
            return self.frame_number > new_tc.frame_number
        elif isinstance(other, int):
            return self.frame_number > other
        else:
            raise TimecodeError(
                'Type %s not supported for comparison.' %
                other.__class__.__name__
            )

    def __le__(self, other):
        """override less or equal to operator"""
        if isinstance(other, Timecode):
            return self.framerate == other.framerate and self.frame_number <= other.frame_number
        elif isinstance(other, str):
            new_tc = STimecode(self.framerate, other)
            return self.frame_number <= new_tc.frame_number
        elif isinstance(other, int):
            return self.frame_number <= other
        else:
            raise TimecodeError(
                'Type %s not supported for comparison.' %
                other.__class__.__name__
            )

    def __lt__(self, other):
        """override less operator"""
        if isinstance(other, Timecode):
            return self.framerate == other.framerate and self.frame_number < other.frame_number
        elif isinstance(other, str):
            new_tc = STimecode(self.framerate, other)
            return self.frame_number < new_tc.frame_number
        elif isinstance(other, int):
            return self.frame_number < other
        else:
            raise TimecodeError(
                'Type %s not supported for comparison.' %
                other.__class__.__name__
            )

    def __add__(self, other):
        """returns new STimecode instance with the given timecode or frames
        added to this one
        """
        if isinstance(other, Timecode):
            added_frame_number = self.frame_number + other.frame_number
        elif isinstance(other, int):
            added_frame_number = self.frame_number + other
        else:
            raise TimecodeError(
                'Type %s not supported for arithmetic.' %
                other.__class__.__name__
            )

        return STimecode(self.framerate, frame_number=added_frame_number, force_non_drop_frame=self.force_non_drop_frame)

    def __sub__(self, other):
        """returns new STimecode instance with subtracted value"""
        if isinstance(other, Timecode):
            subtracted_frame_number = self.frame_number - other.frame_number
        elif isinstance(other, int):
            subtracted_frame_number = self.frame_number - other
        else:
            raise TimecodeError(
                'Type %s not supported for arithmetic.' %
                other.__class__.__name__
            )

        return STimecode(self.framerate, frame_number=subtracted_frame_number, force_non_drop_frame=self.force_non_drop_frame)

    def __mul__(self, other):
        """returns new STimecode instance with multiplied value"""
        if isinstance(other, Timecode):
            multiplied_frame_number = self.frame_number * other.frame_number
        elif isinstance(other, int):
            multiplied_frame_number = self.frame_number * other
        else:
            raise TimecodeError(
                'Type %s not supported for arithmetic.' %
                other.__class__.__name__
            )

        return STimecode(self.framerate, frame_number=multiplied_frame_number, force_non_drop_frame=self.force_non_drop_frame)

    def __div__(self, other):
        """returns new STimecode instance with divided value"""
        if isinstance(other, Timecode):
            div_frame_number = int(float(self.frame_number) / float(other.frame_number))
        elif isinstance(other, int):
            div_frame_number = int(float(self.frame_number) / float(other))
        else:
            raise TimecodeError(
                'Type %s not supported for arithmetic.' %
                other.__class__.__name__
            )

        return STimecode(self.framerate, frame_number=div_frame_number, force_non_drop_frame=self.force_non_drop_frame)

    def __truediv__(self, other):
        """returns new STimecode instance with divided value"""
        return self.__div__(other)

    def __radd__(self, other):
        """returns new STimecode instance with the given timecode or frames
        added to this one
        """
        if isinstance(other, Timecode) and self.framerate != other.framerate:
            me = STimecode(other.framerate, frame_number=self.frame_number, force_non_drop_frame=other.force_non_drop_frame)
            return me.__add__(other)
        else:
            return self.__add__(other)

    def __rsub__(self, other):
        """returns new STimecode instance with subtracted value"""
        if isinstance(other, Timecode) and self.framerate != other.framerate:
            me = STimecode(other.framerate, frame_number=self.frame_number, force_non_drop_frame=other.force_non_drop_frame)
            return - me.__sub__(other)
        else:
            return - self.__sub__(other)

    def __rmul__(self, other):
        """returns new STimecode instance with multiplied value"""
        if isinstance(other, Timecode) and self.framerate != other.framerate:
            me = STimecode(other.framerate, frame_number=self.frame_number, force_non_drop_frame=other.force_non_drop_frame)
            return me.__mul__(other)
        else:
            return self.__mul__(other)

    def __rtruediv__(self, other):
        """returns new STimecode instance with divided value"""
        if isinstance(other, Timecode):
            div_frame_number = int(float(other.frame_number) / float(self.frame_number))
            if self.framerate != other.framerate:
                return STimecode(other.framerate, frame_number=div_frame_number, force_non_drop_frame=other.force_non_drop_frame)
            else:
                return STimecode(self.framerate, frame_number=div_frame_number, force_non_drop_frame=self.force_non_drop_frame)
        else:
            raise TimecodeError(
                'Type %s not supported for arithmetic.' %
                other.__class__.__name__
            )
        
    def __repr__(self):
        return self.tc_to_string(*self.frame_number_to_tc(self.frame_number))

    @property
    def hrs(self):
        hrs, mins, secs, frs, sign = self.frame_number_to_tc(self.frame_number)
        return hrs

    @property
    def mins(self):
        hrs, mins, secs, frs, sign = self.frame_number_to_tc(self.frame_number)
        return mins

    @property
    def secs(self):
        hrs, mins, secs, frs, sign = self.frame_number_to_tc(self.frame_number)
        return secs

    @property
    def frs(self):
        hrs, mins, secs, frs, sign = self.frame_number_to_tc(self.frame_number)
        return frs

    @property
    def float(self):
        """returns the seconds as float
        """
        return float(self.frame_number) / float(self._int_framerate)

    @property
    def sign(self):
        """returns the sign, 1 or -1 [ADD]
        """
        return -1 if self._frame_number < 0 else 1

    def __neg__(self):
        """uniary operator '-' [ADD]
        """
        return STimecode(self.framerate, frame_number= -self.frame_number, force_non_drop_frame=self.force_non_drop_frame)
