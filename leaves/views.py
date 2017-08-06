from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages

from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
from django.views import View

from .models import LeaveType, UserProfile, LeaveTaken, TempLeaveType

from django.contrib.auth.forms import AuthenticationForm 
from django import forms
# Create your views here.
from django.db.models import Count
from datetime import date, datetime
import urllib.parse


@login_required(login_url='/login/')
def home_view(request):
	template_name = "index.html"
	current_user = request.user
	profile = request.user.userprofile
	qs = LeaveType.objects.filter(owner=current_user)
	tqs = TempLeaveType.objects.filter(owner=current_user)
	print(current_user)
	print(qs)
	bday1 = []
	bday2 = []
	mydate = datetime.now()
	cur_month = mydate.strftime("%B")
	cur_date = mydate.strftime("%d")
	a  = User.objects.all()
	try:
		for i in range(0,5):
			x1 = a[i].userprofile.birth_date.strftime("%B")
			x2 = a[i].userprofile.birth_date.strftime("%d")
			if x1 == cur_month and x2 >= cur_date:
				x = str(a[i].userprofile.birth_date.strftime("%d %B"))
				y = str(a[i].first_name + " " + a[i].last_name)
				bday1.append(x)
				bday2.append(y)
	except:
		print("Birthday Exception")
		
	print(bday1)
	print(bday2)
	ziplist = zip(bday1, bday2)
	ziplis = sorted(ziplist)
	applied = 'yes'
	context = {"message":" Succesfully applied",
				"hod_name":"a",
				"fa_name": qs[0].name ,
				"message": "Success",
				"cl":qs[0].CL,
				"el": qs[0].EL,
				"rh":qs[0].RH,
				"fa_desig": str(profile.designation),
				"applied": applied,
				"tcl":tqs[0].TCL,
				"tel": tqs[0].TEL,
				"trh":tqs[0].TRH,
				"bday":ziplis,
	}
	return render(request, "index.html", context)

@login_required(login_url='/login/')
def apply_view(request):
	template_name = "apply.html"
	current_user = request.user
	profile = request.user.userprofile
	print(profile.hod)
	qs = LeaveType.objects.filter(owner=current_user)
	tqs = TempLeaveType.objects.filter(owner=current_user)
	context = {
				"message":"Succesfully applied",
				"hod_name":"a",
				"fa_name": qs[0].name ,
				"fa_dep": profile.dep,
				"fa_desig": profile.designation,

	}
	if request.method == 'POST':
		print(request.POST)
		category 	= request.POST.get("cat")
		days		= request.POST.get("totald")
		fromdate 	= request.POST.get("fromDate")
		enddate 	= request.POST.get("endDate")

		if category == 'Casual Leave':
			new 	= qs[0].CL
			tnew 	= tqs[0].TCL		
			cat 	= 1
			if int(tnew) + int(days) <= new:
				tnew 	= tnew + int(days)
				print(tnew)
				TempLeaveType.objects.filter(owner=current_user).update(TCL=tnew)
				obj = LeaveTaken.objects.create(
				user 		= current_user, 
				category 	= cat,
				dateStart 	= fromdate,
				dateEnd 	= enddate,
				)
				category = urllib.parse.quote(category)
				email = EmailMessage(
					'Leave Application ' + qs[0].name + ' ' + fromdate, 
					'Hi,\n\n' + qs[0].name + ' has applied for leave, please view and approve or reject using the link below.\nLink: http://localhost:8000/approvals/' + current_user.username + '/' + category.lower() + '/' + fromdate + '/' + enddate + '/' + days + '/\n\nThanks,\nFLM-BMSIT' , 
					'FLM Support <support@backbenchertech.com>', 
					['HOD EMAIL'],
					cc=[current_user.email],
					)
				email.send()
				print("Mail sent")
				messages.success(request, ' Casual Leave applied successfully for ' + days + ' days. View status in "My Leaves"')
				return HttpResponseRedirect("/")
			else:
				return HttpResponseRedirect("/exhausted/?q=" + category)
		elif category == 'Earned Leave':
			new 	= qs[0].EL
			tnew 	= tqs[0].TEL
			cat 	= 2
			if int(tnew) + int(days) <= new:
				tnew 	= tnew + int(days)
				TempLeaveType.objects.filter(owner=current_user).update(TEL=tnew)
				obj = LeaveTaken.objects.create(
				user 		= current_user, 
				category 	= cat,
				dateStart 	= fromdate,
				dateEnd 	= enddate,
				)
				#TODO: IMPLEMENT CL EMAIL TECHNIQUE
				return HttpResponseRedirect("/")
			else:
				return HttpResponseRedirect("/exhausted/?q=" + category)
		elif category == 'Special Casual Leave':
			new 	= qs[0].SCL
			tnew 	= tqs[0].TSCL
			cat 	= 3
			if int(tnew) + int(days) <= new:
				tnew 	= ttnew + int(days)
				TempLeaveType.objects.filter(owner=current_user).update(TSCL=tnew)
				obj = LeaveTaken.objects.create(
				user 		= current_user, 
				category 	= cat,
				dateStart 	= fromdate,
				dateEnd 	= enddate,
				)
				return HttpResponseRedirect("/")
			else:
				return HttpResponseRedirect("/exhausted/?q=" + category)
		elif category == 'Maternity Leave':
			new 	= qs[0].ML
			tnew 	= tqs[0].TML
			cat 	= 4
			if int(tnew) + int(days) <= new:
				tnew 	= tnew + int(days)
				TempLeaveType.objects.filter(owner=current_user).update(TML=tnew)
				obj = LeaveTaken.objects.create(
				user 		= current_user, 
				category 	= cat,
				dateStart 	= fromdate,
				dateEnd 	= enddate,
				)
				return HttpResponseRedirect("/")
			else:
				return HttpResponseRedirect("/exhausted/?q=" + category)
		elif category == 'Reserved Holiday':
			new 	= qs[0].RH
			tnew 	= tqs[0].TRH
			cat 	= 5
			if int(tnew) + int(days) <= new:
				tnew 	= tnew + int(days)
				TempLeaveType.objects.filter(owner=current_user).update(TRH=tnew)
				obj = LeaveTaken.objects.create(
				user 		= current_user, 
				category 	= cat,
				dateStart 	= fromdate,
				dateEnd 	= enddate,
				)
				return HttpResponseRedirect("/")
			else:
				return HttpResponseRedirect("/exhausted/?q=" + category)
		
	return render(request, template_name, context)
