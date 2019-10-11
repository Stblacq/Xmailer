from django import db
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from core.models import Contact
import openpyxl
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json
from django.views.decorators.csrf import csrf_exempt
from froala_editor import File, Image, Video, S3
from froala_editor import DjangoAdapter
import time
from django.core.files.storage import FileSystemStorage


def home(request):
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username = request.POST['username'] )
            user.is_active = False
            user.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Profile Created Successfully')
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    tab = 'mail'
    groups = Contact.objects.values('group').distinct()
    return render(request, 'dashboard/index.html', {'tab': tab, 'groups': groups})


@login_required
def contacts(request):
    tab = 'contacts'
    if request.method == 'POST':
        excel_file = request.FILES["contacts_excel"]
        # to do Excel Validation
        wb = openpyxl.load_workbook(excel_file)
        worksheet = wb["Sheet1"]
        i = 0
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            if i != 0:
                new_contact = Contact(first_name=row_data[0],
                                      last_name=row_data[1], email=row_data[2], phone_number=row_data[3], group=str(request.POST['group']).strip().upper())
                new_contact.save()
            i += 1
        messages.add_message(request, messages.SUCCESS,
                             'Uploaded Successfully')
        return redirect('contacts')

    else:
        contacts = Contact.objects.all()
        return render(request, 'dashboard/contacts.html', {'tab': tab, 'contacts': contacts})


@login_required
def edit_contact(request, id):
    if request.method == 'POST':
        contact = Contact.objects.get(pk=id)
        contact.first_name = request.POST['first_name']
        contact.last_name = request.POST['last_name']
        contact.email = request.POST['email']
        contact.phone_number = request.POST['phone_number']
        contact.group = request.POST['group']
        contact.save()
        messages.add_message(request, messages.SUCCESS,
                             'Updated Successfully')
        return redirect('contacts')
    else:
        return redirect('contacts')
    # messages.add_message(request, messages.SUCCESS,
    #                      'Password Changed Successfully')
    # return redirect('login')


@login_required
def delete_contact(request, id):
    if request.method == 'POST':
        contact = Contact.objects.get(pk=id)
        contact.delete()
        messages.add_message(request, messages.SUCCESS,
                             'Deleted Successfully')
        return redirect('contacts')
    else:
        return redirect('contacts')


@login_required
def password_change_success(request):
    messages.add_message(request, messages.SUCCESS,
                         'Password Changed Successfully')
    return redirect('login')


@login_required
@csrf_exempt
def froala(request):
    try:
        response = Image.upload(DjangoAdapter(request),'/core/media/text/')
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    response['link']= request.build_absolute_uri(response['link'])
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def send_email(request):
    # return JsonResponse(request.POST)
    batch = Contact.objects.filter(group=request.POST['group'])
    contacts = []
    for contact in batch:
        contacts.append(contact.email)

    message = Mail(
        from_email='from_email@example.com',
        to_emails=contacts,
        subject=request.POST['subject'],
        html_content= request.POST['message'],
        is_multiple=True)
    try:
        sg = SendGridAPIClient(
            '')
        response = sg.send(message)
        messages.add_message(request, messages.SUCCESS,
                         'Message Successfully')
        return redirect('contacts')

    except Exception as e:
            messages.add_message(request, messages.ERROR,
                         'An Error Occured')
            return redirect('contacts')
