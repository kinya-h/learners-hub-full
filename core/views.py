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

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PaymentCreateSerializer
        return PaymentReadSerializer

    def get_queryset(self):
        # Filter payments by the current user
        return Payment.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def payment_history(self, request):
        payments = self.get_queryset()
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
