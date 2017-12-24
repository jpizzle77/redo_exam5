from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib import messages
import re
import bcrypt
from datetime import datetime


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

def User(request):
		users= User.objects.all()
		for user in users:
			return user

class User_DB_Manager(models.Manager):

	def check_create(self, request, data):
		print "inside the validate_info() method"

		def number(string):
			return re.search('\d', string)

		errors=[]
	

		if len(data['name']) < 1: 
			errors.append(['first_name',"First name cannot be empty or contain numbers!"])
		if number(data['name']):
			errors.append(['first_name','No numbers are allowed for first name'])
			
		if len(data['alias']) < 1:
			errors.append(['last_name',"Last name cannot be empty or contain numbers!"])
		if number(data['alias']):
			errors.append(['last_name','No numbers are allowed for last name'])
			
		if len(data['email']) < 1:
			errors.append(['email','email',"Email name cannot be empty and must be a valid email!"]) 
		if not EMAIL_REGEX.match(data['email']):
			errors.append(['email',"Invalid Email Address!"])

		if len(data['password']) < 1:
			errors.append(['password',"Password cannot be empty!"])
			
		if data['password'] != data['confirm_password']:
			errors.append(['confirm_password','passwords no match!'])

		if errors:
			return [False, errors]

		else:
			print "yo yo ma"
			email_exist = User.objects.filter(email = data['email']) #checking to see if email already exists in the DB
			if email_exist:
				errors.append(['email','email needs to be unique'])
				return [False, errors]
			
			#the point where we have passed all the validations, plus made sure no one else had the same email address. Now we can create a user
			else:
				new_user = User(name=data['name'], alias=data['alias'], email=data['email'], birthday=data['birthday'])
				hashed= bcrypt.hashpw(data['password'].encode(),bcrypt.gensalt())
				new_user.password = hashed
				new_user.save()
				return [True, new_user]

	def check_password(self,request, data):
		print "inside the check_password()"
		print data['pwd']
		errors=[]
		current_user = User.objects.filter(email = data['email'])
		print current_user, "<---here is the current user"
		
		try:
			if current_user[0]:
				print "there is someone in databse"

				if bcrypt.checkpw(data['pwd'].encode(), current_user[0].password.encode()):
					print "passwords match"
					return [True, current_user[0]]
				else:
					print "passwords no match "
					errors.append(["login", "please enter a valid email or correct password"])
					return [False, errors]

		except:
			print "no one in DB"
			errors.append(["login", "please enter a valid email or correct password"])
			return [False, errors]


			
class User(models.Model):
	#username = models.CharField(max_length=255, unique= TRUE)
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	birthday = models.DateField(null=True, blank=True)
	password= models.CharField(max_length=255)
	confirm_password= models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True, null=True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = User_DB_Manager()
	

	def __repr__(self):
		return "<Name: {} Alias:{} Email:{} >".format(self.name, self.alias, self.email)
