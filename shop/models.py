from django.db import models
from users.models import BotUser

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class SubCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название подкатегории")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories", verbose_name="Категория")

    def __str__(self):
        return f"{self.category.name} → {self.name}"

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="products", verbose_name="Подкатегория")
    image = models.ImageField(upload_to="product_images/", verbose_name="Изображение товара")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

class Cart(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return f"{self.user.first_name} ({self.user.telegram_id}) - {self.product.name} ({self.quantity})"

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

class Order(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    products = models.ManyToManyField(Product, through="OrderItem", verbose_name="Товары")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    delivery_info = models.TextField(verbose_name="Данные доставки")

    def __str__(self):
        return f"Заказ {self.id} - {self.user.first_name} ({self.user.telegram_id})"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    def __str__(self):
        return f"{self.order.id}: {self.product.name} ({self.quantity})"

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказах"
