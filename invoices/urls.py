from django.conf.urls import include, url
from django.contrib import admin
from . import views
app_name = "invoices"
urlpatterns = [
	url(r'^$', views.index , name="index"),	
	url(r'^$', views.index , name='index'),
	url(r'^login/$',views.login_user , name="login_user"),
	url(r'^logout/$',views.logout_user,name="logout_user"),
	url(r'^invoice/add/$',views.create_invoice,name="create_invoice"),
	url(r'^invoice/(?P<inv_id>[0-9]+)/$',views.edit_invoice,name="edit_invoice"),
	url(r'^invoice/(?P<inv_id>[0-9]+)/items/add/$',views.add_items,name="add_items"),
	url(r'^invoice/(?P<inv_id>[0-9]+)/delete/item/(?P<item_id>[0-9]+)/$',views.remove_item,name="remove_item"),
	url(r'^invoice/delete/(?P<inv_id>[0-9]+)/$',views.remove_invoice,name="remove_invoice"),
	url(r'^invoice/pay/(?P<inv_id>[0-9]+)/$',views.pay_invoice,name="pay_invoice"),
	url(r'^invoice/print/(?P<inv_id>[0-9]+)/$',views.print_invoice,name="print_invoice"),
	url(r'^logo/upload/$',views.upload_logo,name="upload_logo"),
	url(r'^logo/change/$',views.change_logo,name="change_logo"),
	url(r'^items/add/$',views.create_item,name="create_item"),
	url(r'^customers/add/$',views.create_customer,name="create_customer"),
	url(r'^items/edit/(?P<item_id>[0-9]+)/$',views.edit_item,name="edit_item"),
	url(r'^customers/edit/(?P<customer_id>[0-9]+)/$',views.edit_customer,name="edit_customer"),
	url(r'^customers/delete/(?P<customer_id>[0-9]+)/$',views.delete_customer,name="delete_customer"),
	url(r'^items/delete/(?P<item_id>[0-9]+)/$',views.delete_item,name="delete_item"),
]