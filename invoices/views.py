from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render,get_object_or_404,redirect
from django.views import generic
from django.template import loader
from datetime import date
from django.urls import reverse
from django.db.models import Q
from .models import customer,item,invoice,invoice_items ,invoice_setting
from .forms import customerForm , itemForm, invoiceForm , invoice_itemsForm,invoice_settingForm,UserForm

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

# Create your views here.
def index(request):
	if not request.user.is_authenticated():
		return render(request, 'invoices/login.html')
	else:
		try:
			image = invoice_setting.objects.get(user=request.user)
			logo_url = str(image.logo.url)
		except invoice_setting.DoesNotExist:
			image = None
			logo_url = None
		all_inv = invoice.objects.filter(user=request.user)
		context = {"all_inv":all_inv,"logo_url":logo_url}
		return render(request,'invoices/index.html', context)	

def edit_invoice(request,inv_id):
	if not request.user.is_authenticated():
		return render(request, 'invoices/login.html')
	else:
		selected_inv = get_object_or_404(invoice,pk=inv_id)
		inv_items = invoice_items.objects.filter(user=request.user,invoice_id = inv_id)
		form = invoice_itemsForm(request.POST or None)
		if form.is_valid():
			inv_item = form.save(commit = False)
			inv_item.user = request.user
			inv_tot = form.cleaned_data['quantity'] * form.cleaned_data['unit_price']
			inv_item.total_price = inv_tot
			inv_item.save()
			context = {"selected_inv":selected_inv,"inv_items":inv_items,"form":form}
			return render(request,'invoices/edit_invoice.html',context)
		context = {"selected_inv":selected_inv,"inv_items":inv_items,"form":form}
		return render(request,'invoices/edit_invoice.html', context)		

def create_invoice(request):
	if not request.user.is_authenticated():
		return render(request, 'invoices/login.html')
	else:
		form = invoiceForm(request.POST or None)
		if form.is_valid():
			invoice = form.save(commit=False)
			invoice.user = request.user
			invoice.save()
			context={}
			return redirect('../' + str(invoice.id) ,inv_id = invoice.id)
		context = {"form":form}
		return render(request,'invoices/create_invoice.html',context)


def add_items(request,inv_id):
	if not request.user.is_authenticated():
		return render(request, 'invoices/login.html')
	else:
		form = invoice_itemsForm(request.POST or None)
		if form.is_valid():
			invoice = form.save(commit=False)
			item.invoice_id = inv_id
			invoice.user = request.user
			invoice.total = invoice.quantity * invoice.unit_price
			invoice.save()
			context={}
			return render(request,'invoices/home.html',context)
		context = {"form":form}
		return render(request,'invoices/edit_invoice.html',context)

def remove_item(request,inv_id,item_id):
	if not request.user.is_authenticated():
		return render(request, 'invoices/login.html')
	else:
		current_item = invoice_items.objects.get(pk=item_id)
		current_item.delete()
		selected_inv = get_object_or_404(invoice,pk=inv_id)
		inv_items = invoice_items.objects.filter(user=request.user)
		form = invoice_itemsForm(request.POST or None)
		if form.is_valid():
			inv_item = form.save(commit = False)
			inv_item.user = request.user
			inv_item.save()
			context = {"selected_inv":selected_inv,"inv_items":inv_items,"form":form}
			return render(request,'invoices/edit_invoice.html',context)
		context = {"selected_inv":selected_inv,"inv_items":inv_items,"form":form}
		return render(request,'invoices/edit_invoice.html', context)

def remove_invoice(request,inv_id):
	if not request.user.is_authenticated():
		return render(request, 'invoices/login.html')
	else:
		current_invoice = get_object_or_404(invoice, pk=inv_id)
		current_invoice.delete()
		return render(request,'invoices/home.html')

def pay_invoice(request,inv_id):
	if not request.user.is_authenticated():
		return render(request, 'invoices/login.html')
	else:
		current_invoice = get_object_or_404(invoice, pk=inv_id)
		current_invoice.is_paid=True
		current_invoice.save()
		return render(request,'invoices/home.html')

def print_invoice(request,inv_id):
	inv = get_object_or_404(invoice,pk=inv_id)
	items = invoice_items.objects.filter(invoice_id=inv_id)
	inv_owner = inv.user.id
	inv_logo = invoice_setting.objects.get(user = inv_owner)
	inv_total = 0
	total = 0
	for item in items:
		total = item.quantity * item.unit_price
		inv_total += total
	context = {"inv":inv,"items":items,"total":total,"inv_total":inv_total,"inv_logo":inv_logo}
	return render(request,'invoices/inv.html',context)

