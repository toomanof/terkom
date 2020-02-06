from rest_framework import serializers
from calculation.models.invoice import Invoice, InvoiceItems


class InvoiceSerializerGet(serializers.ModelSerializer):
    contractor = serializers.StringRelatedField(many=False)
    delivered = serializers.StringRelatedField(many=False)
    adopted = serializers.StringRelatedField(many=False)
    abs_url = serializers.SerializerMethodField('get_absolute_url')

    def get_absolute_url(self, obj: Invoice):
        return obj.get_absolute_url()


    class Meta:
        model = Invoice
        fields = ['id', 'number', 'created_at', 'contractor', 'delivered', 'adopted', 'motion', 'total', 'abs_url']


class InvoiceItemsSerializerGet(serializers.ModelSerializer):
    invoice_doc = serializers.StringRelatedField(many=False)
    product = serializers.StringRelatedField(many=False)
    adopted = serializers.StringRelatedField(many=False)

    class Meta:
        model = InvoiceItems
        fields = ['id', 'invoice_doc', 'position', 'product', 'qty', 'price']
