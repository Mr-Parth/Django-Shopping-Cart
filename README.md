
# Shopping Cart

This project provides a shopping cart system with user authentication, role-based access control, and various cart management and product item management functionalities. Built using Django and Django Rest Framework (DRF)


## Installation

1. Install Dependencies:

```bash
  pip install -r requirements.txt
```

2. Database Setup:

```bash
  python manage.py makemigrations
  python manage.py migrate
```

3. Create a Superuser (Admin):

```bash
  python manage.py createsuperuser
```

4. Run Development Server:

```bash
  python manage.py runserver
```

5. Testing

```bash
  python manage.py test
```

Access django admin panel at localhost:8000/admin
Database used : db.sqlite3 (Since it's easy to setup for development. It is a single compact file in a well-defined cross-platform format. For production environment, it is better to changed it to postgresql or other sql variants depending upon further usecases)

    
## API Implemented

### Public APIs

#### Login User
Returns JWT Token and User Data
```http
  POST /api/core/user/login
```

#### Register User
Returns JWT Token and Created User Data
```http
  POST /api/core/user/register
```

### Admin Role APIs

#### Suspend User
```http
  POST /api/core/user/suspend_user/<int:user_id>'
```

#### Add Product Item
```http
  POST /api/item/add_item/'
```

#### Add Product Items in Bulk
```http
  POST /api/item/add_items/'
```

#### Edit Product Item
```http
  PUT /api/item/edit_item/<int:item_id>'
```

#### Delete Product Item
```http
  DELETE /api/item/delete_item/<int:item_id>'
```

### Authorised APIs Irrespective of Role 

#### Add Product Item in User Cart
```http
  POST /api/user/cart/add_item/<str:product_name>'
```

#### Remove Product Item in User Cart
```http
  DELETE /api/user/cart/remove_item/<str:product_name>'
```

#### List Product Items in User Cart
```http
  GET /api/user/cart/list_items/'
```


## License

[MIT](https://choosealicense.com/licenses/mit/)

