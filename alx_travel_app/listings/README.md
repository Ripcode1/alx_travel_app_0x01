# ALX Travel App - API Development for Listings and Bookings

A Django REST Framework-based travel booking platform API with comprehensive CRUD operations for property listings and bookings.

## 🚀 Features

- **Property Listings Management**: Full CRUD operations for property listings
- **Booking System**: Complete booking management with status tracking
- **RESTful API Design**: Following REST best practices
- **Interactive API Documentation**: Auto-generated Swagger/OpenAPI documentation
- **Advanced Filtering**: Search, filter, and sort listings and bookings
- **Authentication**: Session and Basic authentication support
- **PostgreSQL/SQLite Support**: Flexible database configuration

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)
- PostgreSQL (optional, SQLite by default)

### Setup Instructions

1. **Clone the repository**
```bash
git clone <repository-url>
cd alx_travel_app_0x01/alx_travel_app
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create a superuser**
```bash
python manage.py createsuperuser
```

6. **Run the development server**
```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## 🔌 API Endpoints

### Listings Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/listings/` | List all listings | Optional |
| POST | `/api/listings/` | Create a new listing | Required |
| GET | `/api/listings/{id}/` | Get a specific listing | Optional |
| PUT | `/api/listings/{id}/` | Update a listing | Required |
| PATCH | `/api/listings/{id}/` | Partial update a listing | Required |
| DELETE | `/api/listings/{id}/` | Delete a listing | Required |
| GET | `/api/listings/my_listings/` | Get current user's listings | Required |
| GET | `/api/listings/available/` | Get available listings | Optional |
| POST | `/api/listings/{id}/toggle_availability/` | Toggle availability | Required |

### Bookings Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/bookings/` | List user's bookings | Required |
| POST | `/api/bookings/` | Create a new booking | Required |
| GET | `/api/bookings/{id}/` | Get a specific booking | Required |
| PUT | `/api/bookings/{id}/` | Update a booking | Required |
| PATCH | `/api/bookings/{id}/` | Partial update a booking | Required |
| DELETE | `/api/bookings/{id}/` | Delete a booking | Required |
| GET | `/api/bookings/my_bookings/` | Get user's bookings | Required |
| GET | `/api/bookings/my_property_bookings/` | Get bookings for user's properties | Required |
| GET | `/api/bookings/upcoming/` | Get upcoming bookings | Required |
| POST | `/api/bookings/{id}/confirm/` | Confirm a booking (host only) | Required |
| POST | `/api/bookings/{id}/cancel/` | Cancel a booking | Required |

## 📚 API Documentation

### Swagger UI
Access interactive API documentation at: `http://127.0.0.1:8000/swagger/`

### ReDoc
Alternative documentation interface: `http://127.0.0.1:8000/redoc/`

### OpenAPI Schema
Download the API schema:
- JSON: `http://127.0.0.1:8000/swagger.json`
- YAML: `http://127.0.0.1:8000/swagger.yaml`

## 🧪 Testing with Postman

### Setup
1. Import `ALX_Travel_App_Postman_Collection.json` into Postman
2. Set environment variable: `base_url = http://127.0.0.1:8000`
3. Use Basic Auth or Session Auth for protected endpoints

### Sample API Calls

#### Create a Listing
```http
POST /api/listings/
Content-Type: application/json
Authorization: Basic <credentials>

{
  "title": "Cozy Apartment in Paris",
  "description": "Beautiful apartment in the heart of Paris",
  "location": "Paris, France",
  "price_per_night": 120.00,
  "property_type": "apartment",
  "number_of_guests": 4,
  "number_of_bedrooms": 2,
  "number_of_bathrooms": 1,
  "amenities": "WiFi, Kitchen, Air Conditioning",
  "available": true,
  "host_id": 1
}
```

**Response:** `201 Created`

#### Get All Listings
```http
GET /api/listings/
```

**Response:** `200 OK` with paginated results

#### Create a Booking
```http
POST /api/bookings/
Content-Type: application/json
Authorization: Basic <credentials>

{
  "listing_id": 1,
  "user_id": 2,
  "check_in_date": "2025-12-15",
  "check_out_date": "2025-12-20",
  "number_of_guests": 2
}
```

**Response:** `201 Created` with auto-calculated `total_price`

#### Confirm a Booking (Host Only)
```http
POST /api/bookings/1/confirm/
Authorization: Basic <credentials>
```

**Response:** `200 OK` with status changed to "confirmed"

#### Filter Listings
```http
GET /api/listings/?location=Paris&min_price=50&max_price=200&available=true
```

**Response:** `200 OK` with filtered results

#### Update a Listing
```http
PATCH /api/listings/1/
Content-Type: application/json
Authorization: Basic <credentials>

{
  "price_per_night": 150.00
}
```

**Response:** `200 OK` with updated listing

#### Delete a Listing
```http
DELETE /api/listings/1/
Authorization: Basic <credentials>
```

**Response:** `204 No Content`

## 📁 Project Structure

```
alx_travel_app_0x01/
└── alx_travel_app/
    ├── manage.py
    ├── requirements.txt
    ├── README.md
    ├── ALX_Travel_App_Postman_Collection.json
    ├── alx_travel_app/
    │   ├── __init__.py
    │   ├── settings.py          # Django settings with DRF & Swagger config
    │   ├── urls.py              # Main URL configuration with Swagger
    │   ├── wsgi.py
    │   └── asgi.py
    └── listings/
        ├── __init__.py
        ├── models.py            # Listing and Booking models
        ├── serializers.py       # DRF serializers with validation
        ├── views.py             # ViewSets for CRUD operations
        ├── urls.py              # Router configuration
        ├── admin.py             # Django admin interface
        └── apps.py              # App configuration
```

