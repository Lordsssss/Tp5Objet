import unittest
from datetime import datetime
from ModuleTPSY import User  # Assuming the provided code is in `main_module.py`
import gestionnaireDB

class TestUser(unittest.TestCase):
    def test_user_creation(self):
        nfcid = "123456"
        username = "testUser"
        creationdate = datetime.now()
        description = "Test User Description"

        user = User(nfcid, username, creationdate, description)

        self.assertEqual(user.nfcid, nfcid)
        self.assertEqual(user.username, username)
        self.assertEqual(user.creationdate, creationdate)
        self.assertEqual(user.description, description)

    def test_user_repr(self):
        nfcid = "123456"
        username = "testUser"
        creationdate = datetime.now()
        description = "Test User Description"

        user = User(nfcid, username, creationdate, description)

        expected_repr = f"{username} - {nfcid} - {creationdate}"
        self.assertEqual(user.__repr__(), expected_repr)

    def test_user_listUserDisplay(self):
        nfcid = "123456"
        username = "testUser"
        creationdate = datetime.now()
        description = "Test User Description"

        user = User(nfcid, username, creationdate, description)

        self.assertEqual(user.listUserDiplay(), username)

if __name__ == "__main__":
    unittest.main()
