# EcomApp

EcomApp is a Django-based e-commerce application. It provides a product
catalog, product search, a session-based shopping cart, user accounts, and
product reviews.

## Features

- Browse products and view product details, stock, and customer reviews.
- Search the product catalog.
- Add products to a cart, change quantities, and remove items.
- Register, sign in, and manage an account.
- Leave or update a product review while signed in.
- Manage products through the Django admin site.

## Requirements

- Python
- pip

The application uses Django and Pillow (for product image support).

## Run locally

From the repository root, create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows, activate it with:

```powershell
.venv\Scripts\Activate.ps1
```

Install the application dependencies and enter the directory containing
`manage.py`:

```bash
python -m pip install Django Pillow
cd EcomApp
```

Apply database migrations and start the development server:

```bash
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in a browser. To manage the catalog, create an
administrator account and visit <http://127.0.0.1:8000/admin/>:

```bash
python manage.py createsuperuser
```

The current `ALLOWED_HOSTS` setting is configured for an ngrok hostname. For
local browsing, add `localhost` and `127.0.0.1` to `ALLOWED_HOSTS` in
`EcomApp/settings.py`, preserving any hosts you still need.

## Tests

Run the Django test suite from the directory containing `manage.py`:

```bash
python manage.py test
```

## Development note

The included Django settings are for development, not production. Before
deployment, configure a secure secret key, disable debug mode, and set
appropriate allowed hosts and production database settings.
