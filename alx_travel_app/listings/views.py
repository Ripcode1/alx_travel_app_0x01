from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Listing objects.
    
    Provides CRUD operations:
    - list: GET /api/listings/
    - create: POST /api/listings/
    - retrieve: GET /api/listings/{id}/
    - update: PUT /api/listings/{id}/
    - partial_update: PATCH /api/listings/{id}/
    - destroy: DELETE /api/listings/{id}/
    """
    
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['property_type', 'available', 'location']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['price_per_night', 'created_at', 'number_of_guests']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Optionally filter listings by query parameters.
        """
        queryset = super().get_queryset()
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price_per_night__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)
        
        # Filter by number of guests
        guests = self.request.query_params.get('guests')
        if guests:
            queryset = queryset.filter(number_of_guests__gte=guests)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set the host to the current user when creating a listing"""
        serializer.save(host=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_listings(self, request):
        """
        Custom endpoint to get listings created by the current user.
        GET /api/listings/my_listings/
        """
        listings = self.queryset.filter(host=request.user)
        serializer = self.get_serializer(listings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_availability(self, request, pk=None):
        """
        Toggle the availability status of a listing.
        POST /api/listings/{id}/toggle_availability/
        """
        listing = self.get_object()
        
        # Check if user is the host
        if listing.host != request.user:
            return Response(
                {'error': 'You do not have permission to modify this listing'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        listing.available = not listing.available
        listing.save()
        
        serializer = self.get_serializer(listing)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Get all available listings.
        GET /api/listings/available/
        """
        available_listings = self.queryset.filter(available=True)
        serializer = self.get_serializer(available_listings, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Booking objects.
    
    Provides CRUD operations:
    - list: GET /api/bookings/
    - create: POST /api/bookings/
    - retrieve: GET /api/bookings/{id}/
    - update: PUT /api/bookings/{id}/
    - partial_update: PATCH /api/bookings/{id}/
    - destroy: DELETE /api/bookings/{id}/
    """
    
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'listing', 'user']
    ordering_fields = ['check_in_date', 'created_at', 'total_price']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Filter bookings based on user role.
        Users can only see their own bookings.
        Hosts can see bookings for their listings.
        """
        user = self.request.user
        
        # Get bookings where user is the guest or the host of the listing
        return Booking.objects.filter(
            Q(user=user) | Q(listing__host=user)
        ).distinct()
    
    def perform_create(self, serializer):
        """Set the user to the current user when creating a booking"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        """
        Get all bookings made by the current user.
        GET /api/bookings/my_bookings/
        """
        bookings = Booking.objects.filter(user=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_property_bookings(self, request):
        """
        Get all bookings for properties owned by the current user.
        GET /api/bookings/my_property_bookings/
        """
        bookings = Booking.objects.filter(listing__host=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """
        Confirm a booking (only by listing host).
        POST /api/bookings/{id}/confirm/
        """
        booking = self.get_object()
        
        # Check if user is the listing host
        if booking.listing.host != request.user:
            return Response(
                {'error': 'Only the listing host can confirm bookings'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if booking.status != 'pending':
            return Response(
                {'error': f'Cannot confirm booking with status: {booking.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'confirmed'
        booking.save()
        
        serializer = self.get_serializer(booking)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel a booking.
        POST /api/bookings/{id}/cancel/
        """
        booking = self.get_object()
        
        # User can cancel their own booking, or host can cancel any booking
        if booking.user != request.user and booking.listing.host != request.user:
            return Response(
                {'error': 'You do not have permission to cancel this booking'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if booking.status == 'completed':
            return Response(
                {'error': 'Cannot cancel a completed booking'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'cancelled'
        booking.save()
        
        serializer = self.get_serializer(booking)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """
        Get upcoming bookings for the current user.
        GET /api/bookings/upcoming/
        """
        from datetime import date
        
        upcoming_bookings = Booking.objects.filter(
            user=request.user,
            check_in_date__gte=date.today(),
            status__in=['pending', 'confirmed']
        )
        
        serializer = self.get_serializer(upcoming_bookings, many=True)
        return Response(serializer.data)
