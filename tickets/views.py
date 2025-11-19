from django.contrib import messages
from django.shortcuts import redirect, render
from tickets.models import Category, Ticket

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
            
        Ticket.objects.create(
            title=title,
            description=description,
            category=category,
            created_by=request.user
        )

        messages.success(request, "Ticket created successfully!")
        return redirect("index")
    
    categories = Category.objects.all()
    return render(request, "create_ticket.html", {'categories': categories})