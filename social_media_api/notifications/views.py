from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Notification
from .serializers import NotificationSerializer, MarkAsReadSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own notifications
        return Notification.objects.filter(
            recipient=self.request.user
        ).select_related('actor', 'recipient').order_by('-created_at')
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications"""
        notifications = self.get_queryset().filter(is_read=False)
        page = self.paginate_queryset(notifications)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_as_read(self, request):
        """Mark notifications as read or unread"""
        serializer = MarkAsReadSerializer(data=request.data)
        if serializer.is_valid():
            notification_ids = serializer.validated_data['notification_ids']
            read_status = serializer.validated_data['read']
            
            # Filter to only user's notifications
            notifications = Notification.objects.filter(
                id__in=notification_ids,
                recipient=request.user
            )
            
            updated_count = 0
            for notification in notifications:
                if read_status:
                    notification.mark_as_read()
                else:
                    notification.mark_as_unread()
                updated_count += 1
            
            return Response({
                'message': f'{updated_count} notification(s) updated',
                'updated': updated_count,
                'read': read_status
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all notifications as read"""
        notifications = self.get_queryset().filter(is_read=False)
        updated_count = notifications.count()
        
        for notification in notifications:
            notification.mark_as_read()
        
        return Response({
            'message': f'All {updated_count} notification(s) marked as read',
            'updated': updated_count
        })
    
    @action(detail=True, methods=['post'])
    def toggle_read(self, request, pk=None):
        """Toggle read status of a single notification"""
        notification = self.get_object()
        
        if notification.is_read:
            notification.mark_as_unread()
            status_msg = 'marked as unread'
        else:
            notification.mark_as_read()
            status_msg = 'marked as read'
        
        return Response({
            'message': f'Notification {status_msg}',
            'is_read': notification.is_read
        })

class NotificationCountView(generics.GenericAPIView):
    """Get notification counts"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        total = Notification.objects.filter(recipient=request.user).count()
        unread = Notification.objects.filter(recipient=request.user, is_read=False).count()
        
        return Response({
            'total': total,
            'unread': unread,
            'unread_count': unread  # For compatibility
        })
