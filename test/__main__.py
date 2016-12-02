# coding=utf-8
import unittest
import mock
from PIL import Image
from atx.drivers.mixin import DeviceMixin
import atx
import function.steps as steps
from atx.drivers.ios_webdriveragent import IOSDevice


class TestFind(unittest.TestCase):
    def setUp(self):
        self.d = atx.connect('http://localhost:8100')
        self.d.image_path = ['.', '../function/steps/images']

    @mock.patch.object(DeviceMixin, '_cal_scale')
    @mock.patch.object(IOSDevice, 'screenshot')
    def test_in_explore_map(self, mock_screenshot, mock_mixin):
        mock_mixin.return_value = 1
        mock_screenshot.return_value = Image.open('images/explore_map.png')
        self.assertEqual(True, steps.in_explore_map(self.d))
        mock_screenshot.return_value = Image.open('images/blank.png')
        self.assertEqual(False, steps.in_explore_map(self.d))

    @mock.patch.object(DeviceMixin, '_cal_scale')
    @mock.patch.object(IOSDevice, 'screenshot')
    def test_is_fighting(self, mock_screenshot, mock_mixin):
        mock_mixin.return_value = 1
        mock_screenshot.return_value = Image.open('images/fighting.png')
        self.assertEqual(True, steps.is_fighting(self.d))
        mock_screenshot.return_value = Image.open('images/ready.png')
        self.assertEqual(True, steps.is_fighting(self.d))
        mock_screenshot.return_value = Image.open('images/blank.png')
        self.assertEqual(False, steps.is_fighting(self.d))

    @mock.patch.object(DeviceMixin, '_cal_scale')
    @mock.patch.object(IOSDevice, 'screenshot')
    def test_logged_in(self, mock_screenshot, mock_mixin):
        mock_mixin.return_value = 1
        mock_screenshot.return_value = Image.open('images/explore_map.png')
        self.assertEqual(True, steps.logged_in(self.d))

    @mock.patch.object(DeviceMixin, '_cal_scale')
    @mock.patch.object(IOSDevice, 'screenshot')
    def test_is_choosing(self, mock_screenshot, mock_mixin):
        mock_mixin.return_value = 1
        mock_screenshot.return_value = Image.open('images/switching.png')
        self.assertEqual(True, steps.is_choosing(self.d))
        mock_screenshot.return_value = Image.open('images/not_ready.png')
        self.assertEqual(False, steps.is_choosing(self.d))

    @mock.patch.object(DeviceMixin, '_cal_scale')
    @mock.patch.object(IOSDevice, 'screenshot')
    def test_is_not_ready(self, mock_screenshot, mock_mixin):
        mock_mixin.return_value = 1
        mock_screenshot.return_value = Image.open('images/not_ready.png')
        self.assertEqual(True, steps.is_not_ready(self.d))
        mock_screenshot.return_value = Image.open('images/switching.png')
        self.assertEqual(False, steps.is_not_ready(self.d))

    @mock.patch.object(DeviceMixin, '_cal_scale')
    @mock.patch.object(IOSDevice, 'screenshot')
    def test_is_shiju_found(self, mock_screenshot, mock_mixin):
        mock_mixin.return_value = 1
        mock_screenshot.return_value = Image.open('images/shi_ju.png')
        self.assertEqual(True, steps.is_shiju_found(self.d))
        mock_screenshot.return_value = Image.open('images/explore_map.png')
        self.assertEqual(False, steps.is_shiju_found(self.d))

    @mock.patch.object(DeviceMixin, '_cal_scale')
    @mock.patch.object(IOSDevice, 'screenshot')
    def test_success(self, mock_screenshot, mock_mixin):
        mock_mixin.return_value = 1
        mock_screenshot.return_value = Image.open('images/success.png')
        self.assertEqual(True, steps.success(self.d))
        mock_screenshot.return_value = Image.open('images/loss.png')
        self.assertEqual(False, steps.success(self.d))


if __name__ == '__main__':
    unittest.main()
