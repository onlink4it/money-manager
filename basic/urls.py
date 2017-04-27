from django.conf.urls import include, url
from django.contrib import admin
from . import views
app_name = "basic"
urlpatterns = [
    # Examples:
    # url(r'^$', 'money_manager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index , name='index'),
    url(r'^login/$',views.login_user , name="login_user"),
    url(r'^logout/$',views.logout_user,name="logout_user"),
    url(r'^register/$',views.register,name="register"),
    # add/income/ 
    url(r'^add/income/$',views.addincome , name='addincome'),
    # add/outcome/ 
    url(r'^add/outcome/$',views.addoutcome , name='addoutcome'),
    # report/1/ 
    url(r'^report/(?P<maincategory_id>[0-9]+)/$', views.report , name='report'),
    #report/2/ 
    url(r'^report/(?P<maincategory_id>[0-9]+)/(?P<subcategory_id>[0-9]+)/$', views.detailedreport , name='detailedreport'),
    # report/income/ 
    url(r'^report/income/$', views.incomereport, name ='incomereport'),
    # report/outcome/ 
    url(r'^report/outcome/$', views.outcomereport, name ='outcomereport'),
    #report/all/
    url(r'^report/all/$', views.allreport , name='allreport'),
    #graphs/
    url(r'^graph/$',views.graph,name='graph'),
    #graphs/
    url(r'^graphs/$',views.detailed_graph,name='graphs'),
    #categories/
    url(r'^categories/$',views.CategoryList, name="category_index"),
    #categories/
    url(r'^categories/(?P<maincategory_id>[0-9]+)/$',views.SubCategoryList, name="subcategory_list"),
    #categories/add/
    url(r'^categories/add/$',views.addcategory,name="add_category"),
    #categories/123/add/
    url(r'^categories/(?P<maincategory_id>[0-9]+)/add/$',views.addsubcategory, name="add_subcategory"),
    #delete/income/1234/
    url(r'^delete/income/(?P<trans_id>[0-9]+)/$',views.delete_income, name="delete_income"),
    #delete/outcome/1234
    url(r'^delete/outcome/(?P<trans_id>[0-9]+)/$',views.delete_outcome, name="delete_outcome"),
    #delete/category/1213
    url(r'^delete/category/(?P<cat_id>[0-9]+)/$',views.delete_category,name="delete_category"),
    #delete/subcategory/1213
    url(r'^delete/subcategory/(?P<cat_id>[0-9]+)/$',views.delete_subCategory,name="delete_subCategory"),
    #edit/income/1234/
    url(r'^edit/income/(?P<trans_id>[0-9]+)/$',views.edit_income, name="edit_income"),
    #edit/outcome/1234
    url(r'^edit/outcome/(?P<trans_id>[0-9]+)/$',views.edit_outcome, name="edit_outcome"),
    #edit/subcategory/121
    url(r'^edit/subcategory/(?P<cat_id>[0-9]+)/$',views.edit_subCategory,name="edit_subCategory"),
    #edit/category/123
    url(r'^edit/category/(?P<cat_id>[0-9]+)/$',views.edit_category, name = "edit_category"),
]