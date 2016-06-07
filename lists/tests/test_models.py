from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/{}/'.format(list_.id))


class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list1 = List.objects.create()
        item = Item(list=list1)
        item.save()
        self.assertIn(item, list1.item_set.all())

    def test_cannot_save_empty_list_item(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_cannot_save_duplicate_list_item(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='foobar')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='foobar')
            item.full_clean()

    def test_can_save_duplicate_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean() # should not raise
        item.save()
        self.assertEqual(Item.objects.count(), 2)

    def test_list_item_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text="item1")
        item2 = Item.objects.create(list=list1, text="item2")
        item3 = Item.objects.create(list=list1, text="item3")
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')
