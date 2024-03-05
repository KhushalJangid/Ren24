from .email_otp import send_otp_thread
import datetime
from django.contrib import messages
from django.shortcuts import redirect, render
import pytz
from account.models import OTP, User
from account.views import generateOTP
from django.contrib.auth import login


def resendOTP(request):
    '''This function resends otp, redirects to Verification of Forgot Password'''
    myuser=User.objects.get(id=request.session.get("id"))
    otp_obj= OTP.objects.get(user=myuser)
    otp_obj.otp = generateOTP()
    
    print(otp_obj.otp)
    otp_obj.created = datetime.datetime.now(pytz.UTC)
    otp_obj.expire=datetime.datetime.now(pytz.UTC)+datetime.timedelta(minutes=10)
    otp_obj.save()
    email=myuser.email
    otp=otp_obj.otp
    send_otp_thread(email,otp)
    messages.success(request,"OTP sent sucessfully")
    return redirect('resetpass_verify')

def verify(request):
    if request.method == 'POST':
        '''Step 4 of forgot password '''
        otp = request.POST.get('otp')
        user = User.objects.get(id=request.session.get("id"))  # Use get() to avoid KeyError
        otp_obj = OTP.objects.filter(user=user).first()  # Use filter() to handle None case
        if otp_obj:
            check_otp=str(otp_obj.otp)
            if otp==check_otp:  
                if datetime.datetime.now(pytz.UTC) > otp_obj.expire:
                    messages.warning(request, "OTP has expired")
                    return render(request, 'resetpass_verify.html')
                else:
                    return render(request, 'newpass.html')
                
            else:
                print(type(check_otp))
                print(type(otp))
                messages.error(request, 'Wrong OTP')
                return render(request, 'resetpass_verify.html')
        else:
            messages.error(request, 'Invalid OTP or user not found')  # Handle None case
            return render(request, 'resetpass_verify.html')
    else:
        '''Step 3 of forgot password '''
        return render(request, 'resetpass_verify.html')


    
def forgotpassword(request):
    if request.method=="POST" and 'email' in request.POST:
        '''Step 2 of forgot password '''
        email=request.POST['email']
        myuser=User.objects.filter(email=email).first()
        if not myuser:
            messages.error(request,"No account associated with this Email.")
            return redirect('home')
        otp_obj,created = OTP.objects.get_or_create(user=myuser)
        otp_obj.otp = generateOTP()
        otp=otp_obj.otp
        print(otp)
        send_otp_thread(email,otp)
        otp_obj.created = datetime.datetime.now(pytz.UTC)
        otp_obj.expire=datetime.datetime.now(pytz.UTC)+datetime.timedelta(minutes=10)
        otp_obj.save()
        request.session['id']=myuser.id
        return redirect('resetpass_verify')
    elif request.method == 'POST' and 'pass1' in request.POST:
        '''Step 5 (final) of forgot password '''
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        id=request.session.get('id')
        if pass1 != pass2:
                messages.error(request, "Passwords didn't matched!!")
                return render(request,'newpass.html')
        
        myuser = User.objects.get(id=id)
        myuser.set_password(pass1)
        myuser.save()
        login(request,myuser,backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')
    else:
        '''Step 1 of forgot password '''
        return  render(request,'entermobile.html')

# def newpass(request):
#     if request.method=='POST':
#         pass1=request.POST.get('pass1')
#         pass2=request.POST.get('pass2')
#         id=request.session.get("id")
#         if pass1 != pass2:
#             messages.error(request, "Passwords didn't matched!!")
#             return redirect('home')
#         myuser = User.objects.get(id=id)
#         myuser.set_password(pass1)
#         myuser.save()
#         return redirect('login')