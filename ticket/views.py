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


def qr(request,ticketId):
    _pass = Passes.objects.get(psid=ticketId)
    ticket = generate_master_ticket(User.objects.get(email=_pass.email))
    response = HttpResponse(ticket.getvalue(), content_type='image/png')
    return response
    
def event(request):
    if request.method == 'GET':
        events = Events.objects.filter(type='tech')
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
    
def event_type(request,type):
    if request.method == 'GET':
        events = Events.objects.filter(type=type)
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

# def getEvent(request):
#     data = json.loads(request.body)
#     event_id = data['event_id']
#     event = Events.objects.get(id=event_id)
#     if 'user_id' not in data:
#         context = {
#             'id':event.id,
#             'name':event.name,
#             'type':event.get_type_display(),
#             'venue':event.venue,
#             'time':event.time.strftime("%-I:%M %p"),
#             'date':event.date.strftime("%a, %d %b, %Y"),
#             'desc':event.description,
#             'amount':event.amount,
#             'includedInPass':event.includedInPass,
#         }
#         return JsonResponse(context)
#     user_id = data['user_id']
#     if event.includedInPass:
#         user = User.objects.get(id=user_id)
#         _pass = getPass(user)
#         includedInPass = False
#         if _pass is not None:
#             if event.type == 'tech' and _pass.technical is None:
#                 includedInPass = True
#             elif event.type == 'splash' and _pass.splash is None:
#                 includedInPass = True            
#         context = {
#             'id':event.id,
#             'name':event.name,
#             'type':event.get_type_display(),
#             'venue':event.venue,
#             'time':event.time.strftime("%-I:%M %p"),
#             'date':event.date.strftime("%a, %d %b, %Y"),
#             'desc':event.description,
#             'amount':event.amount,
#             'includedInPass':includedInPass,
#         }
#     else:
#         context = {
#             'id':event.id,
#             'name':event.name,
#             'type':event.get_type_display(),
#             'venue':event.venue,
#             'time':event.time.strftime("%-I:%M %p"),
#             'date':event.date.strftime("%a, %d %b, %Y"),
#             'desc':event.description,
#             'amount':event.amount,
#             'includedInPass':False,
#         }
#     return JsonResponse(context)

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
        image = Image.open(ticket.generate_customticket())
        img_rgb = image.convert('RGB')
        response = HttpResponse(content_type='application/pdf')
        pdfbuffer = io.BytesIO()
        img_rgb.save(pdfbuffer, 'PDF', resolution=100.0)
        response.content = pdfbuffer.getvalue()
        response['Content-Disposition'] = f'attachment; filename=\"Renaissance Ticket.pdf\"'
        return response
        # return HttpResponse(ticket.generate_customticket(), content_type='image/png')
    else:
        messages.error('Invalid ticket id')
        return redirect('home')


        
