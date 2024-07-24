from django.test import TestCase

from members.models_user.profil_user import Setting_user


class UserCreationTestCase(TestCase):
    def setUp(self):

        self.user1 = Setting_user.objects.create(id = 1,username='user1', user_id = 11,
                                                 age = 22,floor = 'M',last_name='ФЫВа',sity = 'rostov',
                                                 about=')))',image = 'images_1.jpeg')
        self.user2 = Setting_user.objects.create(id = 2,username='user2', user_id = 12,
                                                 age = 27,floor = 'M',last_name='ФЫВа',sity = 'rostov',
                                                 about=')))',image = 'images_1.jpeg')
        self.user3 = Setting_user.objects.create(id = 3,username='user3', user_id = 13,
                                                 age = 21,floor = 'M',last_name='ФЫВа',sity = 'rostov',
                                                 about=')))',image = 'images_1.jpeg')

    def test_users_ordered_by_date_joined(self):

        users = Setting_user.objects.order_by('user_id')
        self.assertEqual(list(users), [self.user3, self.user2, self.user1])