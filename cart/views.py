from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from item.models import Item
from .models import CartItem
from .serializers import CartItemSerializer

# User: List Available Items
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
def list_user_cart_items(request):
    try:
        cart_items = CartItem.objects.filter(user=request.user)
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart items not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CartItemSerializer(cart_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# User: Add Item to Cart
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_to_cart(request, product_name):
    item = get_object_or_404(Item, product_identifier=product_name)
    quantity = int(request.data.get('quantity', 1))
    if quantity < 1:
        quantity = 0

    # Find an existing cart item for the user and the specified item
    cart_item, _ = CartItem.objects.get_or_create(user=request.user, item=item)

    # Increment quantity based on the request data
    cart_item.quantity += quantity

    if cart_item.quantity > item.stock:
        return Response({'error': 'Required item quantity is not Available'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Save the cart item
    cart_item.save()
    serializer = CartItemSerializer(cart_item)
    return Response({'message': 'Given item quantity increased in cart', 'data': serializer.data}, status=status.HTTP_200_OK)

# User: Remove Item from Cart
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, product_name):
    item = get_object_or_404(Item, product_identifier=product_name)
    quantity = abs(int(request.data.get('quantity', 1)))

    cart_item  = get_object_or_404(CartItem, user=request.user, item=item)
    cart_item.quantity -= quantity

    if cart_item.quantity < 1:
        cart_item.delete()
        return Response({'message': 'Item removed from cart'}, status=status.HTTP_200_OK)
    
    cart_item.save()
    serializer = CartItemSerializer(cart_item)
    return Response({'message': 'Given Item quantity reduced from cart', 'data': serializer.data}, status=status.HTTP_200_OK)