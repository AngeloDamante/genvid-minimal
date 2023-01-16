from unittest import TestCase
import sys
sys.path.append("../")

class Test(TestCase):
    def test_check_exists_with_default_dir(self):
        from create_dataset import check_exists_with_default_dir
        existing_file = "test_file.txt"
        # check_exists_with_default_dir(existing_file, "jsndòivjdnfvidubn")
        # should be ok
