# from email.message import EmailMessage
import base64
import io
from django.http import HttpResponse
from django.shortcuts import render,redirect
import pytz
from account.decorators import profile_required
from account.functions import getPass
from config import settings
from ticket.functions import generate_master_ticket, generate_ticket
from ticket.models import Ticket
from ticket.send_ticket import send_email_thread
from .models import *
from django.contrib import messages
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import login_required
import pyotp
import datetime
from .email_otp import send_otp_thread
from PIL import Image
 
# function to generate OTP
def generateOTP() :
 
    # Declare a digits variable  
    # which stores all digits 
    secret=pyotp.random_base32()
    otp = pyotp.TOTP(secret)
    return otp.now()


def register(request):
    """Create a new user account and send a confirmation email."""
    # check if the request is a POST method
    if request.method == "POST":
        # get the input data from the request
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        user=User.objects.filter(email=email)
        if  user.exists():
            messages.error(request, "Email Already Registered !!")
            return render(request, 'login.html')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't match !!")
            return render(request, 'signup.html')
        myuser = User.objects.create_user(email=email, 
                                          first_name=fname,
                                          last_name=lname,
                                          password=pass1,
                                          is_active=False)
        myuser.save()
        request.session['id'] = myuser.id
        
        # return a success message
        messages.success(request, "Your Account has been created succesfully!!")
        otp_obj,created = OTP.objects.get_or_create(user=myuser)
        otp_obj.otp = generateOTP()
        otp=otp_obj.otp
        otp_obj.created = datetime.datetime.now(pytz.UTC)
        otp_obj.expire=datetime.datetime.now(pytz.UTC)+datetime.timedelta(minutes=10)
        otp_obj.save()
        send_otp_thread(myuser,otp)
        return redirect('verify')
    
    # if the request is not a POST method, render a template with a form
    else:
        return render(request, 'signup.html')




def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        user = User.objects.filter(email=email).first()  # Use .first() instead of .exists()

        if user:
            if user.is_active:
                myuser = authenticate(request, id=user.id, password=password,)
                if myuser is not None:
                    login(request, user,backend="django.contrib.auth.backends.ModelBackend")
                    messages.success(request, "Logged in successfully")
                    # request.session['id'] = user.pk
                    return redirect('home')
                else:   
                    messages.error(request, "Incorrect Password")
                    return render(request,"login.html")
            else:
                messages.error(request, "User not verified")
                request.session['id'] = user.pk
                otp_obj,created = OTP.objects.get_or_create(user=User.objects.get(email=email))
                otp_obj.otp = generateOTP()  # Implement your OTP generation logic
                otp=otp_obj.otp
                otp_obj.created = datetime.datetime.now(pytz.UTC)
                otp_obj.expire=datetime.datetime.now(pytz.UTC)+datetime.timedelta(minutes=10)
                otp_obj.save()
                send_otp_thread(user,otp)   
                return redirect("verify")
        else:
            messages.error(request, "User with the email does not exist")
            return redirect('register')
    else:
        return render(request, "login.html")




