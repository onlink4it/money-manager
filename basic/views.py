from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.template import loader
from datetime import date
from django.urls import reverse
from django.db.models import Q
from .forms import CategoryForm, SubCategoryForm, InTransactionForm, OutTransactionForm, UserForm
from .models import Category,SubCategory,InTransaction,OutTransaction
# Create your views here.

def index(request):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		all_categories = SubCategory.objects.filter(user=request.user)
		maincategories = Category.objects.filter(user=request.user)	
		in_trans = InTransaction.objects.filter(user=request.user)
		out_trans = OutTransaction.objects.filter(user=request.user)
		in_sum = 0
		out_sum = 0
		income_by_subcategory = {}
		income_by_maincategory = {}

		
		#### Each SubCategory Income & Outcome #####	
		for category in all_categories:
			cat_in_sum = 0
			cat_out_sum = 0
			in_selected_trans = InTransaction.objects.filter(sub_cat= category.id,user=request.user)
			out_selected_trans = OutTransaction.objects.filter(sub_cat= category.id,user=request.user)
			if in_selected_trans.count()> 0:
				for trans in in_selected_trans:
					cat_in_sum += trans.amount
			if out_selected_trans.count()> 0:
				for trans in out_selected_trans:
					cat_out_sum += trans.amount
			income_by_subcategory.update({category.name:[cat_in_sum, cat_out_sum, cat_in_sum-cat_out_sum]})

		#### Each MainCategory Income & Outcome ####
		for main_category in maincategories:
			cat_in_sum = 0
			cat_out_sum = 0
			selected_main_cat  = SubCategory.objects.filter(parent = main_category.id,user=request.user)
			for subcategory in  selected_main_cat:
				in_selected_trans = InTransaction.objects.filter(sub_cat= subcategory.id,user=request.user)
				out_selected_trans = OutTransaction.objects.filter(sub_cat= subcategory.id,user=request.user)
				if in_selected_trans.count()> 0:
					for trans in in_selected_trans:
						cat_in_sum += trans.amount
				if out_selected_trans.count()> 0:
					for trans in out_selected_trans:
						cat_out_sum += trans.amount
			income_by_maincategory.update({(main_category.id,main_category.name):[cat_in_sum, cat_out_sum, cat_in_sum-cat_out_sum]})

		#### Total Income ####
		for trans in in_trans:
			in_sum += trans.amount
		#### Total Outcome ####
		for trans in out_trans:
			out_sum += trans.amount
		#### Current Balance ####
		current_balance = in_sum - out_sum
		#### Recent Income Transactions ####
		recent_in_trans = InTransaction.objects.filter(user=request.user).order_by('-date')[:10]
		#### Recent Outcome Transactions ####
		recent_out_trans = OutTransaction.objects.filter(user=request.user).order_by('-date')[:10]

		#### Dictionary ####
		context = {
			"in_sum": in_sum,
			"out_sum": out_sum,
			"current_balance": current_balance,
			"recent_in_trans": recent_in_trans,
			"recent_out_trans": recent_out_trans,
			"income_by_subcategory":income_by_subcategory.items(),
			"income_by_maincategory": income_by_maincategory.items(),
		}

		return render(request,'basic/index.html',context)









def CategoryList(request):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		all_categories = Category.objects.filter(user=request.user)
		context = {"all_categories":all_categories}
		return render(request,"basic/categories.html",context)

def SubCategoryList(request,maincategory_id):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		all_categories = SubCategory.objects.filter(parent=maincategory_id,user=request.user)
		context = {"all_categories":all_categories,"maincategory_id":maincategory_id}
		return render(request,"basic/subcategories.html",context)

