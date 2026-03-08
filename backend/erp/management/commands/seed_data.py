# backend/erp/management/commands/seed_data.py
import random
from django.core.management.base import BaseCommand
from django.db import transaction
from erp.factories import (
    CustomerFactory,
    ProductFactory,
    OrderFactory,
    InvoiceFactory,
    InvoiceEmbeddingFactory
)

class Command(BaseCommand):
    help = "Seed the database with realistic test data (transactional)"

    def add_arguments(self, parser):
        parser.add_argument('--customers', type=int, default=10)
        parser.add_argument('--products', type=int, default=20)
        parser.add_argument('--invoices', type=int, default=50)
        parser.add_argument('--orders', type=int, default=100)
        parser.add_argument('--embeddings', type=int, default=50)

    def handle(self, *args, **options):
        try:
            with transaction.atomic():  # ← tout est dans une transaction
                num_customers = options['customers']
                num_products = options['products']
                num_invoices = options['invoices']
                num_orders = options['orders']
                num_embeddings = options['embeddings']

                self.stdout.write(f"Creating {num_customers} customers...")
                customers = [CustomerFactory() for _ in range(num_customers)]

                self.stdout.write(f"Creating {num_products} products...")
                products = [ProductFactory() for _ in range(num_products)]

                self.stdout.write(f"Creating {num_orders} orders...")
                for _ in range(num_orders):
                    OrderFactory(product=random.choice(products))

                self.stdout.write(f"Creating {num_invoices} invoices...")
                invoices = [InvoiceFactory(customer=random.choice(customers)) for _ in range(num_invoices)]

                self.stdout.write(f"Creating {num_embeddings} invoice embeddings...")
                for invoice in random.sample(invoices, min(num_embeddings, len(invoices))):
                    InvoiceEmbeddingFactory(invoice=invoice)

            self.stdout.write(self.style.SUCCESS(
                f"Seeded {num_customers} customers, {num_products} products, "
                f"{num_orders} orders, {num_invoices} invoices, {num_embeddings} embeddings successfully!"
            ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Seeding failed: {e}"))
            raise  # rollback automatique