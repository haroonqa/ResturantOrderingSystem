from sqlalchemy.orm import Session
from ..models.menu_items import MenuItem
from ..dependencies.database import SessionLocal

def add_sample_menu_items():
    db = SessionLocal()
    try:
        # Sample menu items with dietary types and tags
        menu_items = [
            MenuItem(
                name="Veggie Supreme Pizza",
                price=14.99,
                calories=800,
                category="Pizza",
                dietary_type="vegetarian",
                description="Fresh vegetables on a crispy crust with our signature sauce",
                tags="vegetarian,pizza,healthy"
            ),
            MenuItem(
                name="Classic Cheeseburger",
                price=12.99,
                calories=950,
                category="Burgers",
                description="100% Angus beef patty with melted cheddar",
                tags="beef,classic,burger"
            ),
            MenuItem(
                name="Quinoa Buddha Bowl",
                price=13.99,
                calories=600,
                category="Bowls",
                dietary_type="vegan",
                description="Quinoa, roasted vegetables, and tahini dressing",
                tags="vegan,healthy,gluten-free"
            ),
            MenuItem(
                name="Spicy Buffalo Wings",
                price=10.99,
                calories=850,
                category="Appetizers",
                description="Crispy wings tossed in our signature buffalo sauce",
                tags="spicy,chicken,appetizer"
            ),
            MenuItem(
                name="Mediterranean Salad",
                price=11.99,
                calories=450,
                category="Salads",
                dietary_type="vegetarian",
                description="Fresh greens, feta, olives, and balsamic dressing",
                tags="vegetarian,healthy,salad"
            )
        ]
        
        # Add all menu items
        for item in menu_items:
            db.add(item)
        
        # Commit the changes
        db.commit()
        print("Sample menu items added successfully!")
        
    except Exception as e:
        print(f"Error adding sample menu items: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_menu_items()
