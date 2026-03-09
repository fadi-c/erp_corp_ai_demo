sudo docker compose exec backend python manage.py makemigrations
sudo docker compose exec backend python manage.py migrate
sudo docker compose exec backend python manage.py seed_data --customers 20 --products 100 --orders 120 --invoices 40
