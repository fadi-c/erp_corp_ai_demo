
import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.db import transaction
from erp.factories import CustomerFactory, ProductFactory, OrderFactory, InvoiceFactory
from erp.models import InvoiceEmbedding
from ai.embeddings.factory import EmbeddingFactory

fake = Faker()

class Command(BaseCommand):
    help = "Seed database with realistic ERP data and real embeddings via EmbeddingFactory"

    def add_arguments(self, parser):
        parser.add_argument('--customers', type=int, default=100)
        parser.add_argument('--products', type=int, default=50)
        parser.add_argument('--orders', type=int, default=2000)
        parser.add_argument('--invoices', type=int, default=1000)

    def handle(self, *args, **options):
        embedding_service = EmbeddingFactory.get_embedding_service()
        try:
            with transaction.atomic():
                customers = []
                customer_trends = {}
                for _ in range(options['customers']):
                    customer = CustomerFactory()
                    trend = random.uniform(-0.05, 0.05)
                    customer_trends[customer.id] = trend
                    customers.append(customer)
                self.stdout.write(f"Created {len(customers)} customers with trends.")

                products = []
                product_prices = {}
                for _ in range(options['products']):
                    product = ProductFactory()
                    base_price = random.uniform(100, 5000)
                    product_prices[product.id] = base_price
                    products.append(product)
                self.stdout.write(f"Created {len(products)} products with base prices.")

                for _ in range(options['orders']):
                    product = random.choice(products)
                    OrderFactory(
                        product=product,
                        quantity=random.randint(1, 50),
                        price=round(random.gauss(product_prices[product.id], 50), 2)
                    )
                self.stdout.write(f"Created {options['orders']} orders.")

                invoices = []
                for _ in range(options['invoices']):
                    customer = random.choice(customers)
                    product = random.choice(products)
                    quantity = random.randint(1, 50)
                    base_amount = product_prices[product.id] * quantity
                    margin = round(random.uniform(0.05, 0.3) + customer_trends[customer.id], 2)
                    margin = max(0.01, min(margin, 0.5))
                    amount = round(base_amount * (1 + random.uniform(-0.1, 0.1)), 2)
                    date = fake.date_between(start_date='-2y', end_date='today')
                    description = (
                        f"Invoice for {customer.name}: {quantity} x {product.name} "
                        f"({product.category}), Amount: {amount}, Margin: {margin}"
                    )
                    invoice = InvoiceFactory(
                        customer=customer,
                        amount=amount,
                        margin=margin,
                        date=date,
                        description=description
                    )
                    invoices.append(invoice)
                self.stdout.write(f"Created {len(invoices)} invoices.")

                for invoice in invoices:
                    text = f"""
                    Invoice description: {invoice.description}
                    Amount: {invoice.amount}
                    Margin: {invoice.margin}
                    Date: {invoice.date}
                    """
                    vector = embedding_service.generate(text)
                    InvoiceEmbedding.objects.update_or_create(
                        invoice=invoice,
                        defaults={"embedding": vector}
                    )
                self.stdout.write(self.style.SUCCESS(
                    f"Seeded {len(customers)} customers, {len(products)} products, "
                    f"{options['orders']} orders, {len(invoices)} invoices with real embeddings!"
                ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Seeding failed: {e}"))
            raise