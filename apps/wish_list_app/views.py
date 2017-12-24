from django.shortcuts import render, HttpResponse, redirect
from models import Wish
from django.contrib import messages
from .. login_app.models import User




def index(request):
	print "------##############  inside TRIP APP INDEX route ##################----------"
	print request.session['user']['id'],"<------------------here's the user_id"
	'''current_user_trips= User.objects.get(id =request.session['user']['id']).trips.all()
	current_user_trips =current_user_trips.values('id','users','destination','start_date','end_date', 'plan').distinct()'''

	
	current_user= User.objects.get(id=request.session['user']['id'])
	

	wishes = Wish.objects.all()
	wishes = wishes.values('id', 'item', 'added_by', 'users__id')
	#print wishes

	user = User.objects.get(id=request.session['user']['id'])
	#print type(user)

	user_items= user.wishes.all()
	#print type(user_items)
	user_items=user_items.values('id','item', 'added_by', 'created_at')
	#print dir(user_items)
	

	z = user_items.values('id')
	print dir(z)
	#print z, "zzzzzzzzzzzzzzzz"

	non_user_items= Wish.objects.exclude(id__in=z)
	#print type(non_user_items)
	non_user_items= non_user_items.values('id','item', 'added_by', 'created_at')
	#print non_user_items
	#print items, "non............."


	context= {

		"non_user_items":non_user_items, 	# -all the items the current user did not create
		"user_items":user_items, 			# -all the items the current user created
		"current_user":current_user, 		# -current user that is signed in
		"wishes": wishes,  					# -all the current items in the Wish model (item, added_by, created_at)
		#"users":users
		

	}

	

	return render(request, 'wish_list_app/index.html', context)




def create_wish(request):
	print "VIEWS...........................................   create a wish"


	return render(request, 'wish_list_app/create_wish.html')


def add_wish(request, methods='POST'):

	print "VIEWS.....................................where the wish is posted"
	print request.session['user']['id'],"<------------------here's the user_id"
	print request.POST['wish']

	response = Wish.objects.add_wish(request,request.POST)

	

	

		
	return redirect('wish_list_app:index')




def join_wish(request, number, methods='POST'):

	print "VIEWS...........................................add to wishlist"
	request.session['number']= number

	print number


	join_wish = Wish.objects.join_wish(request,request.POST)

	if join_wish[0]== False:
		for message in join_wish[1]: #saying  for message in errors:
			print "errors on the add wish form"
			messages.error(request, message[1])
		return redirect('wish_list_app:index')

	else:
		print join_wish[0]
		print join_wish[1]
		return redirect('wish_list_app:index')



	
	return redirect('wish_list_app:index')


def show_wish(request,number):
	print "VIEWS...........................................   show the wish list item"


	
	item=Wish.objects.get(id=number)

	print item.item, "heres the asshole userr"

	users_who_wished= item.users.all()
	print users_who_wished

	context= {

		'item':item,
		"users_who_wished":users_who_wished
	}


	return render(request, 'wish_list_app/show_wish.html', context)


def remove(request,number):
	#render delete webpage, and grabs the id that will be deleted via the context dictionary
	print number, "<----here is the item ID/number to be deleted---------------"
	print request

	

	request.session['number']= number

	context= {

		'item': Wish.objects.get(id=number)
	
	}

	
	
	return render(request, 'wish_list_app/remove.html', context)

	

def confirm_remove(request,number, methods='POST'):
	# uses the delete_info() method to delete user
	print "< ------------------this is where we confirm the delete----------------"

	response = Wish.objects.remove(request,request.POST)

	return redirect('wish_list_app:index')



def delete(request,number):
	#render delete webpage, and grabs the id that will be deleted via the context dictionary
	print number, "<----here is the item ID/number to be deleted---------------"
	print request

	

	request.session['number']= number

	context= {

		'item': Wish.objects.get(id=number)
	
	}

	
	
	return render(request, 'wish_list_app/delete.html', context)

	

def confirm_delete(request,number, methods='POST'):
	# uses the delete_info() method to delete user
	print "< ------------------this is where we confirm the delete----------------"

	response = Wish.objects.delete(request,request.POST)

	return redirect('wish_list_app:index')









def clear(request):
	print '----------------            CLEARING THE SESSION         ---------------------'

	request.session.clear()

	return redirect('login_app:index')