@login_required(login_url='/login/')
def account_view(request):
	template_name = "account.html"
	current_user = request.user
	profile = request.user.userprofile
	context = {
				"fa_name": profile.user.first_name + " " + profile.user.last_name,
				"fa_dep": profile.dep,
				"fa_desig": profile.designation,
	}
	return render(request, template_name, context)

@login_required(login_url='/login/')
def help_view(request):
	template_name = "help.html"
	current_user = request.user
	profile = request.user.userprofile
	context = {
				"fa_name": profile.user.first_name + " " + profile.user.last_name,
				"fa_dep": profile.dep,
				"fa_desig": profile.designation,
	}
	if request.method == 'POST':
		name1 	= request.POST.get("fname")
		desig 	= request.POST.get("fdesig")
		query 	= request.POST.get("contact_body")
		email = EmailMessage(
		'Contact Support ' + str(name1), 
		'Hi,\n\nQuery:\n' + str(query)+'\n\nThanks,\n' + str(name1) + '\n' + desig, 
		current_user.email, 
		['FLM Support <support@backbenchertech.com>'],
		cc=[current_user.email],
		)
		email.send()
		messages.success(request, ' Message sent to administrator. Check your email for more details.')
		return HttpResponseRedirect('/')
	return render(request, template_name, context)

@login_required(login_url='/login/')
def exhausted_view(request):	
	template_name = "notRemaining.html"
	current_user = request.user
	profile = request.user.userprofile
	Type = request.GET.get('q', '')
	print(Type)
	context = {
				"fa_name": profile.user.first_name + " " + profile.user.last_name,
				"fa_dep": profile.dep,
				"fa_desig": profile.designation,
				"type": Type,
	}
	return render(request, template_name, context)

@login_required(login_url='/login/')
def my_leave_view(request):
	template_name = "my_leaves.html"
	current_user = request.user
	profile = request.user.userprofile
	qs = LeaveTaken.objects.filter(user=current_user).order_by('-dateStart')
	print(qs[0].dateStart)
	upcoming = []
	past = []
	for i in qs:
		i.approval = str(i.approval)
		if i.dateStart > date.today():
			upcoming.append(i)
		else:
			past.append(i)
	context = {
		"hod_name":"a",
		"fa_name": profile.user.first_name + " " + profile.user.last_name,
		"fa_dep": profile.dep,
		"fa_desig": profile.designation,
		"upcoming": upcoming,
		"past": past,

	}
	#To display past leaves, qs = LeaveTaken.objects.filter(owner=current_user)
	return render(request, template_name, context)

