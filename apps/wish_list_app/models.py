from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from ..login_app.models import User



class WishManager(models.Manager):
	

	def join_wish(self,request,data):
		print "MODELS..............................join_wish()"
		print data, "Data ............"

		errors=[]

		user= User.objects.get(id=request.session['user']['id'])
		print user.id, "The user that will be adding to his/her wishlist"

		wishes_joined =user.wishes.filter(id=request.session['number'])
		print wishes_joined, "Here's the wishes the user has or has not joined"

		if wishes_joined:
			print "This user has added this item to there wishlist already"
			errors.append([request,"You already have this on your wishlist!!"])
			return [False, errors]

		else:
			print "you can add this to your wishlist"
			item=Wish.objects.get(id=request.session['number'])
			x= user.wishes.add(item)

			

			return [True, item]



	def delete(self,request,data):
		print "MODELS...................................delete wish-list item"
		
		item= Wish.objects.get(id=request.session['number'])
		item.delete()

		return request


	def remove(self,request,data):
		print "MODELS...................................remove wish-list item"
		
		#SomeModel.objects.filter(id=id).delete()
		item = Wish.objects.filter(id=request.session['number'])
		item.delete()

		return request

class Wish_plannerManager(models.Manager):
	def add_wish(self,request,data):
		print "MODELS..........................add wish"
		print data
		user= User.objects.get(id=request.session['user']['id'])
		item = Wish(item= data['wish'], added_by= request.session['user']['name'])
		
		item.save()

		#x= user.friends.add(friend1.id)

		x= user.wishes.add(item.id)


		print item.id
		print item.added_by
		
	
		return request
	'''def create_trip(self,request,data):
		print "inside the create_trip() method"
		print data, "heres some data to look at"
		trip = Trip(destination=data['destination'], start_date=data['start_date'],end_date=data['end_date'],plan=data['plan'])#,trip_maker=data['trip_maker'])
		print data['trip_maker']
		trip.save()
		print trip.destination
	 	person_creating_trip=User.objects.get(id=request.session['user']['id'])
	 	print person_creating_trip.name
	 	x= Trip_planner(user=person_creating_trip, trips= trip, trip_maker=data['trip_maker'])
		x.save()
		print x
		return [trip,x]'''
		return request
		

class Wish(models.Model):
	item = models.CharField(max_length=255)
	added_by = models.CharField(max_length=255)
	users = models.ManyToManyField(User,  related_name="wishes", through="Wish_maker")
	created_at = models.DateTimeField(auto_now_add = True, null=True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = WishManager()

	

	def __repr__(self):
		return "<ID: {}-Item: {}- Aded by:{}- Users{}-  >".format(self.id, self.item, self.added_by, self.users)


class Wish_maker(models.Model):
    user = models.ForeignKey(User)
    wishes = models.ForeignKey(Wish)
    wish_maker = models.BooleanField(default=False)
   
    objects = Wish_plannerManager()

    def __repr__(self):
		return "<User Id: {}- Wish Id:{}- Wish Maker:{}- >".format(self.user, self.wishes, self.wish_maker)
