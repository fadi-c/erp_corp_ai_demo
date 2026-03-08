from django.db import models
from pgvector.django import VectorField


class Customer(models.Model):

    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Order(models.Model):
    invoice = models.ForeignKey("Invoice", on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.FloatField()
    margin = models.FloatField()
    date = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Invoice {self.id}"


class InvoiceEmbedding(models.Model):

    invoice = models.OneToOneField(
        Invoice, on_delete=models.CASCADE, related_name="embedding"
    )

    embedding = VectorField(
        dimensions=1536  # embeddings OpenAI text-embedding-3-small = 1536
    )

    created_at = models.DateTimeField(auto_now_add=True)
