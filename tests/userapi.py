import unittest
from sqlalchemy.exc import InvalidRequestError

from flaq.lib.user.model import User as UserApi
from flaq.utils import verify_password, make_password_hash

class UserApiTest(unittest.TestCase):

    def setUp(self):
        """Initalize with dummy details"""

        self.username = 'testuser'
        self.email = 'testuser@gmail.com'
        self.password = 'testpassword'
        self.real_name = 'testusername'
        self.bio = 'userbio'
        self.website = 'test.com'

        self.other_username = 'testuser_1'
        self.other_email = 'testuser_1@gmail.com'
        self.other_password = 'testpassword_1'
        self.other_real_name = 'testusername_1'
        self.other_bio = 'userbio_1'
        self.other_website = 'test_1.com'

        self.invalid_username = 'invaliduser'
        self.invalid_email = 'invalid@abc.com'
        self.user = UserApi(self.username)

    def tearDown(self):
        pass

    def test_1_create_user(self):
        #Create user without username, password and email
        with self.assertRaises(ValueError):
            self.user.create()

        #Create user without email and password
        with self.assertRaises(ValueError):
            self.user.username = self.username
            self.user.create()

        #Create user without password
        with self.assertRaises(ValueError):
            self.user.username = self.username
            self.user.email = self.email
            self.user.create()

        #Create user with all required parameters(username, email, password)
        self.user.password = self.password
        self.user.username = self.username
        self.user.email = self.email
        self.assertTrue(self.user.create().username == self.username)

        #Create username which already exists
        with self.assertRaises(ValueError):
            self.user.username = self.username
            self.user.email = self.email
            self.user.create()

        #Delete a existing user record
        self.assertTrue(self.user.delete())

        #Insert all other optional parameters and check the value
        self.user.password = self.password
        self.user.username = self.username
        self.user.email = self.email
        self.user.real_name = self.real_name
        self.user.bio = self.bio
        self.user.website = self.website
        self.assertTrue(self.user.create())
'''
    def test_2_get_user(self):
        #Check invalid user
        with self.assertRaises(ValueError):
            self.user.get(self.other_username)

        #Check details for user we just created
        user_a = self.user.get(self.username)
        user_b = self.user.get(self.email)

        #Check for user_a (get with username)
        self.assertTrue(user_a.username == self.username)
        self.assertTrue(user_a.email == self.email)
        self.assertTrue(verify_password(user_a.password, self.password))
        self.assertTrue(user_a.real_name == self.real_name)
        self.assertTrue(user_a.website == self.website)
        self.assertTrue(user_a.bio == self.bio)

        #Check for user b (get with email)
        self.assertTrue(user_b.username == self.username)
        self.assertTrue(user_b.email == self.email)
        self.assertTrue(verify_password(user_b.password, self.password))
        self.assertTrue(user_b.real_name == self.real_name)
        self.assertTrue(user_b.website == self.website)
        self.assertTrue(user_b.bio == self.bio)

    def test_3_test_user_role(self):
        user = self.user.get(self.username)
        self.assertTrue(user.role == 'user')
        UserApi(self.username).role = 'mod'
        self.assertTrue(self.user.role(self.user.get(self.username).role == 'mod'))

    def test_4_edit_user(self):
        #Test edit for invalid user
        with self.assertRaises(ValueError):
            self.user.edit(self.other_username)

        #Edit profile without any optional parameters
        self.assertFalse(self.user.edit(self.username))

        #Try to change username of a existing user
        with self.assertRaises(TypeError):
            self.user.edit(self.username, username=self.other_username)

        #Modify email and compare with new email
        self.assertTrue(
            self.user.edit(self.username, email=self.other_email).email == self.other_email)

        #modify real_name and check compare with real_name
        self.assertTrue(
            self.user.edit(self.username, real_name=self.other_real_name).\
                real_name == self.other_real_name)

        #Modify bio and compare with new bio
        self.assertTrue(
            self.user.edit(self.username, bio=self.other_bio).bio == self.other_bio)

        #Modify website and compare with new website
        self.assertTrue(
            self.user.edit(self.username, website=self.other_website).website == self.other_website)

        #Modify password and try recovering the new password
        self.assertTrue(verify_password(self.user.edit(
            self.username, password=self.other_password).password, self.other_password
            ))

    def test_5_user_delete(self):
        #Delete a invalid user
        with self.assertRaises(ValueError):
            UserApi(self.other_username).delete()

        #Delete the user we have created above
        self.assertTrue(UserApi(self.username).delete())
'''
if __name__ == '__main__':
    unittest.main()