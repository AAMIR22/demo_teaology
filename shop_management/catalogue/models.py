from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name if self.name else "Anonymous"

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Cart {self.id} for {self.customer if self.customer else 'Anonymous'}"

    def total_price(self):
        total = sum(item.quantity * item.product.price for item in self.items.all())
        return total - self.discount

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


    def total_price(self):
        return self.quantity * self.product.price
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the total price of the cart after saving the item
        self.cart.save()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Sale(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = self.cart.total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale {self.id}"

    class Meta:
        ordering = ['-date']  # Orders by date in descending order
