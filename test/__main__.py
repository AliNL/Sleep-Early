# coding=utf-8
import unittest
import mock
from PIL import Image
from atx.drivers.mixin import DeviceMixin
import atx
from function.steps import *
from atx.drivers.ios_webdriveragent import IOSDevice


class TestFind(unittest.TestCase):
    def setUp(self):
        self.d = atx.connect('http://localhost:8100')
        self.d.image_path = ['.', '../images']

    @mock.patch.object(DeviceMixin, '_cal_scale')
    @mock.patch.object(IOSDevice, 'screenshot')
    def test_in_explore_map(self, mock_screenshot, mock_mixin):
        mock_mixin.return_value = 1
        mock_screenshot.return_value = Image.open('images/explore_map.png')
        self.assertEqual(True, in_explore_map(self.d))
        mock_screenshot.return_value = Image.open('images/blank.png')
        self.assertEqual(False, in_explore_map(self.d))

    @mock.patch.object(DeviceMixin, '_cal_scale')
    @mock.patch.object(IOSDevice, 'screenshot')
    def test_is_fighting(self, mock_screenshot, mock_mixin):
        mock_mixin.return_value = 1
        mock_screenshot.return_value = Image.open('images/fighting.png')
        self.assertEqual(True, is_fighting(self.d))
        mock_screenshot.return_value = Image.open('images/blank.png')
        self.assertEqual(False, is_fighting(self.d))

    @mock.patch.object(DeviceMixin, '_cal_scale')
    @mock.patch.object(IOSDevice, 'screenshot')
    def test_is_not_ready(self, mock_screenshot, mock_mixin):
        mock_mixin.return_value = 1
        mock_screenshot.return_value = Image.open('images/not_ready.png')
        self.assertEqual(True, is_not_ready(self.d))
        mock_screenshot.return_value = Image.open('images/switching.png')
        self.assertEqual(False, is_not_ready(self.d))

if __name__ == '__main__':
    unittest.main()
