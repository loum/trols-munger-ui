import unittest2
import os
import tempfile

import trols_munger_ui
from filer.files import (remove_files,
                         get_directory_files_list,
                         move_file)


class TestLastUpdate(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.__shelve_dir = tempfile.mkdtemp()
        trols_munger_ui.app.config['SHELVE'] = cls.__shelve_dir
        cls.__app =  trols_munger_ui.app.test_client()

    def test_last_update(self):
        """Test the last update UTC timestamp.
        """
        # Given a shelve DB file
        shelve_db = os.path.join(self.__shelve_dir, 'trols_stats.db')
        file_obj = tempfile.NamedTemporaryFile(delete=False)
        filename = file_obj.name
        file_obj.close()
        move_file(filename, shelve_db)

        # and a know timestamp
        os.utime(shelve_db, (1440901349, 1440901349))

        # when I source the shelve's modfied time stamp
        response = self.__app.get('/_last_update')

        # then I should get a 200 response
        msg = 'Health _last_update response code'
        self.assertEqual(response.status_code, 200, msg)

        # and the UTC time should match
        received = response.data
        expected = '{\n  "last_update": "2015-08-30T02:22:29Z"\n}'
        msg = 'Last updated UTC time mis-match'
        self.assertEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        remove_files(get_directory_files_list(cls.__shelve_dir))
        os.removedirs(cls.__shelve_dir)
