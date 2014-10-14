import unittest
from sqlalchemy.exc import InvalidRequestError

from flaq.models.user import User as UserApi
from flaq.models.user import Role
from flaq.utils import verify_password, make_password_hash

class UserRoleTest(unittest.TestCase):

    def setUp(self):
        """Initalize with dummy details"""

        self.username = 'testuser'
        self.email = 'testuser@gmail.com'
        self.password = 'testpassword'
        self.real_name = 'testusername'
        self.bio = 'userbio'
        self.website = 'test.com'

        self.user = UserApi(self.username)

    def tearDown(self):
        pass

    def test_11_create_user_roles(self):
        self.assertTrue(Role('user').create())
        self.assertTrue(Role.get('user'))
        self.assertTrue(Role.get(Role.get('user').id).id == Role.get('user').id)

        with self.assertRaises(ValueError):
            Role.get('banned')

        self.assertTrue(Role('banned').create().id is not None)


    def test_1_create_user(self):
        #Create user without password and email
        with self.assertRaises(ValueError):
            self.user.create()

        #Create user without password
        with self.assertRaises(ValueError):
            self.user.email = self.email
            self.user.create()

        #Create user with all required parameters(username, email, password)
        self.user.password = self.password
        self.user.email = self.email
        self.assertIsNotNone(self.user.create().id)

        #Create username which already exists
        with self.assertRaises(ValueError):
            self.user.create()

        #Delete a existing user record
        self.assertTrue(UserApi(self.username).delete())

        #Insert all other optional parameters and check the value
        self.user = UserApi(self.username)
        self.user.password = self.password
        self.user.email = self.email
        self.user.real_name = self.real_name
        self.user.bio = self.bio
        self.user.website = self.website
        self.assertTrue(self.user.create())

    def test_2_get_user(self):
        #Check invalid user
        with self.assertRaises(ValueError):
            UserApi.get(self.username+'_other')

        #Check details for user we just created
        user_a = UserApi.get(self.username)
        user_b = UserApi.get(self.email)

        #Check for user_a (get with username)
        self.assertTrue(user_a == user_b)

    def test_3_test_user_role(self):
        self.user = UserApi.get(self.username)
        self.assertTrue(self.user.role.title == 'user')

        self.user.role = 'banned'
        self.assertTrue(self.user.role.title == 'banned')
        self.assertTrue(UserApi.get(self.username).role.title == 'banned')

        with self.assertRaises(ValueError):
            self.user.role = 'mode'

    def test_4_edit_user(self):
        #Test edit for invalid user
        self.other_user = UserApi(self.username+'_other')
        with self.assertRaises(ValueError):
            self.other_user.edit()

        self.user = UserApi(self.username)

        #Edit profile without any optional parameters
        self.assertIsNone(self.user.edit())

        #Modify email and compare with new email
        self.assertTrue(
            self.user.edit(email=self.email+'_other').email == self.email+'_other')

        #modify real_name and check compare with real_name
        self.assertTrue(
            self.user.edit(real_name=self.real_name+'_other').\
                real_name == self.real_name+'_other')

        #Modify bio and compare with new bio
        self.assertTrue(
            self.user.edit(bio=self.bio+'_other').bio == self.bio+'_other')

        #Modify website and compare with new website
        self.assertTrue(
            self.user.edit(website=self.website+'_other').website == self.website+'_other')

        #Modify password and try recovering the new password
        self.assertTrue(verify_password(self.user.edit(
            password=self.password+'_other').password, self.password+'_other'
            ))

    def test_5_delete_user_role(self):
        #Delete a invalid user
        with self.assertRaises(ValueError):
            Role('mod').delete()

        self.assertTrue(Role('user').delete())
        self.assertTrue(Role('banned').delete())

    def test_5_user_delete(self):
        #Delete a invalid user
        with self.assertRaises(ValueError):
            UserApi(self.username+'_other').delete()

        #Delete the user we have created above
        self.assertTrue(UserApi(self.username).delete())


if __name__ == '__main__':
    unittest.main()