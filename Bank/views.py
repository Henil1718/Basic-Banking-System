from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages
from django.db.models import F

from .forms import CreateUserform, CreateTransferform
from .models import Userform, Transferform

# Home page 
def bank(request):
    return render(request, 'Bank/bank.html')

# users page
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
            messages.success(request, f'Your account has been created!')
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
            sender_name = Userform.objects.get(name=user)
            sender = sender_name.name

            if Userform.objects.filter(name=receiver).exists():
                if receiver == sender:
                    messages.error(request, 'Enter a valid name')
                elif sender_name.balance < amount:
                    messages.error(request, 'Insufficient balance')
                elif amount < 0:
                    messages.error(request, 'Enter positive amount')
                elif sender_name.balance >= amount:
                    sender_name.balance = F('balance') - amount
                    sender_name.save()

                    receiver_name = Userform.objects.get(name=receiver)
                    receiver_name.balance = F('balance') + amount
                    receiver_name.save()

                    transfer_form = Transferform()
                    transfer_form.sender_name = sender_name
                    transfer_form.receiver_name = receiver
                    transfer_form.amount = amount
                    transfer_form.date = datetime.now()
                    transfer_form.save()
                    messages.success(request, 'Transaction successful')
                    return redirect('transaction_history')
            else:
                messages.error(request, 'Enter valid name')
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
    result = reversed(list(transaction_details))
    context = {
        'transaction_details' : result
    }
    return render(request, 'Bank/transaction_history.html', context)