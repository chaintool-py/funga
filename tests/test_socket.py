# standard imports
import unittest
import logging

logg = logging.getLogger(__name__)


class SocketTest(unittest.TestCase):

    def test_placeholder_warning(self):
        logg.warning('socket tests are missing! :/')


if __name__ == '__main__':
    unittest.main()
