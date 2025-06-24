import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_project.settings')
django.setup()

from django.contrib.auth.models import User
from menu.models import Category, MenuItem
from reviews.models import Review
from django.utils import timezone


def create_superuser():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser created.")
    else:
        print("Superuser already exists.")


def create_menu_categories():
    categories = [
        {"name": "Appetizers", "description": "Start your meal with these delicious appetizers"},
        {"name": "Main Course", "description": "Our chef's special main dishes"},
        {"name": "Desserts", "description": "Sweet treats to finish your meal"},
        {"name": "Beverages", "description": "Refreshing drinks to complement your food"},
        {"name": "Soups & Salads", "description": "Fresh and healthy options"},
    ]
    
    for cat in categories:
        Category.objects.get_or_create(
            name=cat["name"],
            defaults={"description": cat["description"]}
        )
    
    print(f"Created {len(categories)} menu categories.")


def create_menu_items():
    appetizers = Category.objects.get(name="Appetizers")
    main_course = Category.objects.get(name="Main Course")
    desserts = Category.objects.get(name="Desserts")
    beverages = Category.objects.get(name="Beverages")
    soups_salads = Category.objects.get(name="Soups & Salads")
    
    menu_items = [
        
        {
            "name": "Bruschetta",
            "description": "Toasted bread topped with tomatoes, fresh basil, and garlic",
            "price": 8.99,
            "category": appetizers,
            "is_vegetarian": True,
            "is_gluten_free": False,
            "is_featured": True,
            "calories": 320,
        },
        {
            "name": "Spinach Artichoke Dip",
            "description": "Creamy dip with spinach, artichokes, and melted cheese, served with tortilla chips",
            "price": 10.99,
            "category": appetizers,
            "is_vegetarian": True,
            "is_gluten_free": False,
            "is_featured": False,
            "calories": 450,
        },
        {
            "name": "Calamari",
            "description": "Crispy fried calamari served with marinara sauce and lemon wedges",
            "price": 12.99,
            "category": appetizers,
            "is_vegetarian": False,
            "is_gluten_free": False,
            "is_featured": False,
            "calories": 380,
        },
        
        {
            "name": "Grilled Salmon",
            "description": "Fresh Atlantic salmon fillet grilled to perfection, served with seasonal vegetables and rice pilaf",
            "price": 24.99,
            "category": main_course,
            "is_vegetarian": False,
            "is_gluten_free": True,
            "is_featured": True,
            "calories": 520,
        },
        {
            "name": "Filet Mignon",
            "description": "8oz premium beef tenderloin, topped with herb butter, served with mashed potatoes and asparagus",
            "price": 32.99,
            "category": main_course,
            "is_vegetarian": False,
            "is_gluten_free": True,
            "is_featured": True,
            "calories": 650,
        },
        {
            "name": "Mushroom Risotto",
            "description": "Creamy Arborio rice with wild mushrooms, finished with truffle oil and parmesan",
            "price": 18.99,
            "category": main_course,
            "is_vegetarian": True,
            "is_gluten_free": True,
            "is_featured": False,
            "calories": 480,
        },
        {
            "name": "Chicken Parmesan",
            "description": "Breaded chicken breast topped with marinara sauce and melted mozzarella, served with pasta",
            "price": 19.99,
            "category": main_course,
            "is_vegetarian": False,
            "is_gluten_free": False,
            "is_featured": False,
            "calories": 720,
        },
        
        {
            "name": "Chocolate Lava Cake",
            "description": "Warm chocolate cake with a molten center, served with vanilla ice cream",
            "price": 8.99,
            "category": desserts,
            "is_vegetarian": True,
            "is_gluten_free": False,
            "is_featured": True,
            "calories": 430,
        },
        {
            "name": "Tiramisu",
            "description": "Classic Italian dessert with layers of coffee-soaked ladyfingers and mascarpone cream",
            "price": 7.99,
            "category": desserts,
            "is_vegetarian": True,
            "is_gluten_free": False,
            "is_featured": False,
            "calories": 380,
        },
        {
            "name": "Fresh Lemonade",
            "description": "Freshly squeezed lemons with just the right amount of sweetness",
            "price": 4.99,
            "category": beverages,
            "is_vegetarian": True,
            "is_gluten_free": True,
            "is_featured": False,
            "calories": 120,
        },
        {
            "name": "Iced Tea",
            "description": "Freshly brewed black tea served with lemon",
            "price": 3.99,
            "category": beverages,
            "is_vegetarian": True,
            "is_gluten_free": True,
            "is_featured": False,
            "calories": 80,
        },
        
        
        {
            "name": "Caesar Salad",
            "description": "Crisp romaine lettuce with Caesar dressing, croutons, and parmesan cheese",
            "price": 9.99,
            "category": soups_salads,
            "is_vegetarian": True,
            "is_gluten_free": False,
            "is_featured": False,
            "calories": 320,
        },
        {
            "name": "French Onion Soup",
            "description": "Rich beef broth with caramelized onions, topped with melted Gruyère cheese and croutons",
            "price": 7.99,
            "category": soups_salads,
            "is_vegetarian": False,
            "is_gluten_free": False,
            "is_featured": False,
            "calories": 290,
        },
    ]
    
    for item in menu_items:
        MenuItem.objects.get_or_create(
            name=item["name"],
            defaults={
                "description": item["description"],
                "price": item["price"],
                "category": item["category"],
                "is_vegetarian": item["is_vegetarian"],
                "is_gluten_free": item["is_gluten_free"],
                "is_featured": item["is_featured"],
                "is_available": True,
                "spicy_level": random.randint(0, 2),
                "image": f"menu_images/placeholder.jpg",  # Using placeholder image path
            }
        )
    
    print(f"Created {len(menu_items)} menu items.")

def create_reviews():
    
    if not User.objects.filter(username='customer').exists():
        user = User.objects.create_user('customer', 'customer@example.com', 'customer123')
        user.first_name = 'John'
        user.last_name = 'Doe'
        user.save()
    else:
        user = User.objects.get(username='customer')
    
    
    menu_items = MenuItem.objects.all()
    
    reviews_data = [
        {
            "rating": 5,
            "comment": "The food was absolutely delicious! Will definitely come back again.",
            "menu_item": menu_items.filter(name="Grilled Salmon").first(),
        },
        {
            "rating": 4,
            "comment": "Great atmosphere and excellent service. The filet mignon was cooked to perfection.",
            "menu_item": menu_items.filter(name="Filet Mignon").first(),
        },
        {
            "rating": 5,
            "comment": "The chocolate lava cake was amazing! Best dessert I've had in a long time.",
            "menu_item": menu_items.filter(name="Chocolate Lava Cake").first(),
        },
    ]
    
    for review_data in reviews_data:
        if review_data["menu_item"]:
            Review.objects.get_or_create(
                user=user,
                menu_item=review_data["menu_item"],
                defaults={
                    "rating": review_data["rating"],
                    "comment": review_data["comment"],
                    "created_at": timezone.now() - timedelta(days=random.randint(1, 30)),
                }
            )
    
    print(f"Created {len(reviews_data)} reviews.")

if __name__ == "__main__":
    print("Starting database population...")
    create_superuser()
    create_menu_categories()
    create_menu_items()
    create_reviews()
    print("Database population completed!") 