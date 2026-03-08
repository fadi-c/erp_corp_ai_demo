#!/bin/bash
set -e

# Upgrade pip et installer requirements
python -m pip install --upgrade pip
pip install -r requirements.txt

# Ajouter binaires de l'utilisateur au PATH
export PATH=$PATH:/home/django/.local/bin

# Exécuter la commande passée
exec "$@"