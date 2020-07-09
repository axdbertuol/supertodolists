from django.test import TestCase
from ..models import Item, List
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your tests here.


class ItemModelTest(TestCase):

	def test_default_text(self):
		item = Item()
		self.assertEqual(item.text, '')

	def test_item_is_related_to_list(self):
		list_ = List.objects.create()
		item = Item()
		item.list = list_
		item.save()
		self.assertIn(item, list_.item_set.all())

	def test_cannot_save_empty_list_items(self):
		list_ = List.objects.create()
		item = Item(list=list_, text='')
		with self.assertRaises(ValidationError):
			item.save()
			item.full_clean()

	def test_duplicate_items_are_invalid(self):
		list_ = List.objects.create()
		Item.objects.create(list=list_, text='bla')
		with self.assertRaises(ValidationError):
			item = Item(list=list_, text='bla')
			# This method will validate all fields on your model
			item.full_clean()

	def test_CAN_save_same_item_to_different_lists(self):
		list1 = List.objects.create()
		list2 = List.objects.create()
		Item.objects.create(list=list1, text='bla')
		item = Item(list=list2, text='bla')
		item.full_clean()  # should not raise

	def test_list_ordering(self):
		list1 = List.objects.create()
		item1 = Item.objects.create(list=list1, text='bla')
		item2 = Item.objects.create(list=list1, text='ba')
		item3 = Item.objects.create(list=list1, text='bl')
		self.assertEqual(
			list(Item.objects.all()),
			[item1, item2, item3]
		)

	def test_string_representation(self):
		item = Item(text='some text')
		self.assertEqual(str(item), 'some text')


class ListModelTest(TestCase):
	def test_get_absolute_url(self):
		list_ = List.objects.create()
		self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

	def test_create_new_function_creates_list_and_first_item(self):
		List.create_new(first_item_text='new item text')
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'new item text')
		new_list = List.objects.first()
		self.assertEqual(new_item.list, new_list)

	def test_create_new_optionally_saves_owner(self):
		user = User.objects.create()
		List.create_new(first_item_text='new item text', owner=user)
		new_list = List.objects.first()
		self.assertEqual(new_list.owner, user)

	def test_lists_can_have_owners(self):
		List(owner=User())  # should not raise

	def test_list_owner_is_optional(self):
		List().full_clean()  # should not raise

	def test_create_returns_new_list_object(self):
		returned = List.create_new(first_item_text='new item text')
		new_list = List.objects.first()
		self.assertEqual(returned, new_list)

	def test_lists_can_have_owners(self):
		user = User.objects.create(email='a@b.com')
		list_ = List.objects.create(owner=user)
		self.assertIn(list_, user.list_set.all())

	def test_list_owner_is_optional(self):
		List.objects.create()  # should not raise

	def test_list_name_is_first_item_text(self):
		list_ = List.objects.create()
		Item.objects.create(list=list_, text='first item')
		Item.objects.create(list=list_, text='second item')
		self.assertEqual(list_.name, 'first item')

	def test_list_has_shared_with_attr(self):
		user = User.objects.create(email='a@b.com')
		user2 = User.objects.create(email='c@d.com')
		lista = List.create_new(first_item_text='oie', owner=user)
		lista.shared_with.add(user2)
		# print(lista._meta.fields)
		# print(f'Sharees: {lista.shared_with.all()}')
		self.assertIn(user2, lista.shared_with.all())

	def test_list_cannot_add_own_user_to_shared_with_attr(self):
		user = User.objects.create_user(email='a@b.com', password='alocporra')
		# user2 = User.objects.create(email='c@d.com')
		lista = List.create_new(first_item_text='oie', owner=user)
		# print('Pre-add')
		lista.shared_with.add(user)
		# print('Post-add')
		# print(lista._meta.fields)
		# print(f'Sharees: {lista.shared_with.all()}')
		self.assertNotIn(user, lista.shared_with.all())

