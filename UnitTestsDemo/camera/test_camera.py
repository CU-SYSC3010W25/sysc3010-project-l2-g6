import unittest
from unittest.mock import patch, MagicMock
from src import Camera

class TestCamera(unittest.TestCase):

    def setUp(self):
        self.camera = Camera()

    @patch('camera.Camera.startStream')
    def test_start_stream(self, mock_start_stream):
        # Test the startStream method
        self.camera.startStream()
        mock_start_stream.assert_called_once()

    @patch('camera.Camera.stopCamera')
    def test_stop_camera(self, mock_stop_camera):
        # Test the stopCamera method
        self.camera.stopCamera()
        mock_stop_camera.assert_called_once()

    @patch('camera.Camera.settingsListen')
    def test_settings_listen(self, mock_settings_listen):
        # Test the settingsListen method
        self.camera.settingsListen()
        mock_settings_listen.assert_called_once()

if __name__ == '__main__':
    unittest.main()