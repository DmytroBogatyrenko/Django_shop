
from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Product

# Create your tests here.


class CategoryModelTest(TestCase):

    def setUp(self):
        self.root = Category.objects.create(name='Зброя')
        self.child = Category.objects.create(name='Мечі', parent=self.root)

    def test_str_shows_name(self):
        self.assertEqual(str(self.root), 'Зброя')

    def test_is_root_returns_true_for_root(self):
        self.assertTrue(self.root.is_root())

    def test_is_root_returns_false_for_child(self):
        self.assertFalse(self.child.is_root())

    def test_get_children_returns_subcategories(self):
        children = list(self.root.get_children())
        self.assertIn(self.child, children)

    def test_get_absolute_url(self):
        url = self.root.get_absolute_url()
        self.assertIn(str(self.root.id), url)


class ProductModelTest(TestCase):

    def setUp(self):
        category = Category.objects.create(name='Артефакти')
        self.product = Product.objects.create(
            name='Кристал Долі',
            category=category,
            price='999.00',
            slug='krystal-doli',
        )

    def test_str_shows_name(self):
        self.assertEqual(str(self.product), 'Кристал Долі')

    def test_get_absolute_url(self):
        url = self.product.get_absolute_url()
        self.assertIn(self.product.slug, url)


class ProductListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        category = Category.objects.create(name='Реліквії')
        Product.objects.create(
            name='Амулет Ордену', category=category,
            price='500.00', slug='amulet-ordenu',
        )

    def test_catalog_returns_200(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)

    def test_catalog_uses_correct_template(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertTemplateUsed(response, 'shop/product_list.html')

    def test_catalog_shows_products(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertContains(response, 'Амулет Ордену')

    def test_search_finds_product(self):
        response = self.client.get(reverse('shop:product_list'), {'q': 'Амулет'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Амулет Ордену')

    def test_search_returns_empty_for_unknown(self):
        response = self.client.get(reverse('shop:product_list'), {'q': 'xxxxxx'})
        self.assertEqual(response.status_code, 200)


class ProductDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        category = Category.objects.create(name='Сувої')
        self.product = Product.objects.create(
            name='Карта Забутих Земель', category=category,
            price='1200.00', slug='karta-zabutykh-zemel',
        )

    def test_product_detail_returns_200(self):
        url = reverse('shop:product_detail', args=[self.product.id, self.product.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_detail_shows_name_and_price(self):
        url = reverse('shop:product_detail', args=[self.product.id, self.product.slug])
        response = self.client.get(url)
        self.assertContains(response, 'Карта Забутих Земель')
        self.assertContains(response, '1200')

    def test_wrong_slug_returns_404(self):
        url = reverse('shop:product_detail', args=[self.product.id, 'nepravylnyi-slug'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