@login_required(login_url='/login/')
def approval_view(request, name, cat, fromd, endd, days):
	print(fromd + ' ' + name)
	template_name = "approval.html"
	current_user = request.user
	profile = request.user.userprofile
	#TODO: Load only if desig == HOD
	'''
	qs = LeaveTaken.objects.filter(user=current_user).order_by('-dateStart')
	
		Show the url params on page.
		Two buttons -Approve and reject,
		if approve - 
	
		if approve = true, Update LeaveType Table with TempLeaveType values
		else reset TempLeaveType and send email saying that it is rejected.

	'''
	fromdate1 	= '-'.join(fromd.split('-')[::-1])
	enddate1 	= '-'.join(endd.split('-')[::-1])
	u = User.objects.get(username=name)
	context = {
		"fa_name"	: profile.user.first_name + " " + profile.user.last_name,
		"fa_dep"	: profile.dep,
		"fa_desig"	: profile.designation,
		"category"	: cat,
		"name"		: u.first_name + ' ' + u.last_name,
		"fromd"		: fromdate1,
		"endd"		: enddate1,

	}
	if request.method == 'POST':
		status	 	= request.POST.get("approval")
		status		= status.upper()
		qs 			= LeaveType.objects.filter(owner=u)
		tqs 		= TempLeaveType.objects.filter(owner=u)
		category 	= cat.upper()
		fromdate 	= fromd
		enddate 	= endd
		if status 	== 'ACCEPT':				#TODO: Implement Reject, decrement temp
			if category == 'CASUAL LEAVE':
				new = qs[0].CL
				tnew = tqs[0].TCL
				print(new)
				cat = 1
				if int(new) > int(days) or int(new) == int(days):
					new = new - int(days)
					tnew = tnew - int(days)
					LeaveType.objects.filter(owner=u).update(CL=new)
					TempLeaveType.objects.filter(owner=u).update(TCL=tnew)
					obj = LeaveTaken.objects.filter(
					user 		= u, 
					category 	= cat,
					dateStart 	= fromdate,
					dateEnd 	= enddate,
					).update(approval 	= 'True')
					fromdate 	= '-'.join(fromdate.split('-')[::-1])
					enddate 	= '-'.join(enddate.split('-')[::-1])
					email = EmailMessage(
						'[Approved] Leave Application: ' + u.first_name + ' ' + u.last_name + ' ' + fromdate, 
						'Your Leave Application has been approved. \n Category: '+ category.title() + '\n From: '+fromdate  + '\n To: ' + enddate + '\n' , 
						'support@backbenchertech.com', 
						[current_user.email],
						cc=['HOD EMAIL'],
					)
					email.send()
					print("Mail sent")
					messages.success(request, ' Approved')
					return HttpResponseRedirect("/")
				else:
					return HttpResponseRedirect("/exhausted/?q=" + category)
			elif category == 'EARNED LEAVE':
				new = qs[0].EL
				tnew = tqs[0].TEL
				cat = 2
				if int(new) > int(days) or int(new) == int(days):
					new = new - int(days)
					tnew = tnew - int(days)
					LeaveType.objects.filter(owner=u).update(EL=new)
					TempLeaveType.objects.filter(owner=u).update(TEL=tnew)
					obj = LeaveTaken.objects.filter(
					user 		= u, 
					category 	= cat,
					dateStart 	= fromdate,
					dateEnd 	= enddate,
					).update(approval 	= 'True')
					fromdate 	= '-'.join(fromdate.split('-')[::-1])
					enddate 	= '-'.join(enddate.split('-')[::-1])
					email = EmailMessage(
							'[Approved] Leave Application: ' + u.first_name + ' ' + u.last_name + ' ' + fromdate, 
							'Your Leave Application has been approved. \n Category: '+ category.title() + '\n From: '+fromdate  + '\n To: ' + enddate + '\n' , 
							'support@backbenchertech.com', 
							[current_user.email],
							cc=['HOD EMAIL'],
						)
					email.send()
					print("Mail sent")
					messages.success(request, ' Approved')
					return HttpResponseRedirect("/")
				else:
					return HttpResponseRedirect("/exhausted/?q=" + category)
			elif category == 'SPECIAL CASUAL LEAVE':
				new = qs[0].SCL
				tnew = tqs[0].TSCL
				cat = 3
				if int(new) > int(days) or int(new) == int(days):
					new = new - int(days)
					tnew = tnew - int(days)
					LeaveType.objects.filter(owner=u).update(SCL=new)
					TempLeaveType.objects.filter(owner=u).update(TSCL=tnew)
					obj = LeaveTaken.objects.filter(
					user 		= u, 
					category 	= cat,
					dateStart 	= fromdate,
					dateEnd 	= enddate,
					).update(approval 	= 'True')
					fromdate 	= '-'.join(fromdate.split('-')[::-1])
					enddate 	= '-'.join(enddate.split('-')[::-1])
					email = EmailMessage(
							'[Approved] Leave Application: ' + u.first_name + ' ' + u.last_name + ' ' + fromdate, 
							'Your Leave Application has been approved. \n Category: '+ category.title() + '\n From: '+fromdate  + '\n To: ' + enddate + '\n' , 
							'support@backbenchertech.com', 
							[current_user.email],
							cc=['HOD EMAIL'],
						)
					email.send()
					print("Mail sent")
					messages.success(request, ' Approved')
					return HttpResponseRedirect("/")
				else:
					return HttpResponseRedirect("/exhausted/?q=" + category)
			elif category == 'MATERNITY LEAVE':
				new = qs[0].ML
				tnew = tqs[0].TML
				cat = 4
				if int(new) > int(days) or int(new) == int(days):
					new = new - int(days)
					tnew = tnew - int(days)
					LeaveType.objects.filter(owner=u).update(ML=new)
					TempLeaveType.objects.filter(owner=u).update(TML=tnew)
					obj = LeaveTaken.objects.filter(
					user 		= u, 
					category 	= cat,
					dateStart 	= fromdate,
					dateEnd 	= enddate,
					).update(approval 	= 'True')
					fromdate 	= '-'.join(fromdate.split('-')[::-1])
					enddate 	= '-'.join(enddate.split('-')[::-1])
					email = EmailMessage(
							'[Approved] Leave Application: ' + u.first_name + ' ' + u.last_name + ' ' + fromdate, 
							'Your Leave Application has been approved. \n Category: '+ category.title() + '\n From: '+fromdate  + '\n To: ' + enddate + '\n' , 
							'support@backbenchertech.com', 
							[current_user.email],
							cc=['HOD EMAIL'],
						)
					email.send()
					print("Mail sent")
					messages.success(request, ' Approved')
					return HttpResponseRedirect("/")
				else:
					return HttpResponseRedirect("/exhausted/?q=" + category)
			elif category == 'RESERVED HOLIDAY':
				new = qs[0].RH
				tnew = tqs[0].TRH
				cat = 5
				if int(new) > int(days) or int(new) == int(days):
					new = new - int(days)
					tnew = tnew - int(days)
					LeaveType.objects.filter(owner=u).update(RH=new)
					TempLeaveType.objects.filter(owner=u).update(TRH=tnew)
					obj = LeaveTaken.objects.filter(
					user 		= u, 
					category 	= cat,
					dateStart 	= fromdate,
					dateEnd 	= enddate,
					).update(approval 	= 'True')
					fromdate 	= '-'.join(fromdate.split('-')[::-1])
					enddate 	= '-'.join(enddate.split('-')[::-1])
					email = EmailMessage(
							'[Approved] Leave Application: ' + u.first_name + ' ' + u.last_name + ' ' + fromdate, 
							'Your Leave Application has been approved.\n\n Category: '+ category.title() + '\n From: '+fromdate  + '\n To: ' + enddate + '\n' , 
							'support@backbenchertech.com', 
							[current_user.email],
							cc=['HOD EMAIL'],
						)
					email.send()
					print("Mail sent")
					messages.success(request, ' Approved')
					return HttpResponseRedirect("/")
				else:
					return HttpResponseRedirect("/exhausted/?q=" + category)

		elif status 	== 'REJECT':
			if category == 'CASUAL LEAVE':
				tnew = tqs[0].TCL
				if tnew > 0:
					tnew = tnew - int(days)
					TempLeaveType.objects.filter(owner=u).update(TCL=tnew)
					fromdate 	= '-'.join(fromdate.split('-')[::-1])
					enddate 	= '-'.join(enddate.split('-')[::-1])
					email = EmailMessage(
								'[Rejected] Leave Application: ' + u.first_name + ' ' + u.last_name+ ' ' +fromdate, 
								'Your Leave Application has been rejected. Please contact HoD for further information.\n\nCategory: '+ category.title() + '\nFrom: '+fromdate  + '\nTo: ' + enddate + '\n\nThanks,\nFLM-BMSIT' , 
								'support@backbenchertech.com', 
								[current_user.email],
								cc=['HOD EMAIL'],
							)
					email.send()
					print("CL Reject Mail sent")
				return HttpResponseRedirect("/")
			if category == 'EARNED LEAVE':
				tnew = tqs[0].TEL
				if tnew > 0:
					tnew = tnew - int(days)
					TempLeaveType.objects.filter(owner=u).update(TCL=tnew)
					fromdate 	= '-'.join(fromdate.split('-')[::-1])
					enddate 	= '-'.join(enddate.split('-')[::-1])
					email = EmailMessage(
								'[Rejected] Leave Application:' + u.first_name + ' ' + u.last_name+ ' ' +fromdate, 
								'Your Leave Application has been rejected. Please contact HoD for further information.\n\nCategory: '+ category.title() + '\nFrom: '+fromdate  + '\nTo: ' + enddate + '\n\nThanks,\nFLM-BMSIT' , 
								'support@backbenchertech.com', 
								[current_user.email],
								cc=['HOD EMAIL'],
							)
					email.send()
					print("EL Reject Mail sent")
				return HttpResponseRedirect("/")
			if category == 'SPECIAL CASUAL LEAVE':
				tnew = tqs[0].TSCL
				if tnew > 0:
					tnew = tnew - int(days)
					TempLeaveType.objects.filter(owner=u).update(TCL=tnew)
					fromdate 	= '-'.join(fromdate.split('-')[::-1])
					enddate 	= '-'.join(enddate.split('-')[::-1])
					email = EmailMessage(
								'[Rejected] Leave Application:' + u.first_name + ' ' + u.last_name+ ' ' + fromdate, 
								'Your Leave Application has been rejected. Please contact HoD for further information.\n\nCategory: '+ category.title() + '\nFrom: '+fromdate  + '\nTo: ' + enddate + '\n\nThanks,\nFLM-BMSIT' , 
								'support@backbenchertech.com', 
								[current_user.email],
								cc=['HOD EMAIL'],
							)
					email.send()
					print("SCL Reject Mail sent")
				return HttpResponseRedirect("/")
			if category == 'MATERNITY LEAVE':
				tnew = tqs[0].TML
				if tnew > 0:
					tnew = tnew - int(days)
					TempLeaveType.objects.filter(owner=u).update(TCL=tnew)
					fromdate 	= '-'.join(fromdate.split('-')[::-1])
					enddate 	= '-'.join(enddate.split('-')[::-1])
					email = EmailMessage(
								'[Rejected] Leave Application:' + u.first_name + ' ' + u.last_name + ' ' + fromdate, 
								'Your Leave Application has been rejected. Please contact HoD for further information.\n\nCategory: '+ category.title() + '\nFrom: '+fromdate  + '\nTo: ' + enddate + '\n\nThanks,\nFLM-BMSIT' , 
								'support@backbenchertech.com', 
								[current_user.email],
								cc=['HOD EMAIL'],
							)
					email.send()
					print("ML Reject Mail sent")
				return HttpResponseRedirect("/")
			if category == 'RESTRICTED HOLIDAY':
				tnew = tqs[0].TRH
				if tnew > 0:
					tnew = tnew - int(days)
					TempLeaveType.objects.filter(owner=u).update(TCL=tnew)
					fromdate 	= '-'.join(fromdate.split('-')[::-1])
					enddate 	= '-'.join(enddate.split('-')[::-1])
					email = EmailMessage(
								'[Rejected] Leave Application' + u.first_name + ' ' + u.last_name+ ' ' + fromdate, 
								'Your Leave Application has been rejected. Please contact HoD for further information.\n\nCategory: '+ category.title() + '\nFrom: '+fromdate  + '\nTo: ' + enddate + '\n\nThanks,\nFLM-BMSIT' , 
								'support@backbenchertech.com', 
								[current_user.email],
								cc=['HOD EMAIL'],
							)
					email.send()
					print("RH Reject Mail sent")
				return HttpResponseRedirect("/")

	#Display temp table value of each faculty whose temp table field is non zero, on approval decrement master table by temp table field value 
	# Show all leaves as  a group, comment feature on disaaproving to let HOD tell them to remove some category
	# if reject reset temp table
	# we can add clstartdate, clenddate...rhstartdate,rhenddate to temp model to store dates
	return render(request, template_name, context)


class LoginForm1(AuthenticationForm):
	username = forms.CharField(label="Username", max_length=30, 
							   widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder': 'Username'}))
	password = forms.CharField(label="Password", max_length=30, 
							   widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder': 'Password'}))


