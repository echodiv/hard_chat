# TODO: https://www.internalpointers.com/post/run-painless-test-suites-python-unittest
from tests.test_forms import *
from tests.test_models.test_messages import *
from tests.test_models.test_posts import *
from tests.test_models.test_users import *
from tests.test_vievs import *
import unittest

if __name__ == '__main__':
    unittest.main()
