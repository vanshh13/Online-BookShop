# 📚 Online BookShop

An online bookstore web application developed using Python and Django. This platform allows users to browse, search, and purchase books seamlessly.

## 🚀 Features

- **User Authentication**: Secure registration and login functionalities.
- **Book Catalog**: Browse through a diverse collection of books.
- **Search Functionality**: Easily search for books by title, author, or genre.
- **Shopping Cart**: Add books to a cart and manage purchases.
- **Admin Panel**: Manage inventory, orders, and user information.

## 🛠️ Technologies Used

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default Django database)
- **Others**: Bootstrap for responsive design

## 📂 Project Structure

```text
Online-BookShop/
├── Shop/             # Main Django application
├── book/             # App handling book-related functionalities
├── media/            # Directory for media files
├── static/           # Static files (CSS, JS, Images)
├── templates/        # HTML templates
├── db.sqlite3        # SQLite database
├── manage.py         # Django's command-line utility
└── README.md         # Project documentation
```


## ⚙️ Installation & Setup

Follow the steps below to set up and run the project on your local machine:

1. Clone the repository

```bash
git clone https://github.com/vanshh13/Online-BookShop.git
cd Online-BookShop
```
2. Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```
3. Create a superuser (for admin access)

```bash
python manage.py createsuperuser
```

4. Run the development server

```bash
python manage.py runserver
```

