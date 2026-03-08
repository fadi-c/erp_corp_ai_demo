import random
import factory
from faker import Faker
from erp.models import Customer, Product, Order, Invoice, InvoiceEmbedding

fake = Faker()


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    name = factory.LazyAttribute(lambda _: fake.company())
    industry = factory.LazyAttribute(lambda _: fake.job())


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.LazyAttribute(lambda _: fake.word().capitalize())
    category = factory.LazyAttribute(lambda _: random.choice([
        "Electronics", "Industrial", "Furniture", "Software", "Services"
    ]))


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    product = factory.SubFactory(ProductFactory)
    quantity = factory.LazyAttribute(lambda _: random.randint(1, 100))
    price = factory.LazyAttribute(lambda _: round(random.uniform(10, 5000), 2))


class InvoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Invoice

    customer = factory.SubFactory(CustomerFactory)
    amount = factory.LazyAttribute(lambda _: round(random.uniform(1000, 50000), 2))
    margin = factory.LazyAttribute(lambda _: round(random.uniform(0.05, 0.3), 2))
    date = factory.LazyAttribute(lambda _: fake.date_between(start_date='-1y', end_date='today'))
    description = factory.LazyAttribute(lambda o: f"Invoice for {o.customer.name}")

