from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from django.db.models import F

from .forms import CreateUserform, CreateTransferform
from .models import Userform, Transferform

# Home page 
def bank(request):
    return render(request, 'Bank/bank.html')

# available users page
def transaction(request):
    users = Userform.objects.all()
    context = {
        'users' : users
    }
    return render(request, 'Bank/transaction.html', context)

# user creation page
def create_user(request):
    if request.method == 'POST':
        form = CreateUserform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction')
    else:
        form = CreateUserform()
    context = {
        'form' : form
    }
    return render(request, 'Bank/create_user.html', context)

#  transaction page
def transfer(request, user_id):
    user = Userform.objects.get(pk=user_id)
    if request.method == 'POST':
        forms = CreateTransferform(request.POST)
        if forms.is_valid():
            receiver = forms.cleaned_data['receiver_name']
            amount = forms.cleaned_data['amount']
            sender = user
            sender_name = Userform.objects.get(name=sender)

            if receiver != user and sender_name.balance >= amount:
                sender_name.balance = F('balance') - amount
                sender_name.save()

                receiver_name = Userform.objects.get(name=receiver)
                receiver_name.balance = F('balance') + amount
                receiver_name.save()

                transfer_form = Transferform()
                transfer_form.sender_name = sender
                transfer_form.receiver_name = receiver
                transfer_form.amount = amount
                transfer_form.date = datetime.now()
                transfer_form.save()

                return redirect('transaction_history')
            else:
                html = '<div class="alert alert-warning"> <strong>Warning!</strong> Indicates a warning that might need attention.</div>'
                return HttpResponse('Error handler content', status=403)
        else:
            html = '<div class="alert alert-warning"> <strong>Warning!</strong> Indicates a warning that might need attention.</div>'
            return HttpResponse(html)
    else:
        forms = CreateTransferform()
    context = {
        'user' : user,
        'forms' : forms
    }
    return render(request, 'Bank/transfer.html', context)

# transaction_history page
def transaction_history(request):
    transaction_details = Transferform.objects.all()
    context = {
        'transaction_details' : transaction_details
    }
    return render(request, 'Bank/transaction_history.html', context)