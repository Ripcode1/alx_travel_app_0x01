# 🚀 ALX Travel App - Complete Setup and Testing Guide

## ✅ Project Overview

This project implements a complete **RESTful API** for a travel booking platform using **Django REST Framework**. It includes:

- ✅ Full CRUD operations for Listings and Bookings
- ✅ RESTful API design with proper HTTP methods
- ✅ Django REST Framework ViewSets
- ✅ Automatic URL routing with DRF routers
- ✅ Interactive Swagger/OpenAPI documentation
- ✅ Advanced filtering, searching, and sorting
- ✅ Authentication and permissions
- ✅ Comprehensive validation

---

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
    │   ├── settings.py        # Django settings with DRF & Swagger config
    │   ├── urls.py            # Main URL configuration with Swagger
    │   ├── wsgi.py
    │   └── asgi.py
    └── listings/
        ├── __init__.py
        ├── models.py          # Listing and Booking models
        ├── serializers.py     # DRF serializers with validation
        ├── views.py           # ViewSets with CRUD operations ← KEY FILE
        ├── urls.py            # Router configuration ← KEY FILE
        ├── admin.py           # Django admin interface
        └── apps.py
```

---

## 🛠️ Quick Start Guide

### Step 1: Install Dependencies

```bash
cd alx_travel_app_0x01/alx_travel_app
pip install -r requirements.txt
```

**Dependencies installed:**
- Django 4.2+
- djangorestframework
- django-filter
- drf-yasg (Swagger)
- django-cors-headers
- psycopg2-binary

### Step 2: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Create Superuser

```bash
python manage.py createsuperuser
```

Enter username, email, and password when prompted.

### Step 4: Run Server

```bash
python manage.py runserver
```

Server starts at: `http://127.0.0.1:8000/`

---

## 📚 Access API Documentation

### Swagger UI (Interactive)
```
http://127.0.0.1:8000/swagger/
```

### ReDoc (Alternative)
```
http://127.0.0.1:8000/redoc/
```

### Django Admin
```
http://127.0.0.1:8000/admin/
```

---

## 🔌 API Endpoints Reference

### Listings API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/listings/` | List all listings |
| POST | `/api/listings/` | Create new listing |
| GET | `/api/listings/{id}/` | Get specific listing |
| PUT | `/api/listings/{id}/` | Update listing |
| PATCH | `/api/listings/{id}/` | Partial update |
| DELETE | `/api/listings/{id}/` | Delete listing |
| GET | `/api/listings/my_listings/` | User's listings |
| GET | `/api/listings/available/` | Available listings |
| POST | `/api/listings/{id}/toggle_availability/` | Toggle availability |

### Bookings API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/bookings/` | List all bookings |
| POST | `/api/bookings/` | Create booking |
| GET | `/api/bookings/{id}/` | Get specific booking |
| PUT | `/api/bookings/{id}/` | Update booking |
| PATCH | `/api/bookings/{id}/` | Partial update |
| DELETE | `/api/bookings/{id}/` | Delete booking |
| GET | `/api/bookings/my_bookings/` | User's bookings |
| GET | `/api/bookings/my_property_bookings/` | Property bookings |
| GET | `/api/bookings/upcoming/` | Upcoming bookings |
| POST | `/api/bookings/{id}/confirm/` | Confirm booking |
| POST | `/api/bookings/{id}/cancel/` | Cancel booking |

---

## 🧪 Testing with Postman

### Method 1: Import Collection

1. Open Postman
2. Click **Import**
3. Select `ALX_Travel_App_Postman_Collection.json`
4. Collection with all endpoints will be imported

### Method 2: Manual Testing

#### Test 1: Create a Listing

**Request:**
```http
POST http://127.0.0.1:8000/api/listings/
Content-Type: application/json

{
  "title": "Luxury Villa in Bali",
  "description": "Beautiful beachfront villa",
  "location": "Bali, Indonesia",
  "price_per_night": 250.00,
  "property_type": "villa",
  "number_of_guests": 6,
  "number_of_bedrooms": 3,
  "number_of_bathrooms": 2,
  "amenities": "Pool, WiFi, Beach Access",
  "available": true,
  "host_id": 1
}
```

**Expected Response:** `201 Created`

#### Test 2: Get All Listings

**Request:**
```http
GET http://127.0.0.1:8000/api/listings/
```

**Expected Response:** `200 OK` with paginated results

#### Test 3: Filter Listings

**Request:**
```http
GET http://127.0.0.1:8000/api/listings/?location=Bali&min_price=100&max_price=300
```

**Expected Response:** `200 OK` with filtered results

#### Test 4: Create a Booking

**Request:**
```http
POST http://127.0.0.1:8000/api/bookings/
Content-Type: application/json

{
  "listing_id": 1,
  "user_id": 2,
  "check_in_date": "2025-12-15",
  "check_out_date": "2025-12-20",
  "number_of_guests": 4
}
```

**Expected Response:** `201 Created` with `total_price` calculated automatically

