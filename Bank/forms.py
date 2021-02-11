from django.forms import ModelForm

from .models import Userform, Transferform

# user form
class CreateUserform(ModelForm):
    class Meta:
        model = Userform
        fields = ['name', 'email', 'balance']

# transaction_history form
class CreateTransferform(ModelForm):
    class Meta:
        model = Transferform
        fields = ['receiver_name', 'amount']