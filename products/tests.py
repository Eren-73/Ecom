from django.test import TestCase
<<<<<<< HEAD

# Create your tests here.
=======
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Product, Category, ProductImage
from accounts.models import VendorProfile
from PIL import Image
import io

class ProductFormTests(TestCase):

    def create_test_image(self, name='test.jpg', size=(100, 100), color=(255, 0, 0)):
        image = Image.new('RGB', size, color)
        byte_arr = io.BytesIO()
        image.save(byte_arr, format='JPEG')
        byte_arr.seek(0)
        return SimpleUploadedFile(name, byte_arr.read(), content_type='image/jpeg')

    def setUp(self):
        self.user = User.objects.create_user(username='vendor1', password='testpass')
        self.vendor = VendorProfile.objects.create(
            user=self.user,
            business_name='Shop1',
            description='Desc',
            phone='1234',
            address='Adresse',
            city='City'
        )
        self.category = Category.objects.create(name='Catégorie1', description='Une catégorie test')

        self.product = Product.objects.create(
            vendor=self.vendor,
            name='Produit1',
            description='Description produit',
            price=100,
            category=self.category,
            tags='tag1,tag2',
            stock_quantity=10,
            image=self.create_test_image('main.jpg')
        )

        self.additional_image = ProductImage.objects.create(
            product=self.product,
            image=self.create_test_image('additional1.jpg')
        )

        self.client.login(username='vendor1', password='testpass')

    def test_create_product_view(self):
        url = reverse('product_create')
        post_data = {
            'name': 'Produit2',
            'description': 'Desc produit 2',
            'price': '200',
            'category': self.category.id,
            'tags': 'tag3,tag4',
            'stock_quantity': '5',
            'is_active': True,
            'images-TOTAL_FORMS': '2',
            'images-INITIAL_FORMS': '0',
            'images-MIN_NUM_FORMS': '0',
            'images-MAX_NUM_FORMS': '5',
        }
        files_data = {
            'image': self.create_test_image('main_prod2.jpg'),
            'images-0-image': self.create_test_image('add1_prod2.jpg'),
            'images-1-image': self.create_test_image('add2_prod2.jpg'),
        }

        response = self.client.post(url, data=post_data, files=files_data, follow=True)
        self.assertEqual(response.status_code, 200)

        new_product = Product.objects.get(name='Produit2')
        self.assertEqual(new_product.additional_images.count(), 2)
        self.assertTrue(new_product.image)

    def test_edit_product_view(self):
        url = reverse('product_edit', kwargs={'pk': self.product.id})
        post_data = {
            'name': 'Produit1 modifié',
            'description': 'Desc modifiée',
            'price': '150',
            'category': self.category.id,
            'tags': 'tag1,tag2,tag3',
            'stock_quantity': '15',
            'images-TOTAL_FORMS': '2',
            'images-INITIAL_FORMS': '1',
            'images-MIN_NUM_FORMS': '0',
            'images-MAX_NUM_FORMS': '5',
            'images-0-id': str(self.additional_image.id),
        }
        files_data = {
            'image': self.create_test_image('main_updated.jpg'),
            'images-0-image': self.create_test_image('additional1_updated.jpg'),
            'images-1-image': self.create_test_image('add2_new.jpg'),
        }

        response = self.client.post(url, data=post_data, files=files_data, follow=True)
        self.assertEqual(response.status_code, 200)

        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Produit1 modifié')
        self.assertEqual(self.product.additional_images.count(), 2)
        self.assertTrue(self.product.image)
>>>>>>> feature/produits