def report(request,maincategory_id):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		maincategory = get_object_or_404(Category,pk=maincategory_id,user=request.user)
		sub_cat = SubCategory.objects.filter(parent = maincategory_id,user=request.user)
		report = {}
		for sub in sub_cat:
			in_trans = InTransaction.objects.filter(sub_cat= sub.id,user=request.user)
			out_trans = OutTransaction.objects.filter(sub_cat= sub.id,user=request.user)
			sum_in = 0
			sum_out = 0
			for trans in in_trans:
				sum_in += trans.amount
			for trans in out_trans:
				sum_out += trans.amount

			report.update({(sub.id,sub.name):[sum_in, sum_out, sum_in - sum_out]})
		context = {'maincategory': maincategory,
			'report': report.items(),
			}
		return render(request,'basic/report.html',context)

def detailedreport(request,maincategory_id,subcategory_id):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		subcategory = get_object_or_404(SubCategory,pk=subcategory_id,user=request.user)
		in_trans = InTransaction.objects.filter(sub_cat=subcategory_id,user=request.user)
		out_trans = OutTransaction.objects.filter(sub_cat=subcategory_id,user=request.user)
		context = {'in_trans':in_trans,'out_trans':out_trans}
		return render(request,'basic/detailedreport.html',context)

def incomereport(request):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		in_trans = InTransaction.objects.filter(user=request.user)
		context = {'in_trans':in_trans,}
		return render(request,'basic/incomereport.html',context)

def outcomereport(request):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		out_trans = OutTransaction.objects.filter(user=request.user)
		context = {'out_trans':out_trans,}
		return render(request,'basic/outcomereport.html',context)

def allreport(request):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		in_trans = InTransaction.objects.filter(user=request.user)
		out_trans = OutTransaction.objects.filter(user=request.user)
		context = {'in_trans':in_trans,'out_trans':out_trans,}
		return render(request,'basic/allreport.html',context)

def graph(request):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		context={}
		return render(request,'basic/graph.html',context)








def addcategory(request):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		all_categories=Category.objects.filter(user=request.user)
		form = CategoryForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			category = form.save(commit=False)
			category.user = request.user
			category.save()
			context={"all_categories":all_categories}
			return render(request,'basic/categories.html',context)
		context = {"form":form}
		return render(request,'basic/addcategory.html',context)

def addsubcategory(request,maincategory_id):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		all_categories=Category.objects.filter(user=request.user)
		user = request.user
		all_categories = Category.objects.filter(user=request.user)
		maincategory = get_object_or_404(Category,pk=maincategory_id)
		maincategory_id = maincategory.id
		sub_form = SubCategoryForm(request.POST or None)
		if sub_form.is_valid():
			subcategory = sub_form.save(commit=False)
			subcategory.user = request.user
			subcategory.parent = maincategory
			subcategory.save()
			context={"all_categories":all_categories}
			return render(request,'basic/categories.html',context)
		context = {"sub_form":sub_form,"maincategory":maincategory,"maincategory_id":maincategory_id,"user":user,"all_categories":all_categories}
		return render(request,'basic/addsubcategory.html',context)

def addincome(request):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		add_income_form = InTransactionForm(request.POST or None)
		all_SubCategories = SubCategory.objects.filter(user=request.user)
		if add_income_form.is_valid():
			inTrans = add_income_form.save(commit=False)
			inTrans.user = request.user
			inTrans.save()
			context={"all_SubCategories": all_SubCategories}
			return render(request,'basic/home.html',context)
		context = {"add_income_form":add_income_form,"all_SubCategories": all_SubCategories}
		return render(request,'basic/addincome.html',context)

def addoutcome(request):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		add_outcome_form = OutTransactionForm(request.POST or None)
		all_SubCategories = SubCategory.objects.filter(user=request.user)
		if add_outcome_form.is_valid():
			outTrans = add_outcome_form.save(commit=False)
			outTrans.user = request.user
			outTrans.save()
			context={"all_SubCategories": all_SubCategories}
			return render(request,'basic/home.html',context)
		context = {"add_outcome_form":add_outcome_form,"all_SubCategories": all_SubCategories}
		return render(request,'basic/addoutcome.html',context)



