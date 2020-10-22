from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import*
# Create your views here.

def index(request):
    pass
    return render(request, "index.html")

def register(request):
    print(request.POST)
    resultFromValidator = User.objects.registerValidator(request.POST)
    print ("RESULTS FROM THE VALIDATOR BELOW")
    print (resultFromValidator)
    # if there are any error messages, the length of resultFromValidator will be greater than 0
    if len(resultFromValidator)>0:
        # for each error message, we are sending the message to the messages framework that allows us to send messages to the HTML for one refresh
        for key, value in resultFromValidator.items():
            messages.error(request, value)
        # after storing the error messages in the messages framework, redirect to the route that takes us to the form
        return redirect('/')
    # if the form is filled out properly, information from the form can be used to create a new user
    newUser = User.objects.create(name= request.POST['name'], username = request.POST['uname'], password = request.POST['pw'])
    print("HERE IS THE NEW USER OBJECT THAT WAS CREATED")
    print(newUser.id)
    request.session['loggedInId'] = newUser.id

    # redirect on post request
    return redirect("/success")

def login(request):
    print(request.POST)
    resultFromValidator = User.objects.loginValidator(request.POST)
    print("PRINTING THE LOGIN VALIDATOR RESULTS")
    print(resultFromValidator)
    if len(resultFromValidator)>0:
        for key, value in resultFromValidator.items():
            messages.error(request, value)
        return redirect("/")
    # if we are here that means login was valid
    userMatch = User.objects.filter(username = request.POST['uname'])
    request.session['loggedInId'] = userMatch[0].id

    return redirect('/success')
    

def home(request):
    loggedInUser = User.objects.get(id = request.session['loggedInId'])
    context = {
        'loggedInUser' : loggedInUser,
        'allTrips': Trip.objects.all(),
        'favTrips': Trip.objects.filter(joiner = loggedInUser),
        'otherTrips': Trip.objects.exclude(joiner = loggedInUser)
    }
    return render(request, "home.html", context)

def logout(request):
    # clear the session (request.session)
    request.session.clear()
    return redirect("/")

def addTrip(request):
    return render(request, "addtrip.html")

def createTrip(request):
    print(request.POST)
    resultFromValidator = Trip.objects.tripValidator(request.POST)
    print(resultFromValidator)
    if len(resultFromValidator)>0:
        for key, value in resultFromValidator.items():
            messages.error(request, value)
        return redirect("/trips/add")
    newTrip = Trip.objects.create(destination = request.POST['dest'], start_date = request.POST['fdate'], end_date = request.POST['tdate'], description = request.POST['desc'], uploader = User.objects.get(id=request.session['loggedInId']))
    return redirect('/success')

def showTrip(request, tripID):
    context = {
        'tripToShow': Trip.objects.get(id=tripID)
    }
    return render(request, "tripinfo.html", context )

def join(request, tripID):
    # get the user instance
    loggedInUser = User.objects.get(id = request.session['loggedInId'])
    # get the trip instance
    this_trip = Trip.objects.get(id=tripID)
    # make many to many join
    this_trip.joiner.add(loggedInUser)
    return redirect('/success')

