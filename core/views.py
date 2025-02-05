from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Payment
from .serializers import PaymentCreateSerializer, PaymentReadSerializer
from django.views.generic import TemplateView

class ReactAppView(TemplateView):
    template_name = 'index.html'

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def get_serializer_class(self):
        # Use PaymentCreateSerializer for create, update, and partial_update actions
        if self.action in ['create', 'update', 'partial_update']:
            return PaymentCreateSerializer
        # Use PaymentReadSerializer for all other actions (list, retrieve)
        return PaymentReadSerializer

    def get_queryset(self):
        # Filter payments by the current user
        return Payment.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def payment_history(self, request):
        """
        Custom action to retrieve payment history for the authenticated user.
        """
        payments = self.get_queryset()
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        Automatically assign the current user to the payment during creation.
        """
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Handle payment creation and return appropriate response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Handle payment update and return appropriate response.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Handle payment deletion and return appropriate response.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)