## 📊 Models

### Listing Model
- `title`: Property title
- `description`: Detailed description
- `location`: Property location
- `price_per_night`: Nightly rate (Decimal)
- `property_type`: Type (apartment, house, villa, condo, cabin)
- `number_of_guests`: Maximum guests
- `number_of_bedrooms`: Number of bedrooms
- `number_of_bathrooms`: Number of bathrooms
- `amenities`: Comma-separated amenities
- `available`: Availability status (Boolean)
- `host`: Foreign key to User
- `created_at`: Auto timestamp
- `updated_at`: Auto timestamp

### Booking Model
- `listing`: Foreign key to Listing
- `user`: Foreign key to User
- `check_in_date`: Check-in date
- `check_out_date`: Check-out date
- `number_of_guests`: Number of guests
- `total_price`: Auto-calculated total price
- `status`: Booking status (pending, confirmed, cancelled, completed)
- `created_at`: Auto timestamp
- `updated_at`: Auto timestamp

## 🔐 Authentication

The API supports two authentication methods:

### 1. Session Authentication
Login via `/api-auth/login/` for session-based auth

### 2. Basic Authentication
Include Basic Auth headers in your requests:
```
Authorization: Basic <base64-encoded-credentials>
```

## 🎯 Key Features

### ViewSets
Uses Django REST Framework's `ModelViewSet` for efficient CRUD operations:
- `ListingViewSet`: Manages all listing operations
- `BookingViewSet`: Manages all booking operations

### Router Configuration
Automatic URL routing using `DefaultRouter`:
```python
router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')
```

### Custom Actions
Additional endpoints using `@action` decorator:
- `/api/listings/my_listings/` - Get user's listings
- `/api/listings/available/` - Get available listings
- `/api/bookings/my_bookings/` - Get user's bookings
- `/api/bookings/upcoming/` - Get upcoming bookings
- `/api/bookings/{id}/confirm/` - Confirm booking
- `/api/bookings/{id}/cancel/` - Cancel booking

### Filtering & Search
- **Search**: Full-text search across title, description, and location
- **Filters**: Filter by property_type, location, available, status
- **Ordering**: Sort by price, date, guests
- **Custom Filters**: min_price, max_price, guests

### Validation
- Price must be positive
- Check-out date must be after check-in date
- Check-in date cannot be in the past
- Number of guests cannot exceed listing capacity
- Automatic price calculation based on nights

### Permissions
- Read operations: Open to all (listings only)
- Create/Update/Delete: Authenticated users only
- Host-only actions: Toggle availability, confirm bookings
- User-specific: Can only see own bookings

## 📝 Query Parameters

### Listings
- `search=<query>` - Search in title, description, location
- `property_type=<type>` - Filter by type
- `location=<location>` - Filter by location
- `available=<true|false>` - Filter by availability
- `min_price=<price>` - Minimum price
- `max_price=<price>` - Maximum price
- `guests=<number>` - Minimum guests capacity
- `ordering=<field>` - Sort (use `-` for descending)

### Bookings
- `status=<status>` - Filter by status
- `listing=<id>` - Filter by listing
- `ordering=<field>` - Sort by field

## 🧪 Running Tests

```bash
python manage.py test
```

## 📝 Additional Commands

**Create migrations:**
```bash
python manage.py makemigrations
```

**Apply migrations:**
```bash
python manage.py migrate
```

**Create superuser:**
```bash
python manage.py createsuperuser
```

**Collect static files:**
```bash
python manage.py collectstatic
```

**Access Django Admin:**
```
http://127.0.0.1:8000/admin/
```

## 🌐 Database Configuration

### SQLite (Default)
Already configured in `settings.py`

### PostgreSQL (Optional)
1. Install PostgreSQL
2. Create a database
3. Update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'alx_travel_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## ✨ REST Framework Configuration

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

## 🎓 Learning Objectives Achieved

✅ Implemented ViewSets in Django REST Framework  
✅ Configured API routes using DRF's routers  
✅ Applied RESTful conventions in API endpoint design  
✅ Documented APIs with Swagger for interactive exploration  
✅ Tested API endpoints with Postman  
✅ Created and managed CRUD endpoints for multiple models  
✅ Integrated automatic API documentation  
✅ Deployed well-structured and tested API endpoints  

## 🚀 Real-World Use Case

This project mirrors backend development for travel booking platforms like:
- Airbnb
- Booking.com
- Expedia
- VRBO

Key implementations:
- Property listing management
- Booking request handling
- User authentication
- Status tracking
- Price calculation
- Availability management

## 📞 Support

For issues or questions:
1. Check the Swagger documentation at `/swagger/`
2. Review the Postman collection
3. Check Django server logs for errors
4. Verify all dependencies are installed
5. Ensure migrations are applied

## 📄 License

This project is part of the ALX Software Engineering program.

---

**Project Status:** ✅ Complete and Ready for Submission

**Repository:** alx_travel_app_0x01  
**Directory:** alx_travel_app  
**Required Files:** ✅ listings/views.py, ✅ listings/urls.py, ✅ README.md

**Happy Coding!** 🚀