#### Test 5: Confirm Booking (Host Only)

**Request:**
```http
POST http://127.0.0.1:8000/api/bookings/1/confirm/
```

**Expected Response:** `200 OK` with status changed to "confirmed"

#### Test 6: Update Listing

**Request:**
```http
PATCH http://127.0.0.1:8000/api/listings/1/
Content-Type: application/json

{
  "price_per_night": 300.00
}
```

**Expected Response:** `200 OK` with updated data

#### Test 7: Delete Listing

**Request:**
```http
DELETE http://127.0.0.1:8000/api/listings/1/
```

**Expected Response:** `204 No Content`

---

## 🔐 Authentication

### Using Postman

**Method 1: Basic Auth**
1. Go to Authorization tab
2. Select "Basic Auth"
3. Enter username and password

**Method 2: Session Auth**
1. Login first at `/api-auth/login/`
2. Subsequent requests use cookies

---

## ✨ Key Features Implemented

### 1. **ModelViewSets** (listings/views.py)

```python
class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # ... filtering, searching, ordering
```

### 2. **Router Configuration** (listings/urls.py)

```python
router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')
```

### 3. **Custom Actions**

```python
@action(detail=False, methods=['get'])
def my_listings(self, request):
    # Custom endpoint: /api/listings/my_listings/
    ...

@action(detail=True, methods=['post'])
def toggle_availability(self, request, pk=None):
    # Custom endpoint: /api/listings/{id}/toggle_availability/
    ...
```

### 4. **Advanced Filtering**

```python
filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
filterset_fields = ['property_type', 'available', 'location']
search_fields = ['title', 'description', 'location']
ordering_fields = ['price_per_night', 'created_at', 'number_of_guests']
```

### 5. **Validation**

```python
def validate(self, data):
    if check_out <= check_in:
        raise serializers.ValidationError("...")
    if number_of_guests > listing.number_of_guests:
        raise serializers.ValidationError("...")
    return data
```

---

## 📊 Models Overview

### Listing Model
- Property information (title, description, location)
- Pricing and capacity
- Amenities and availability
- Host relationship

### Booking Model
- Booking dates and guests
- Automatic price calculation
- Status tracking (pending, confirmed, cancelled, completed)
- Validation for dates and capacity

---

## 🎯 Testing Checklist

Use this checklist to verify all CRUD operations:

### Listings
- [ ] GET /api/listings/ - List all listings
- [ ] POST /api/listings/ - Create a listing
- [ ] GET /api/listings/{id}/ - Get specific listing
- [ ] PUT /api/listings/{id}/ - Update listing
- [ ] PATCH /api/listings/{id}/ - Partial update
- [ ] DELETE /api/listings/{id}/ - Delete listing

### Bookings
- [ ] GET /api/bookings/ - List all bookings
- [ ] POST /api/bookings/ - Create a booking
- [ ] GET /api/bookings/{id}/ - Get specific booking
- [ ] PUT /api/bookings/{id}/ - Update booking
- [ ] PATCH /api/bookings/{id}/ - Partial update
- [ ] DELETE /api/bookings/{id}/ - Delete booking

### Custom Endpoints
- [ ] GET /api/listings/my_listings/ - User's listings
- [ ] GET /api/listings/available/ - Available listings
- [ ] POST /api/listings/{id}/toggle_availability/ - Toggle availability
- [ ] GET /api/bookings/my_bookings/ - User's bookings
- [ ] GET /api/bookings/upcoming/ - Upcoming bookings
- [ ] POST /api/bookings/{id}/confirm/ - Confirm booking
- [ ] POST /api/bookings/{id}/cancel/ - Cancel booking

---

## 📝 Common Commands

```bash
# Run server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Shell access
python manage.py shell
```

---

## 🎓 Project Requirements Met

✅ **ViewSets Created**: ListingViewSet and BookingViewSet using ModelViewSet  
✅ **CRUD Operations**: Full Create, Read, Update, Delete for both models  
✅ **Router Configuration**: URLs automatically generated with DefaultRouter  
✅ **RESTful Conventions**: Proper HTTP methods and URL structure  
✅ **Swagger Documentation**: Interactive API docs at /swagger/  
✅ **API Testing**: Postman collection provided  
✅ **Endpoints under /api/**: All endpoints follow /api/listings/ and /api/bookings/  

---

## 🚀 Next Steps

1. **Download the project** from outputs folder
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run migrations**: `python manage.py migrate`
4. **Create superuser**: `python manage.py createsuperuser`
5. **Start server**: `python manage.py runserver`
6. **Open Swagger**: http://127.0.0.1:8000/swagger/
7. **Test with Postman**: Import the collection
8. **Upload to GitHub**: Create repository alx_travel_app_0x01

---

## 📞 Support

If you encounter any issues:
1. Check the README.md for detailed documentation
2. Verify all dependencies are installed
3. Ensure migrations are applied
4. Check Django server logs for errors

**Happy Coding!** 🎉
