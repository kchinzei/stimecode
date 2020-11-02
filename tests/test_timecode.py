#!-*- coding: utf-8 -*-

import unittest

from timecode import Timecode


class TimecodeTester(unittest.TestCase):
    """tests Timecode class
    """

    @classmethod
    def setUpClass(cls):
        """set up the test in class level
        """
        pass

    @classmethod
    def tearDownClass(cls):
        """clean up the tests in class level
        """
        pass

    def test_instance_creation(self):
        """test instance creation, none of these should raise any error
        """
        Timecode('23.976', '00:00:00:00')
        Timecode('23.98', '00:00:00:00')
        Timecode('24', '00:00:00:00')
        Timecode('25', '00:00:00:00')
        Timecode('29.97', '00:00:00;00')
        Timecode('30', '00:00:00:00')
        Timecode('50', '00:00:00:00')
        Timecode('59.94', '00:00:00;00')
        Timecode('60', '00:00:00:00')
        Timecode('ms', '03:36:09.230')
        Timecode('24', start_timecode=None, frames=12000)

        Timecode('23.976')
        Timecode('23.98')
        Timecode('24')
        Timecode('25')
        Timecode('29.97')
        Timecode('30')
        Timecode('50')
        Timecode('59.94')
        Timecode('60')
        Timecode('ms')

        Timecode('23.976', 421729315)
        Timecode('23.98', 421729315)
        Timecode('24', 421729315)
        Timecode('25', 421729315)
        Timecode('29.97', 421729315)
        Timecode('30', 421729315)
        Timecode('50', 421729315)
        Timecode('59.94', 421729315)
        Timecode('60', 421729315)
        Timecode('ms', 421729315)

        Timecode('24000/1000', '00:00:00:00')
        Timecode('24000/1001', '00:00:00;00')
        Timecode('30000/1000', '00:00:00:00')
        Timecode('30000/1001', '00:00:00;00')
        Timecode('60000/1000', '00:00:00:00')
        Timecode('60000/1001', '00:00:00;00')

        Timecode((24000, 1000), '00:00:00:00')
        Timecode((24000, 1001), '00:00:00;00')
        Timecode((30000, 1000), '00:00:00:00')
        Timecode((30000, 1001), '00:00:00;00')
        Timecode((60000, 1000), '00:00:00:00')
        Timecode((60000, 1001), '00:00:00;00')

        Timecode(24, frames=12000)
        Timecode(23.976, '00:00:00:00')
        Timecode(23.98, '00:00:00:00')
        Timecode(24, '00:00:00:00')
        Timecode(25, '00:00:00:00')
        Timecode(29.97, '00:00:00;00')
        Timecode(30, '00:00:00:00')
        Timecode(50, '00:00:00:00')
        Timecode(59.94, '00:00:00;00')
        Timecode(60, '00:00:00:00')
        Timecode(1000, '03:36:09.230')
        Timecode(24, start_timecode=None, frames=12000)

        Timecode(23.976)
        Timecode(23.98)
        Timecode(24)
        Timecode(25)
        Timecode(29.97)
        Timecode(30)
        Timecode(50)
        Timecode(59.94)
        Timecode(60)
        Timecode(1000)
        Timecode(24, frames=12000)

    def test_2398_vs_23976(self):
        timeobj1 = Timecode('23.98', '04:01:45:23')
        timeobj2 = Timecode('23.976', '04:01:45:23')
        self.assertEqual(timeobj1._frames, timeobj2._frames)
        self.assertEqual(repr(timeobj1), repr(timeobj2))

    def test_repr_overload(self):
        timeobj = Timecode('24', '01:00:00:00')
        self.assertEqual('01:00:00:00', timeobj.__repr__())

        timeobj = Timecode('23.98', '20:00:00:00')
        self.assertEqual('20:00:00:00', timeobj.__repr__())

        timeobj = Timecode('29.97', '00:09:00;00')
        self.assertEqual('00:08:59;28', timeobj.__repr__())

        timeobj = Timecode('29.97', '00:09:00:00', force_non_drop_frame=True)
        self.assertEqual('00:08:59:14', timeobj.__repr__())

        timeobj = Timecode('30', '00:10:00:00')
        self.assertEqual('00:10:00:00', timeobj.__repr__())

        timeobj = Timecode('60', '00:00:09:00')
        self.assertEqual('00:00:09:00', timeobj.__repr__())

        timeobj = Timecode('59.94', '00:00:20;00')
        self.assertEqual('00:00:20;00', timeobj.__repr__())

        timeobj = Timecode('59.94', '00:00:20;00')
        self.assertNotEqual('00:00:20:00', timeobj.__repr__())

        timeobj = Timecode('ms', '00:00:00.900')
        self.assertEqual('00:00:00.900', timeobj.__repr__())

        timeobj = Timecode('ms', '00:00:00.900')
        self.assertNotEqual('00:00:00:900', timeobj.__repr__())

        timeobj = Timecode('24', frames=49)
        self.assertEqual('00:00:02:00', timeobj.__repr__())

    def test_timecode_init(self):
        """testing several timecode initialization
        """
        tc = Timecode('29.97')
        self.assertEqual('00:00:00;00', tc.__str__())
        self.assertEqual(1, tc._frames)

        tc = Timecode('29.97', force_non_drop_frame=True)
        self.assertEqual('00:00:00:00', tc.__str__())
        self.assertEqual(1, tc._frames)

        tc = Timecode('29.97', force_non_drop_frame=True)

        tc = Timecode('29.97', '00:00:00;01')
        self.assertEqual(2, tc._frames)

        tc = Timecode('29.97', '00:00:00:01', force_non_drop_frame=True)
        self.assertEqual(2, tc._frames)

        tc = Timecode('29.97', '03:36:09;23')
        self.assertEqual(388704, tc._frames)

        tc = Timecode('29.97', '03:36:09:23', force_non_drop_frame=True)
        self.assertEqual(388705, tc._frames)

        tc = Timecode('29.97', '03:36:09;23')
        self.assertEqual(388704, tc._frames)

        tc = Timecode('30', '03:36:09:23')
        self.assertEqual(389094, tc._frames)

        tc = Timecode('25', '03:36:09:23')
        self.assertEqual(324249, tc._frames)

        tc = Timecode('59.94', '03:36:09;23')
        self.assertEqual(777384, tc._frames)

        tc = Timecode('60', '03:36:09:23')
        self.assertEqual(778164, tc._frames)

        tc = Timecode('59.94', '03:36:09;23')
        self.assertEqual(777384, tc._frames)

        tc = Timecode('23.98', '03:36:09:23')
        self.assertEqual(311280, tc._frames)

        tc = Timecode('24', '03:36:09:23')
        self.assertEqual(311280, tc._frames)

        tc = Timecode('ms', '03:36:09.230')
        self.assertEqual(3, tc.hrs)
        self.assertEqual(36, tc.mins)
        self.assertEqual(9, tc.secs)
        self.assertEqual(230, tc.frs)

        tc = Timecode('24', frames=12000)
        self.assertEqual('00:08:19:23', tc.__str__())

        tc = Timecode('29.97', frames=2589408)
        self.assertEqual('23:59:59;29', tc.__str__())

        tc = Timecode('29.97', frames=2589409)
        self.assertEqual('00:00:00;00', tc.__str__())

        tc = Timecode('29.97', frames=2589409, force_non_drop_frame=True)
        self.assertEqual('00:00:00:00', tc.__str__())

        tc = Timecode('59.94', frames=5178816)
        self.assertEqual('23:59:59;59', tc.__str__())

        tc = Timecode('59.94', frames=5178817)
        self.assertEqual('00:00:00;00', tc.__str__())

        tc = Timecode('25', 421729315)
        self.assertEqual('19:23:14:23', tc.__str__())

        tc = Timecode('29.97', 421729315)
        self.assertEqual('19:23:14;23', tc.__str__())
        self.assertTrue(tc.drop_frame)

    def test_start_seconds_argument_is_zero(self):
        """testing if a ValueError will be raised when the start_seconds
        parameters is zero.
        """
        with self.assertRaises(ValueError) as cm:
            Timecode('29.97', start_seconds=0)

        self.assertEqual(
            str(cm.exception),
            '``start_seconds`` argument can not be 0'
        )

    def test_frame_to_tc(self):
        tc = Timecode('29.97', '00:00:00;01')
        self.assertEqual(0, tc.hrs)
        self.assertEqual(0, tc.mins)
        self.assertEqual(0, tc.secs)
        self.assertEqual(1, tc.frs)
        self.assertEqual('00:00:00;01', tc.__str__())

        tc = Timecode('29.97', '03:36:09;23')
        self.assertEqual(3, tc.hrs)
        self.assertEqual(36, tc.mins)
        self.assertEqual(9, tc.secs)
        self.assertEqual(23, tc.frs)

        tc = Timecode('29.97', '03:36:09;23')
        self.assertEqual(3, tc.hrs)
        self.assertEqual(36, tc.mins)
        self.assertEqual(9, tc.secs)
        self.assertEqual(23, tc.frs)

        tc = Timecode('30', '03:36:09:23')
        self.assertEqual(3, tc.hrs)
        self.assertEqual(36, tc.mins)
        self.assertEqual(9, tc.secs)
        self.assertEqual(23, tc.frs)

        tc = Timecode('25', '03:36:09:23')
        self.assertEqual(3, tc.hrs)
        self.assertEqual(36, tc.mins)
        self.assertEqual(9, tc.secs)
        self.assertEqual(23, tc.frs)

        tc = Timecode('59.94', '03:36:09;23')
        self.assertEqual(3, tc.hrs)
        self.assertEqual(36, tc.mins)
        self.assertEqual(9, tc.secs)
        self.assertEqual(23, tc.frs)

        tc = Timecode('60', '03:36:09:23')
        self.assertEqual(3, tc.hrs)
        self.assertEqual(36, tc.mins)
        self.assertEqual(9, tc.secs)
        self.assertEqual(23, tc.frs)

        tc = Timecode('59.94', '03:36:09;23')
        self.assertEqual(3, tc.hrs)
        self.assertEqual(36, tc.mins)
        self.assertEqual(9, tc.secs)
        self.assertEqual(23, tc.frs)

        tc = Timecode('23.98', '03:36:09:23')
        self.assertEqual(3, tc.hrs)
        self.assertEqual(36, tc.mins)
        self.assertEqual(9, tc.secs)
        self.assertEqual(23, tc.frs)

        tc = Timecode('24', '03:36:09:23')
        self.assertEqual(3, tc.hrs)
        self.assertEqual(36, tc.mins)
        self.assertEqual(9, tc.secs)
        self.assertEqual(23, tc.frs)

        tc = Timecode('ms', '03:36:09.230')
        self.assertEqual(3, tc.hrs)
        self.assertEqual(36, tc.mins)
        self.assertEqual(9, tc.secs)
        self.assertEqual(230, tc.frs)

        tc = Timecode('24', frames=12000)
        self.assertEqual('00:08:19:23', tc.__str__())
        self.assertEqual(0, tc.hrs)
        self.assertEqual(8, tc.mins)
        self.assertEqual(19, tc.secs)
        self.assertEqual(23, tc.frs)

    def test_tc_to_frame_test_in_2997(self):
        """testing if timecode to frame conversion is ok in 2997
        """
        tc = Timecode('29.97', '00:00:00;00')
        self.assertEqual(tc._frames, 1)

        tc = Timecode('29.97', '00:00:00;21')
        self.assertEqual(tc._frames, 22)

        tc = Timecode('29.97', '00:00:00;29')
        self.assertEqual(tc._frames, 30)

        tc = Timecode('29.97', '00:00:00;60')
        self.assertEqual(tc._frames, 61)

        tc = Timecode('29.97', '00:00:01;00')
        self.assertEqual(tc._frames, 31)

        tc = Timecode('29.97', '00:00:10;00')
        self.assertEqual(tc._frames, 301)

        # test with non existing timecodes
        tc = Timecode('29.97', '00:01:00;00')
        self.assertEqual(1799, tc._frames)
        self.assertEqual('00:00:59;28', tc.__str__())

        # test the limit
        tc = Timecode('29.97', '23:59:59;29')
        self.assertEqual(2589408, tc._frames)

    def test_force_drop_frame_to_false(self):
        tc = Timecode('29.97', '01:00:00:00', force_non_drop_frame=True)
        self.assertEqual('00:59:56:12', tc.__repr__())

    def test_drop_frame(self):
        tc = Timecode('29.97', '13:36:59;29')
        timecode = tc.next()
        self.assertEqual("13:37:00;02", timecode.__str__())

        tc = Timecode('59.94', '13:36:59;59')
        self.assertEqual("13:36:59;59", tc.__str__())

        timecode = tc.next()
        self.assertEqual("13:37:00;04", timecode.__str__())

        tc = Timecode('59.94', '13:39:59;59')
        timecode = tc.next()
        self.assertEqual("13:40:00;00", timecode.__str__())

        tc = Timecode('29.97', '13:39:59;29')
        timecode = tc.next()
        self.assertEqual("13:40:00;00", timecode.__str__())

    def test_setting_frame_rate_to_2997_forces_drop_frame(self):
        """testing if setting the frame rate to 29.97 forces the dropframe to
        True
        """
        tc = Timecode('29.97')
        self.assertTrue(tc.drop_frame)

        tc = Timecode('29.97')
        self.assertTrue(tc.drop_frame)

    def test_setting_frame_rate_to_5994_forces_drop_frame(self):
        """testing if setting the frame rate to 59.94 forces the dropframe to
        True
        """
        tc = Timecode('59.94')
        self.assertTrue(tc.drop_frame)

        tc = Timecode('59.94')
        self.assertTrue(tc.drop_frame)

    def test_setting_frame_rate_to_ms_or_1000_forces_drop_frame(self):
        """testing if setting the frame rate to 59.94 forces the dropframe to
        True
        """
        tc = Timecode('ms')
        self.assertTrue(tc.ms_frame)

        tc = Timecode('1000')
        self.assertTrue(tc.ms_frame)

    def test_iteration(self):
        tc = Timecode('29.97', '03:36:09;23')
        assert tc == "03:36:09;23"

        for x in range(60):
            t = tc.next()
            self.assertTrue(t)

        assert t == "03:36:11;23"
        assert tc._frames == 388764

        # tc = Timecode('29.97', '03:36:09;23', force_drop_frame_to=False)
        # assert tc == '03:36:09;23'

        # for x in range(60):
        #     t = tc.next()
        #     self.assertTrue(t)

        # assert t == ''
        # assert tc.frames == 388764

        tc = Timecode('29.97', '03:36:09;23')
        for x in range(60):
            t = tc.next()
            self.assertTrue(t)
        assert t == "03:36:11;23"
        self.assertEqual(388764, tc._frames)

        tc = Timecode('30', '03:36:09:23')
        for x in range(60):
            t = tc.next()
            self.assertTrue(t)
        assert t == "03:36:11:23"
        self.assertEqual(389154, tc._frames)

        tc = Timecode('25', '03:36:09:23')
        for x in range(60):
            t = tc.next()
            self.assertTrue(t)
        assert t == "03:36:12:08"
        self.assertEqual(324309, tc._frames)

        tc = Timecode('59.94', '03:36:09;23')
        for x in range(60):
            t = tc.next()
            self.assertTrue(t)
        assert t == "03:36:10;23"
        self.assertEqual(777444, tc._frames)

        tc = Timecode('60', '03:36:09:23')
        for x in range(60):
            t = tc.next()
            self.assertTrue(t)
        assert t == "03:36:10:23"
        self.assertEqual(778224, tc._frames)

        tc = Timecode('59.94', '03:36:09:23')
        for x in range(60):
            t = tc.next()
            self.assertTrue(t)
        assert t == "03:36:10:23"
        self.assertEqual(777444, tc._frames)

        tc = Timecode('23.98', '03:36:09:23')
        for x in range(60):
            t = tc.next()
            self.assertTrue(t)
        assert t == "03:36:12:11"
        self.assertEqual(311340, tc._frames)

        tc = Timecode('24', '03:36:09:23')
        for x in range(60):
            t = tc.next()
            self.assertTrue(t)
        assert t == "03:36:12:11"
        self.assertEqual(311340, tc._frames)

        tc = Timecode('ms', '03:36:09.230')
        for x in range(60):
            t = tc.next()
            self.assertIsNotNone(t)
        assert t == '03:36:09.290'
        self.assertEqual(12969291, tc._frames)

        tc = Timecode('24', frames=12000)
        for x in range(60):
            t = tc.next()
            self.assertTrue(t)
        assert t == "00:08:22:11"
        self.assertEqual(12060, tc._frames)

    def test_op_overloads_add(self):
        tc = Timecode('29.97', '03:36:09;23')
        tc2 = Timecode('29.97', '00:00:29;23')
        d = tc + tc2
        f = tc + 894
        self.assertEqual("03:36:39;17", d.__str__())
        self.assertEqual(389598, d._frames)
        self.assertEqual("03:36:39;17", f.__str__())
        self.assertEqual(389598, f._frames)

        tc = Timecode('29.97', '03:36:09;23')
        tc2 = Timecode('29.97', '00:00:29;23')
        d = tc + tc2
        f = tc + 894
        self.assertEqual("03:36:39;17", d.__str__())
        self.assertEqual(389598, d._frames)
        self.assertEqual("03:36:39;17", f.__str__())
        self.assertEqual(389598, f._frames)

        tc = Timecode('30', '03:36:09:23')
        tc2 = Timecode('30', '00:00:29:23')
        d = tc + tc2
        f = tc + 894
        self.assertEqual("03:36:39:17", d.__str__())
        self.assertEqual(389988, d._frames)
        self.assertEqual("03:36:39:17", f.__str__())
        self.assertEqual(389988, f._frames)

        tc = Timecode('25', '03:36:09:23')
        tc2 = Timecode('25', '00:00:29:23')
        self.assertEqual(749, tc2._frames)
        d = tc + tc2
        f = tc + 749
        self.assertEqual("03:36:39:22", d.__str__())
        self.assertEqual(324998, d._frames)
        self.assertEqual("03:36:39:22", f.__str__())
        self.assertEqual(324998, f._frames)

        tc = Timecode('59.94', '03:36:09;23')
        tc2 = Timecode('59.94', '00:00:29;23')
        self.assertEqual(1764, tc2._frames)
        d = tc + tc2
        f = tc + 1764
        self.assertEqual("03:36:38;47", d.__str__())
        self.assertEqual(779148, d._frames)
        self.assertEqual("03:36:38;47", f.__str__())
        self.assertEqual(779148, f._frames)

        tc = Timecode('60', '03:36:09:23')
        tc2 = Timecode('60', '00:00:29:23')
        self.assertEqual(1764, tc2._frames)
        d = tc + tc2
        f = tc + 1764
        self.assertEqual("03:36:38:47", d.__str__())
        self.assertEqual(779928, d._frames)
        self.assertEqual("03:36:38:47", f.__str__())
        self.assertEqual(779928, f._frames)

        tc = Timecode('59.94', '03:36:09;23')
        tc2 = Timecode('59.94', '00:00:29;23')
        self.assertEqual(1764, tc2._frames)
        d = tc + tc2
        f = tc + 1764
        self.assertEqual("03:36:38;47", d.__str__())
        self.assertEqual(779148, d._frames)
        self.assertEqual("03:36:38;47", f.__str__())
        self.assertEqual(779148, f._frames)

        tc = Timecode('23.98', '03:36:09:23')
        tc2 = Timecode('23.98', '00:00:29:23')
        self.assertEqual(720, tc2._frames)
        d = tc + tc2
        f = tc + 720
        self.assertEqual("03:36:39:23", d.__str__())
        self.assertEqual(312000, d._frames)
        self.assertEqual("03:36:39:23", f.__str__())
        self.assertEqual(312000, f._frames)

        tc = Timecode('23.98', '03:36:09:23')
        tc2 = Timecode('23.98', '00:00:29:23')
        self.assertEqual(720, tc2._frames)
        d = tc + tc2
        f = tc + 720
        self.assertEqual("03:36:39:23", d.__str__())
        self.assertEqual(312000, d._frames)
        self.assertEqual("03:36:39:23", f.__str__())
        self.assertEqual(312000, f._frames)

        tc = Timecode('ms', '03:36:09.230')
        tc2 = Timecode('ms', '01:06:09.230')
        self.assertEqual(3969231, tc2._frames)
        d = tc + tc2
        f = tc + 720
        self.assertEqual("04:42:18.461", d.__str__())
        self.assertEqual(16938462, d._frames)
        self.assertEqual("03:36:09.950", f.__str__())
        self.assertEqual(12969951, f._frames)

        tc = Timecode('24', frames=12000)
        tc2 = Timecode('24', frames=485)
        self.assertEqual(485, tc2._frames)
        d = tc + tc2
        f = tc + 719
        self.assertEqual("00:08:40:04", d.__str__())
        self.assertEqual(12485, d._frames)
        self.assertEqual("00:08:49:22", f.__str__())
        self.assertEqual(12719, f._frames)

    def test_add_with_two_different_frame_rates(self):
        """testing if the resultant object will have the left sides frame rate
        when two timecodes with different frame rates are added together
        """
        tc1 = Timecode('29.97', '00:00:00;00')
        tc2 = Timecode('24', '00:00:00:10')
        tc3 = tc1 + tc2
        self.assertEqual('29.97', tc3.framerate)
        self.assertEqual(12, tc3._frames)
        assert tc3 == '00:00:00;11'

    def test_frame_number_attribute_value_is_correctly_calculated(self):
        """testing if the Timecode.frame_number attribute is correctly
        calculated
        """
        tc1 = Timecode('24', '00:00:00:00')
        self.assertEqual(1, tc1._frames)
        self.assertEqual(0, tc1.frame_number)

        tc2 = Timecode('24', '00:00:01:00')
        self.assertEqual(25, tc2._frames)
        self.assertEqual(24, tc2.frame_number)

        tc3 = Timecode('29.97', '00:01:00;00')
        self.assertEqual(1799, tc3._frames)
        self.assertEqual(1798, tc3.frame_number)

        tc4 = Timecode('30', '00:01:00:00')
        self.assertEqual(1801, tc4._frames)
        self.assertEqual(1800, tc4.frame_number)

        tc5 = Timecode('50', '00:01:00:00')
        self.assertEqual(3001, tc5._frames)
        self.assertEqual(3000, tc5.frame_number)

        tc6 = Timecode('59.94', '00:01:00;00')
        self.assertEqual(3597, tc6._frames)
        self.assertEqual(3596, tc6.frame_number)

        tc7 = Timecode('60', '00:01:00:00')
        self.assertEqual(3601, tc7._frames)
        self.assertEqual(3600, tc7.frame_number)

    def test_op_overloads_subtract(self):
        tc = Timecode('29.97', '03:36:09;23')
        tc2 = Timecode('29.97', '00:00:29;23')
        self.assertEqual(894, tc2._frames)
        d = tc - tc2
        f = tc - 894
        self.assertEqual("03:35:39;27", d.__str__())
        self.assertEqual(387810, d._frames)
        self.assertEqual("03:35:39;27", f.__str__())
        self.assertEqual(387810, f._frames)

        tc = Timecode('29.97', '03:36:09;23')
        tc2 = Timecode('29.97', '00:00:29;23')
        d = tc - tc2
        f = tc - 894
        self.assertEqual("03:35:39;27", d.__str__())
        self.assertEqual(387810, d._frames)
        self.assertEqual("03:35:39;27", f.__str__())
        self.assertEqual(387810, f._frames)

        tc = Timecode('30', '03:36:09:23')
        tc2 = Timecode('30', '00:00:29:23')
        d = tc - tc2
        f = tc - 894
        self.assertEqual("03:35:39:29", d.__str__())
        self.assertEqual(388200, d._frames)
        self.assertEqual("03:35:39:29", f.__str__())
        self.assertEqual(388200, f._frames)

        tc = Timecode('25', '03:36:09:23')
        tc2 = Timecode('25', '00:00:29:23')
        self.assertEqual(749, tc2._frames)
        d = tc - tc2
        f = tc - 749
        self.assertEqual("03:35:39:24", d.__str__())
        self.assertEqual(323500, d._frames)
        self.assertEqual("03:35:39:24", f.__str__())
        self.assertEqual(323500, f._frames)

        tc = Timecode('59.94', '03:36:09;23')
        tc2 = Timecode('59.94', '00:00:29;23')
        self.assertEqual(1764, tc2._frames)
        d = tc - tc2
        f = tc - 1764
        self.assertEqual("03:35:39;55", d.__str__())
        self.assertEqual(775620, d._frames)
        self.assertEqual("03:35:39;55", f.__str__())
        self.assertEqual(775620, f._frames)

        tc = Timecode('60', '03:36:09:23')
        tc2 = Timecode('60', '00:00:29:23')
        self.assertEqual(1764, tc2._frames)
        d = tc - tc2
        f = tc - 1764
        self.assertEqual("03:35:39:59", d.__str__())
        self.assertEqual(776400, d._frames)
        self.assertEqual("03:35:39:59", f.__str__())
        self.assertEqual(776400, f._frames)

        tc = Timecode('59.94', '03:36:09;23')
        tc2 = Timecode('59.94', '00:00:29;23')
        d = tc - tc2
        f = tc - 1764
        self.assertEqual("03:35:39;55", d.__str__())
        self.assertEqual(775620, d._frames)
        self.assertEqual("03:35:39;55", f.__str__())
        self.assertEqual(775620, f._frames)

        tc = Timecode('23.98', '03:36:09:23')
        tc2 = Timecode('23.98', '00:00:29:23')
        self.assertEqual(720, tc2._frames)
        d = tc - tc2
        f = tc - 720
        self.assertEqual("03:35:39:23", d.__str__())
        self.assertEqual(310560, d._frames)
        self.assertEqual("03:35:39:23", f.__str__())
        self.assertEqual(310560, f._frames)

        tc = Timecode('23.98', '03:36:09:23')
        tc2 = Timecode('23.98', '00:00:29:23')
        d = tc - tc2
        f = tc - 720
        self.assertEqual("03:35:39:23", d.__str__())
        self.assertEqual(310560, d._frames)
        self.assertEqual("03:35:39:23", f.__str__())
        self.assertEqual(310560, f._frames)

        tc = Timecode('ms', '03:36:09.230')
        tc2 = Timecode('ms', '01:06:09.230')
        self.assertEqual(3969231, tc2._frames)
        d = tc - tc2
        f = tc - 3969231
        self.assertEqual("02:29:59.999", d.__str__())
        self.assertEqual(9000000, d._frames)
        self.assertEqual("02:29:59.999", f.__str__())
        self.assertEqual(9000000, f._frames)

        tc = Timecode('24', frames=12000)
        tc2 = Timecode('24', frames=485)
        self.assertEqual(485, tc2._frames)
        d = tc - tc2
        f = tc - 485
        self.assertEqual("00:07:59:18", d.__str__())
        self.assertEqual(11515, d._frames)
        self.assertEqual("00:07:59:18", f.__str__())
        self.assertEqual(11515, f._frames)

    def test_op_overloads_mult(self):
        tc = Timecode('29.97', '00:00:09;23')
        tc2 = Timecode('29.97', '00:00:29;23')
        d = tc * tc2
        f = tc * 4
        self.assertEqual("02:26:09;29", d.__str__())
        self.assertEqual(262836, d._frames)
        self.assertEqual("00:00:39;05", f.__str__())
        self.assertEqual(1176, f._frames)

        tc = Timecode('29.97', '00:00:09;23')
        tc2 = Timecode('29.97', '00:00:29;23')
        d = tc * tc2
        f = tc * 4
        self.assertEqual("02:26:09;29", d.__str__())
        self.assertEqual(262836, d._frames)
        self.assertEqual("00:00:39;05", f.__str__())
        self.assertEqual(1176, f._frames)

        tc = Timecode('30', '03:36:09:23')
        tc2 = Timecode('30', '00:00:29:23')
        d = tc * tc2
        f = tc * 894
        self.assertEqual("04:50:01:05", d.__str__())
        self.assertEqual(347850036, d._frames)
        self.assertEqual("04:50:01:05", f.__str__())
        self.assertEqual(347850036, f._frames)

        tc = Timecode('25', '03:36:09:23')
        tc2 = Timecode('25', '00:00:29:23')
        self.assertEqual(749, tc2._frames)
        d = tc * tc2
        f = tc * 749
        self.assertEqual("10:28:20:00", d.__str__())
        self.assertEqual(242862501, d._frames)
        self.assertEqual("10:28:20:00", f.__str__())
        self.assertEqual(242862501, f._frames)

        tc = Timecode('59.94', '03:36:09;23')
        tc2 = Timecode('59.94', '00:00:29;23')
        self.assertEqual(1764, tc2._frames)
        d = tc * tc2
        f = tc * 1764
        self.assertEqual("18:59:27;35", d.__str__())
        self.assertEqual(1371305376, d._frames)
        self.assertEqual("18:59:27;35", f.__str__())
        self.assertEqual(1371305376, f._frames)

        tc = Timecode('60', '03:36:09:23')
        tc2 = Timecode('60', '00:00:29:23')
        self.assertEqual(1764, tc2._frames)
        d = tc * tc2
        f = tc * 1764
        self.assertEqual("19:00:21:35", d.__str__())
        self.assertEqual(1372681296, d._frames)
        self.assertEqual("19:00:21:35", f.__str__())
        self.assertEqual(1372681296, f._frames)

        tc = Timecode('59.94', '03:36:09;23')
        tc2 = Timecode('59.94', '00:00:29;23')
        d = tc * tc2
        f = tc * 1764
        self.assertEqual("18:59:27;35", d.__str__())
        self.assertEqual(1371305376, d._frames)
        self.assertEqual("18:59:27;35", f.__str__())
        self.assertEqual(1371305376, f._frames)

        tc = Timecode('23.98', '03:36:09:23')
        tc2 = Timecode('23.98', '00:00:29:23')
        self.assertEqual(tc._frames, 311280)
        self.assertEqual(tc2._frames, 720)
        d = tc * tc2
        f = tc * 720
        self.assertEqual(224121600, d._frames)
        self.assertEqual("01:59:59:23", d.__str__())
        self.assertEqual(224121600, f._frames)
        self.assertEqual("01:59:59:23", f.__str__())

        tc = Timecode('ms', '03:36:09.230')
        tc2 = Timecode('ms', '01:06:09.230')
        self.assertEqual(3969231, tc2._frames)
        d = tc * tc2
        f = tc * 3969231
        self.assertEqual("17:22:11.360", d.__str__())
        self.assertEqual(51477873731361, d._frames)
        self.assertEqual("17:22:11.360", f.__str__())
        self.assertEqual(51477873731361, f._frames)

        tc = Timecode('24', frames=12000)
        tc2 = Timecode('24', frames=485)
        self.assertEqual(485, tc2._frames)
        d = tc * tc2
        f = tc * 485
        self.assertEqual("19:21:39:23", d.__str__())
        self.assertEqual(5820000, d._frames)
        self.assertEqual("19:21:39:23", f.__str__())
        self.assertEqual(5820000, f._frames)

    def test_24_hour_limit_in_24fps(self):
        """testing if the timecode will loop back to 00:00:00:00 after 24 hours
        in 24 fps
        """
        tc = Timecode('24', '00:00:00:21')
        tc2 = Timecode('24', '23:59:59:23')
        self.assertEqual(
            '00:00:00:21',
            (tc + tc2).__str__()
        )
        self.assertEqual(
            '02:00:00:00',
            (tc2 + 159840001).__str__()
        )

    def test_24_hour_limit_in_2997fps(self):
        """testing if the timecode will loop back to 00:00:00:00 after 24 hours
        in 29.97 fps
        """
        tc = Timecode('29.97', '00:00:00;21')
        self.assertTrue(tc.drop_frame)
        self.assertEqual(22, tc._frames)

        tc2 = Timecode('29.97', '23:59:59;29')
        self.assertTrue(tc2.drop_frame)
        self.assertEqual(2589408, tc2._frames)

        self.assertEqual(
            '00:00:00;21',
            tc.__repr__()
        )
        self.assertEqual(
            '23:59:59;29',
            tc2.__repr__()
        )

        self.assertEqual(
            '00:00:00;21',
            (tc + tc2).__str__()
        )

        self.assertEqual(
            '02:00:00;00',
            (tc2 + 215785).__str__()
        )

        self.assertEqual(
            '02:00:00;00',
            (tc2 + 215785 + 2589408).__str__()
        )

        self.assertEqual(
            '02:00:00;00',
            (tc2 + 215785 + 2589408 + 2589408).__str__()
        )

    def test_24_hour_limit(self):
        """testing if the timecode will loop back to 00:00:00:00 after 24 hours
        in 29.97 fps
        """
        tc0 = Timecode('59.94', '23:59:59;29')
        self.assertEqual(5178786, tc0._frames)
        tc0 = Timecode('29.97', '23:59:59;29')
        self.assertEqual(2589408, tc0._frames)

        tc1 = Timecode('29.97', frames=2589408)
        self.assertEqual('23:59:59;29', tc1.__str__())

        tc2 = Timecode('29.97', '23:59:59;29')
        tc3 = tc2 + 1
        self.assertEqual('00:00:00;00', tc3.__str__())

        tc2 = Timecode('29.97', '23:59:59;29')
        tc3 = tc2 + 21
        self.assertEqual('00:00:00;20', tc3.__str__())

        tc = Timecode('29.97', '00:00:00;21')
        tc2 = Timecode('29.97', '23:59:59;29')
        tc3 = (tc + tc2)
        self.assertEqual('00:00:00;21', tc3.__str__())

        tc = Timecode('29.97', '04:20:13;21')
        tca = Timecode('29.97', frames=467944)
        self.assertEqual(467944, tca._frames)
        self.assertEqual(467944, tc._frames)
        self.assertEqual('04:20:13;21', tca.__str__())
        self.assertEqual('04:20:13;21', tc.__str__())

        tc2 = Timecode('29.97', '23:59:59;29')
        self.assertEqual(2589408, tc2._frames)
        self.assertEqual('23:59:59;29', tc2.__str__())
        tc2a = Timecode('29.97', frames=2589408)
        self.assertEqual(2589408, tc2a._frames)
        self.assertEqual('23:59:59;29', tc2a.__str__())

        tc3 = (tc + tc2)
        self.assertEqual('04:20:13;21', tc3.__str__())

        tc = Timecode('59.94', '04:20:13;21')
        self.assertEqual('04:20:13;21', tc.__str__())

        tca = Timecode('59.94', frames=935866)
        self.assertEqual('04:20:13;21', tca.__str__())

        tc2 = Timecode('59.94', '23:59:59;59')
        tc3 = (tc + tc2)
        self.assertEqual('04:20:13;21', tc3.__str__())

    def test_framerate_can_be_changed(self):
        """testing if the timecode value will be automatically updated when the
        framerate attribute is changed
        """
        tc1 = Timecode('25', frames=100)
        self.assertEqual('00:00:03:24', tc1.__str__())
        self.assertEqual(100, tc1._frames)

        tc1.framerate = '12'
        self.assertEqual('00:00:08:03', tc1.__str__())
        self.assertEqual(100, tc1._frames)

    def test_rational_framerate_conversions(self):
        tc = Timecode('24000/1000', '00:00:00:00')
        self.assertEqual(tc.framerate, '24')
        self.assertEqual(tc._int_framerate, 24)

        tc = Timecode('24000/1001', '00:00:00;00')
        self.assertEqual(tc.framerate, '24')
        self.assertEqual(tc._int_framerate, 24)

        tc = Timecode('30000/1000', '00:00:00:00')
        self.assertEqual(tc.framerate, '30')
        self.assertEqual(tc._int_framerate, 30)

        tc = Timecode('30000/1001', '00:00:00;00')
        self.assertEqual(tc.framerate, '29.97')
        self.assertEqual(tc._int_framerate, 30)

        tc = Timecode('60000/1000', '00:00:00:00')
        self.assertEqual(tc.framerate, '60')
        self.assertEqual(tc._int_framerate, 60)

        tc = Timecode('60000/1001', '00:00:00;00')
        self.assertEqual(tc.framerate, '59.94')
        self.assertEqual(tc._int_framerate, 60)

        tc = Timecode((60000, 1001), '00:00:00;00')
        self.assertEqual(tc.framerate, '59.94')
        self.assertEqual(tc._int_framerate, 60)

    def test_rational_frame_delimiter(self):
        tc = Timecode('24000/1000', frames=1)
        self.assertFalse(';' in tc.__repr__())

        tc = Timecode('24000/1001', frames=1)
        self.assertFalse(';' in tc.__repr__())

        tc = Timecode('30000/1001', frames=1)
        self.assertTrue(';' in tc.__repr__())

    def test_ms_vs_fraction_frames(self):
        tc1 = Timecode('ms', '00:00:00.040')
        self.assertTrue(tc1.ms_frame)
        self.assertFalse(tc1.fraction_frame)

        tc2 = Timecode(24, '00:00:00.042')
        self.assertTrue(tc2.fraction_frame)
        self.assertFalse(tc2.ms_frame)

        self.assertNotEqual(tc1, tc2)

        self.assertEqual(tc1.frame_number, 40)
        self.assertEqual(tc2.frame_number, 1)

    def test_toggle_fractional_frame(self):
        tc = Timecode(24, 421729315)
        self.assertEqual(tc.__repr__(), '19:23:14:23')

        tc.set_fractional(True)
        self.assertEqual(tc.__repr__(), '19:23:14.958')

        tc.set_fractional(False)
        self.assertEqual(tc.__repr__(), '19:23:14:23')

    def test_ge_overload(self):
        tc1 = Timecode(24, '00:00:00:00')
        tc2 = Timecode(24, '00:00:00:00')
        tc3 = Timecode(24, '00:00:00:01')
        tc4 = Timecode(24, '00:00:01.100')
        tc5 = Timecode(24, '00:00:01.200')

        self.assertTrue(tc1 == tc2)
        self.assertTrue(tc1 >= tc2)
        self.assertTrue(tc3 >= tc2)
        self.assertFalse(tc2 >= tc3)
        self.assertTrue(tc4 <= tc5)

    def test_gt_overload(self):
        tc1 = Timecode(24, '00:00:00:00')
        tc2 = Timecode(24, '00:00:00:00')
        tc3 = Timecode(24, '00:00:00:01')
        tc4 = Timecode(24, '00:00:01.100')
        tc5 = Timecode(24, '00:00:01.200')

        self.assertFalse(tc1 > tc2)
        self.assertFalse(tc2 > tc2)
        self.assertTrue(tc3 > tc2)
        self.assertTrue(tc5 > tc4)

    def test_le_overload(self):
        tc1 = Timecode(24, '00:00:00:00')
        tc2 = Timecode(24, '00:00:00:00')
        tc3 = Timecode(24, '00:00:00:01')
        tc4 = Timecode(24, '00:00:01.100')
        tc5 = Timecode(24, '00:00:01.200')

        self.assertTrue(tc1 == tc2)
        self.assertTrue(tc1 <= tc2)
        self.assertTrue(tc2 <= tc3)
        self.assertFalse(tc2 >= tc3)
        self.assertTrue(tc5 >= tc4)
        self.assertTrue(tc5 > tc4)

    def test_gt_overload(self):
        tc1 = Timecode(24, '00:00:00:00')
        tc2 = Timecode(24, '00:00:00:00')
        tc3 = Timecode(24, '00:00:00:01')
        tc4 = Timecode(24, '00:00:01.100')
        tc5 = Timecode(24, '00:00:01.200')

        self.assertFalse(tc1 < tc2)
        self.assertFalse(tc2 < tc2)
        self.assertTrue(tc2 < tc3)
        self.assertTrue(tc4 < tc5)

    def test_parse_timecode_with_int(self):
        """tests parse_timecode method with int input
        """
        result = Timecode.parse_timecode(16663)
        self.assertTrue(result == (0, 0, 41, 17))  # issue #16

    def test_frames_argument_is_not_an_int(self):
        """testing if a TypeError will be raised when the frames argument is
        not an integer
        """
        with self.assertRaises(TypeError) as cm:
            Timecode('30', frames=0.1223)

        self.assertEqual(
            "Timecode.frames should be a positive integer bigger than zero, not a float",
            str(cm.exception)
        )

    def test_frames_argument_is_zero(self):
        """testing if a ValueError will be raised when the frames argument is
        given as 0
        """
        with self.assertRaises(ValueError) as cm:
            Timecode('30', frames=0)

        self.assertEqual(
            "Timecode.frames should be a positive integer bigger than zero, not 0",
            str(cm.exception)
        )

    def test_bug_report_30(self):
        """testing bug report 30

        The claim on the bug report was to get ``00:34:45:09`` from a Timecode
        with 23.976 as the frame rate (supplied with Python 3's Fraction
        library) and 50000 as the total number of frames. The support for
        Fraction instances was missing and it has been added. But the claim for
        the resultant Timecode was wrong, the resultant Timecode should have
        been ``00:34:43:07`` and that has been approved by DaVinci Resolve.
        """
        from fractions import Fraction
        framerate = Fraction(24000, 1001)  # 23.976023976023978
        frame_idx = 50000

        tc1 = Timecode(framerate, frames=frame_idx)
        self.assertEqual(
            '00:34:43:07',
            tc1.__repr__()
        )

    def test_bug_report_31_part1(self):
        """testing bug report 31
        """
        timecode1 = '01:00:10:00'
        timecode2 = '01:00:10:00'
        timecode3 = '01:01:00:00'
        a = Timecode('25', timecode1)
        b = Timecode('25', timecode2)

        with self.assertRaises(ValueError) as cm:
            offset = a - b
            c = Timecode('25', timecode3) + offset

        self.assertEqual(
            str(cm.exception),
            "Timecode.frames should be a positive integer bigger than zero, not 0"
        )

    def test_bug_report_31_part2(self):
        """testing bug report 31
        """
        timecode1 = '01:00:08:00'
        timecode2 = '01:00:10:00'
        timecode3 = '01:01:00:00'
        a = Timecode('25', timecode1)
        b = Timecode('25', timecode2)
        offset = a - b
        c = Timecode('25', timecode3) + offset