def edit_category(request,cat_id):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		all_categories = Category.objects.filter(user=request.user)
		selected_cat = Category.objects.get(pk = cat_id,user=request.user)
		form = CategoryForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			category = form.save(commit=False)
			category.user = request.user
			category.save()
			context={"all_categories":all_categories}
			return render(request,'basic/categories.html',context)
		context = {"form":form,"selected_cat":selected_cat,"all_categories":all_categories}
		return render(request,'basic/edit_category.html',context)

def edit_subCategory(request,cat_id):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		all_categories = Category.objects.filter(user=request.user)
		selected_cat = SubCategory.objects.get(pk = cat_id,user=request.user)
		form = SubCategoryForm(request.POST or None , request.FILES or None)
		if form.is_valid():
			sub_cat = form.save(commit=False)
			sub_cat.user = request.user
			sub_cat.save()
			context = {"all_categories": all_categories}
			return render(request,'basic/categories.html',context)
		context = {"form": form,"all_categories": all_categories,"cat_id":cat_id,"selected_cat":selected_cat}
		return render(request,'basic/edit_subcategory.html',context)

def edit_income(request,trans_id):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		edit_income_form = InTransactionForm(request.POST or None)
		all_SubCategories = SubCategory.objects.filter(user=request.user)
		current_trans = InTransaction.objects.get(pk = trans_id,user=request.user)
		if edit_income_form.is_valid():
			inTrans = edit_income_form.save(commit=False)
			inTrans.user = request.user
			inTrans.save()
			context={}
			return render(request,'basic/home.html',context)
		context = {"all_SubCategories": all_SubCategories,"current_trans":current_trans}
		return render(request,'basic/edit_income.html',context)

def edit_outcome(request,trans_id):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		edit_outcome_form = OutTransactionForm(request.POST or None)
		all_SubCategories = SubCategory.objects.filter(user=request.user)
		current_trans = OutTransaction.objects.get(pk = trans_id,user=request.user)
		if edit_outcome_form.is_valid():
			outTrans = edit_outcome_form.save(commit=False)
			outTrans.user = request.user
			outTrans.save()
			context={}
			return render(request,'basic/home.html',context)
		context = {"all_SubCategories":all_SubCategories,"current_trans":current_trans}
		return render(request,'basic/edit_outcome.html',context)








def delete_category(request,cat_id):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		all_categories = Category.objects.filter(user=request.user)
		current_cat = Category.objects.get(pk=cat_id,user=request.user)
		current_cat.delete()
		context = {"all_categories": all_categories}
		return render(request,'basic/categories.html',context)

def delete_subCategory(request,cat_id):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		all_categories = Category.objects.filter(user=request.user)
		current_cat = SubCategory.objects.get(pk=cat_id,user=request.user)
		current_cat.delete()
		context={"all_categories": all_categories}
		return render(request,'basic/home.html',context)

def delete_income(request,trans_id):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		selected_trans = InTransaction.objects.get(pk=trans_id,user=request.user)
		selected_trans.delete()
		context = {}
		return render(request,'basic/home.html',context)

def delete_outcome(request,trans_id):
	if not request.user.is_authenticated():
		return render(request, 'basic/login.html')
	else:
		selected_trans = OutTransaction.objects.get(pk=trans_id,user=request.user)
		selected_trans.delete()
		context = {}
		return render(request,'basic/home.html',context)









def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				all_categories = Category.objects.filter(user=request.user)
				return render(request, 'basic/home.html', {'all_categories': all_categories})
			else:
				return render(request, 'basic/login.html', {'error_message': 'Your account has been disabled'})
		else:
			return render(request, 'basic/login.html', {'error_message': 'Invalid login'})
	return render(request, 'basic/login.html')


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
				return render(request, 'basic/home.html', {'all_categories': all_categories})
	context = {"form": form,}
	return render(request, 'basic/register.html', context)

def logout_user(request):
	logout(request)
	form = UserForm(request.POST or None)
	context = {"form": form,}
	return render(request, 'basic/login.html', context)