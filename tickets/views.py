from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from tickets.models import Category, Ticket, TicketAssignment
from django.contrib.auth.models import User

def create_category(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        
        errors = {}

        if not name:
            errors["name"] = "Category name is required."

        if Category.objects.filter(name=name).exists():
            errors["name"] = "This category already exists."

        if errors:
            return render(request, "create_category.html", {
                "errors": errors,
                "form_data": request.POST
            })
            
        Category.objects.create(name=name)

        messages.success(request, "Category created successfully!")
        return redirect("tickets:category_list")
    
    return render(request, "create_category.html")

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'list_categories.html', {'categories': categories})

def tickets(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets_list.html', {'tickets': tickets})

def create_ticket(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        category_id = request.POST.get("category")
        
        errors = {}

        if not title:
            errors["title"] = "Ticket title is required."

        if not category_id:
            errors["category"] = "Category is required."
        else:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                errors["category"] = "Selected category does not exist."

        if errors:
            categories = Category.objects.all()
            return render(request, "create_ticket.html", {
                "errors": errors,
                "form_data": request.POST,
                "categories": categories
            })
        user_profile = request.user.profile
        if not user_profile.department:
            errors["department"] = "Your profile does not have an associated department."
            categories = Category.objects.all()
            return render(request, "create_ticket.html", {
                "errors": errors,
                "form_data": request.POST,
                "categories": categories
            })
        
        Ticket.objects.create(
            title=title,
            description=description,
            category=category,
            created_by=request.user,
            department=user_profile.department
        )

        messages.success(request, "Ticket created successfully!")
        return redirect("index")
    
    categories = Category.objects.all()
    return render(request, "create_ticket.html", {'categories': categories})

def assign_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    user_profile = getattr(request.user, "profile", None)
    if user_profile and user_profile.department:
        users = User.objects.filter(profile__department=user_profile.department)
    elif request.user.is_superuser:
        users = User.objects.all()
    else:
        users = User.objects.none()

    if request.method == "POST":
        user_id = request.POST.get("user_id", "").strip()

        errors = {}
        if not user_id:
            errors["user_id"] = "Please select a user to assign the ticket."
            return redirect("assign.html", ticket.id)
        user = get_object_or_404(User, id=user_id)

        created = TicketAssignment.objects.get_or_create(
            assigned_to=user,
            ticket=ticket,
        )

        if created:
            messages.success(request, f"Ticket #{ticket.id} assigned to {user.username}.")
        else:
            messages.info(request, f"{user.username} is already assigned to this ticket.")

        return redirect("tickets:ticket_details", ticket.id)

    return render(request, "assign.html", {
        "ticket": ticket,
        "users": users,
    })
    
def ticket_details(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    assignments = TicketAssignment.objects.filter(ticket=ticket)

    return render(request, "ticket_details.html", {
        "ticket": ticket,
        "assignments": assignments,
    })