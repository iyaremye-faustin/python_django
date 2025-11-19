from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from tickets.models import Ticket

@login_required
def index(request):
    tickets = Ticket.objects.filter(created_by=request.user)
    assignedToMe = Ticket.objects.filter(assignments__assigned_to=request.user)
    statistics = {
        'total_tickets': tickets.count(),
        'open_tickets': tickets.filter(status='open').count(),
        'in_progress_tickets': tickets.filter(status='in_progress').count(),
        'closed_tickets': tickets.filter(status='closed').count(),
        'cancelled_tickets': tickets.filter(status='cancelled').count(),
        'assigned_to_me': assignedToMe.count(),
    }
    return render(request, 'index.html', {'tickets': tickets, 'statistics': statistics, 'assignedToMe': assignedToMe})

def changeTicketStatus(request, ticket_id, new_status):
    try:
        ticket = Ticket.objects.get(id=ticket_id, created_by=request.user)
        ticket.status = new_status
        ticket.save()
    except Ticket.DoesNotExist:
        pass
    return redirect('dashboard:index')  