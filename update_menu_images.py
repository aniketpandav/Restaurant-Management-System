import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_project.settings')
django.setup()

from menu.models import MenuItem

def update_menu_images():
    """
    Update menu items with image file paths
    """
    image_map = {
        'Bruschetta': 'bruschetta.jpg',
        'Spinach Artichoke Dip': 'spinach_artichoke_dip.jpg',
        'Calamari': 'calamari.jpg',
        'Grilled Salmon': 'grilled_salmon.jpg',
        'Filet Mignon': 'filet_mignon.jpg',
        'Mushroom Risotto': 'mushroom_risotto.jpg',
        'Chicken Parmesan': 'chicken_parmesan.jpg',
        'Chocolate Lava Cake': 'chocolate_lava_cake.jpg',
        'Tiramisu': 'tiramisu.jpg',
        'Fresh Lemonade': 'fresh_lemonade.jpg',
        'Iced Tea': 'iced_tea.jpg',
        'Caesar Salad': 'caesar_salad.jpg',
        'French Onion Soup': 'french_onion_soup.jpg',
    }
    
    for item_name, image_file in image_map.items():
        try:
            item = MenuItem.objects.get(name=item_name)
            item.image = f'menu_images/{image_file}'
            item.save()
            print(f"Updated image for {item_name}")
        except MenuItem.DoesNotExist:
            print(f"Menu item '{item_name}' not found")
    
    print("Menu image update completed!")

if __name__ == "__main__":
    update_menu_images() 