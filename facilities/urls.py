from django.urls import path
from .views import (
    RoomListView, RoomCreateView, RoomUpdateView, RoomDeleteView, RoomDetailView,
    SickbayListView, SickbayCreateView, SickbayUpdateView, SickbayDeleteView, SickbayDetailView,
    AllocationListView, AllocationCreateView, AllocationUpdateView, AllocationDetailView,  AllocationDeleteView
)

urlpatterns = [
    # Room URLs
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('rooms/create/', RoomCreateView.as_view(), name='room_create'),
    path('rooms/<int:pk>/update/', RoomUpdateView.as_view(), name='room_update'),
    path('rooms/<int:pk>/delete/', RoomDeleteView.as_view(), name='room_delete'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room_detail'),

    # Sickbay URLs
    path('sickbays/', SickbayListView.as_view(), name='sickbay_list'),
    path('sickbays/create/', SickbayCreateView.as_view(), name='sickbay_create'),
    path('sickbays/<int:pk>/update/', SickbayUpdateView.as_view(), name='sickbay_update'),
    path('sickbays/<int:pk>/delete/', SickbayDeleteView.as_view(), name='sickbay_delete'),
    path('sickbays/<int:pk>/', SickbayDetailView.as_view(), name='sickbay_detail'),

    # Allocation URLs
    path('allocations/', AllocationListView.as_view(), name='allocation_list'),
    path('allocations/<int:pk>/', AllocationDetailView.as_view(), name='allocation_detail'),
    path('allocations/create/', AllocationCreateView.as_view(), name='allocation_create'),
    path('allocations/<int:pk>/update/', AllocationUpdateView.as_view(), name='allocation_update'),
    path('allocations/<int:pk>/delete/', AllocationDeleteView.as_view(), name='allocation_delete'),
]

# urlpatterns = [
    # Inventory
    # path('inventory/', InventoryListView.as_view(), name='inventory_list'),
    # path('inventory/<int:pk>/', InventoryDetailView.as_view(), name='inventory_detail'),
    # path('inventory/create/', InventoryCreateView.as_view(), name='inventory_create'),
    # path('inventory/<int:pk>/update/', InventoryUpdateView.as_view(), name='inventory_update'),
    # path('inventory/<int:pk>/delete/', InventoryDeleteView.as_view(), name='inventory_delete'),
# ]
