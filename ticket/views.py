from datetime import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from account.decorators import profile_required
from account.functions import getPass
from account.models import Passes, User
from django.contrib.auth.decorators import login_required
from ticket.functions import generate_master_ticket
from .models import *
from django.contrib import messages
# Create your views here.

day1 = datetime.strptime('2024-3-19','%Y-%m-%d').date()
day2 = datetime.strptime('2024-3-20','%Y-%m-%d').date()
day3 = datetime.strptime('2024-3-21','%Y-%m-%d').date()

def qr(request,ticketId):
    _pass = Passes.objects.filter(psid=ticketId).first()
    if _pass:
        ticket = generate_master_ticket(User.objects.get(email=_pass.email))
        response = HttpResponse(ticket.getvalue(), content_type='image/png')
        return response
    else:
        messages.error(request,'Invalid ticket id')
        return redirect('home')
    
def event(request):
    if request.method == 'GET':
        _type = 'tech'
        _day = day1
        day = request.GET.get('day')
        typ = request.GET.get('type')
        if day:
            if day == '1':
                _day = day1
            elif day == '2':
                _day = day2
            elif day == '3':
                _day = day3
        if typ:
            _type = typ
        print(_type,typ,_day,day)
        events = Events.objects.filter(type=_type,date=_day)
        context = []
        meta = []
        i = 0
        for event in events:
            if i <3:
                meta.append(event)
            else:
                context.append(meta.copy())
                meta.clear()
                meta.append(event)
                i = 0
            i +=1
        if i<4:
            context.append(meta)
        return render(request,'event.html',{'events':context,'modal':events})

@login_required
@profile_required('/u/profile')
def buy(request,eventId):
    user = request.user
    _pass = getPass(user)
    if _pass == None:
        messages.error(request,'Ren Pass not activated')
        return redirect('events')
    event = Events.objects.filter(id=eventId)
    if event.exists():
        event = event.first()
        _type = event.type
        if not event.includedInPass:
            messages.error(request,'This event is not free with Ren Pass, Please contact SDC for Tickets')
            return redirect('events')
        if _type == 'tech' and _pass.technical != None:
            messages.error(request,'Technical event already used')
            return redirect('events')
        if _type == 'splash' and _pass.splash != None:
            messages.error(request,'Technical event already used')
            return redirect('events')
        if _type == 'tech':
            _pass.technical = event
            _pass.save()
            Ticket.objects.create(user=user,event=event)
            messages.success(request,f'Ticket for {event.name} generated succesfully !')
            return redirect('profile')
        if _type == 'splash':
            _pass.splash = event
            _pass.save()
            Ticket.objects.create(user=user,event=event)
            messages.success(request,f'Ticket for {event.name} generated succesfully !')
            return redirect('profile')
        

def custom(request,ticketId):
    ticket = CustomTicket.objects.filter(id=ticketId)
    if ticket.exists():
        ticket = ticket.first()
        # image = Image.open(ticket.generate_customticket())
        # img_rgb = image.convert('RGB')
        # response = HttpResponse(content_type='application/pdf')
        # pdfbuffer = io.BytesIO()
        # img_rgb.save(pdfbuffer, 'PDF', resolution=100.0)
        # response.content = pdfbuffer.getvalue()
        # response['Content-Disposition'] = f'attachment; filename=\"Renaissance Ticket.pdf\"'
        # return response
        return HttpResponse(ticket.generate_customticket().getvalue(), content_type='image/png')
    else:
        messages.error(request,'Invalid ticket id')
        return redirect('home')


        