def upload_logo(request):
	if not request.user.is_authenticated():
		return render(request, 'invoices/login.html')
	else:
		form = invoice_settingForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			inv_setting = form.save(commit = False)
			inv_setting.user = request.user
			inv_setting.logo = request.FILES['logo']
			file_type = inv_setting.logo.url.split('.')[-1]
			file_type = file_type.lower()
			if file_type not in IMAGE_FILE_TYPES:
				context={"error_message":'Image file must be PNG, JPG, or JPEG',"form":form}
				return render(request,'upload_logo',context)
			inv_setting.save()
			return render(request,'invoices/home.html')
		context = {"form":form}
		return render(request,'invoices/upload_logo.html', context)

def change_logo(request):
	if not request.user.is_authenticated():
		return render(request, 'invoices/login.html')
	else:
		the_logo = get_object_or_404(invoice_setting,user=request.user)
		form = invoice_settingForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			inv_setting = invoice_setting.objects.get(user=request.user)
			inv_setting.logo = request.FILES['logo']
			file_type = inv_setting.logo.url.split('.')[-1]
			file_type = file_type.lower()
			if file_type not in IMAGE_FILE_TYPES:
				context={"error_message":'Image file must be PNG, JPG, or JPEG',"form":form}
				return render(request,'invoices/change_logo.html',context)
			inv_setting.save()
			return render(request,'invoices/home.html')
		context = {"form":form}
		return render(request,'invoices/change_logo.html', context)


def create_customer(request):
	if not request.user.is_authenticated():
		return render(request, 'invoices/login.html')
	else:
		user_customers = customer.objects.filter(user = request.user)
		form = customerForm(request.POST or None)
		if form.is_valid():
			new_customer = form.save(commit=False)
			new_customer.user = request.user
			new_customer.save()
			context = {"form":form,}
			return redirect('../../')
		context = {"form":form,"user_customers":user_customers}
		return render(request,'invoices/create_customer.html',context)

def create_item(request):
	if not request.user.is_authenticated():
		return render(request, 'invoices/login.html')
	else:
		user_items = item.objects.filter(user=request.user)
		form = itemForm(request.POST or None)
		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.user = request.user
			new_item.save()
			return redirect('../../')
		context = {"form":form,"user_items":user_items}
		return render(request,'invoices/create_item.html',context)



def edit_customer(request,customer_id):
	if not request.user.is_authenticated():
		return render(request, 'invoices/login.html')
	else:
		selected_inv = get_object_or_404(customer,pk=customer_id)
		form = customerForm(request.POST or None,instance = selected_inv)
		if form.is_valid():
			form.save()
			return redirect('../../../')
		context = {"selected_inv":selected_inv,"form":form}
		return render(request,'invoices/edit_customer.html', context)

def edit_item(request,item_id):
	if not request.user.is_authenticated():
		return render(request, 'invoices/login.html')
	else:
		selected_inv = get_object_or_404(item,pk=item_id)
		form = itemForm(request.POST or None,instance = selected_inv)
		if form.is_valid():
			form.save()
			return redirect('../../../')
		context = {"selected_inv":selected_inv,"form":form}
		return render(request,'invoices/edit_item.html', context)

def delete_customer(request,customer_id):
	if not request.user.is_authenticated():
		return render(request, 'invoices/login.html')
	else:
		this_customer = customer.objects.get(user = request.user , pk = customer_id)
		this_customer.delete()
		return redirect('../../add/')


def delete_item(request,item_id):
	if not request.user.is_authenticated():
		return render(request, 'invoices/login.html')
	else:
		this_customer = item.objects.get(user = request.user , pk = item_id)
		this_customer.delete()
		return redirect('../../add/')












def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return render(request, 'invoices/home.html', {})
			else:
				return render(request, 'invoices/login.html', {'error_message': 'Your account has been disabled'})
		else:
			return render(request, 'invoices/login.html', {'error_message': 'Invalid login'})
	return render(request, 'invoices/login.html')


def register(request):
	form = UserForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user.set_password(password)
		user.save()
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				all_categories = Category.objects.filter(user=request.user)
				return render(request, 'invoices/home.html', {'all_categories': all_categories})
	context = {"form": form,}
	return render(request, 'invoices/register.html', context)

def logout_user(request):
	logout(request)
	form = UserForm(request.POST or None)
	context = {"form": form,}
	return render(request, 'invoices/login.html', context)