def signout(request):
    logout(request)
    messages.success(request, "Logged Out Sucessfully")
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'GET':
        # get the current user's profile or create a new one
        profile= Profile.objects.filter(user=request.user)
        if profile.exists():
            profile = profile.first()
        # render the template with the profile data
            tickets = Ticket.objects.filter(user=request.user)
            ticket_img = []
            for ticket in tickets:
                ticket_img.append(base64.b64encode(generate_ticket(ticket.id)).decode('utf-8'))
            if profile.dob is not None:
                dob = profile.dob.strftime("%Y-%m-%d")
            else:
                dob = ''
            context = {
                'profile':profile,
                'dob':dob,
                'tickets':ticket_img
            }
            return render(request, 'profile.html',context)
        else:
            return render(request, 'profile.html')
    else:
        first_name=request.POST.get("fname")
        last_name=request.POST.get("lname")
        phone=request.POST.get("phone")
        dob=request.POST.get("dob")
        rollno=request.POST.get("rollno")
        gender=request.POST.get("gender")
        college=request.POST.get("college")
        address=request.POST.get("address")
        image = request.FILES.get("image")
        user_obj=request.user
        profile_obj,created=Profile.objects.get_or_create(user=user_obj)
        if created:
            user=request.user
            _pass = getPass(user)
            if not _pass:
                pass
            else:
                image_buffer =generate_master_ticket(user)
                tkt=Image.open(image_buffer)
                img_rgb=tkt.convert('RGB')
                pdf_buffer = io.BytesIO()
                img_rgb.save(pdf_buffer, 'PDF', resolution=100.0)
                send_email_thread(user,pdf_buffer)
                messages.success(request,"Ticket has been sent to your registered email")
        user_obj.first_name=first_name
        user_obj.last_name=last_name
        profile_obj.phone=phone
        profile_obj.dob=dob
        profile_obj.rollno=rollno
        profile_obj.gender= genders.get(gender)
        profile_obj.college=college
        profile_obj.address=address
        # profile_obj.user
        print(image)
        if image is not None and image != "":
            profile_obj.image = image
        profile_obj.save()
        user_obj.save()
        profile =request.user.profile
        # render the template with the profile data
        tickets = Ticket.objects.filter(user=request.user)
        ticket_img = []
        for ticket in tickets:
            ticket_img.append(base64.b64encode(generate_ticket(ticket.id)).decode('utf-8'))
        context = {
            'profile':profile,
            'dob':dob,
            'tickets':ticket_img
        }
        messages.success(request,"Profile updated Sucessfully")
        next = request.GET.get("next")
        if next:
            if next != '/u/send_ticket' and next != '/u/download_ticket':
                return redirect(next)
        return render(request,"profile.html",context)
          


def resendOTP(request):
    myuser=User.objects.get(id=request.session.get("id"))
    otp_obj= OTP.objects.get(user=myuser)
    otp_obj.otp = generateOTP()
    otp_obj.created = datetime.datetime.now(pytz.UTC)
    otp_obj.expire=datetime.datetime.now(pytz.UTC)+datetime.timedelta(minutes=10)
    otp=otp_obj.otp
    otp_obj.save()
    send_otp_thread(myuser,otp)   
    messages.success(request,"OTP sent sucessfully")
    return redirect('verify')

def verify(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user = User.objects.get(id=request.session.get("id"))  # Use get() to avoid KeyError
        otp_obj = OTP.objects.filter(user=user).first()  # Use filter() to handle None case
        check_otp=str(otp_obj.otp)
        if otp==check_otp:  
            if datetime.datetime.now(pytz.UTC) > otp_obj.expire:
                messages.warning(request, "OTP has expired")
                return resendOTP(request)
            user.is_active=True
            user.save()
            login(request, user,backend="django.contrib.auth.backends.ModelBackend")
            return redirect('home')
            
        else:
            messages.error(request, 'Wrong OTP')
            return render(request, 'verify.html')
    else:
        return render(request, 'verify.html')

@login_required
@profile_required('/u/profile')
def send_ticket(request):
    if request.method=='POST':
        user=request.user
        _pass = getPass(user)
        if not _pass:
            messages.error(request,"Your Ren Pass is not activated yet, Please try again later")
            return redirect('profile')
        email=user.email
        image_buffer =generate_master_ticket(user)
        image=Image.open(image_buffer)
        img_rgb=image.convert('RGB')
        pdf_buffer = io.BytesIO()
        img_rgb.save(pdf_buffer, 'PDF', resolution=100.0)
        send_email_thread(user,pdf_buffer)
        messages.success(request,"Ticket has been sent to your registered email")
        return redirect('profile')
    else:
        return HttpResponse('Method not allowed',status=400)

@login_required
@profile_required('/u/profile')
def download_ticket(request):
    if request.method == 'POST':
        user = request.user
        _pass = getPass(user)  # Assuming `getPass` retrieves user's pass information
        if not _pass:
            messages.error(request, "Your Ren Pass is not activated yet, Please try again later")
            return redirect('profile')

        image_buffer =generate_master_ticket(user) # Assuming `generate_master_ticket` creates the image
        image = Image.open(image_buffer)
        img_rgb = image.convert('RGB')

        # Set the response as a PDF download
        response = HttpResponse(content_type='application/pdf')
        pdfbuffer = io.BytesIO()
        img_rgb.save(pdfbuffer, 'PDF', resolution=100.0)
        response.content = pdfbuffer.getvalue()
        response['Content-Disposition'] = f'attachment; filename=ticket_{user.email}.pdf'
        return response
    else:
        return HttpResponse('Method not allowed',status=400)
        

        
        