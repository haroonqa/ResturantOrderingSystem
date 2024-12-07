from .orders import router as orders_router
from .order_details import router as order_details_router
from .customer import router as customer_router
from .promotion import router as promotion_router
from .ingredients import router as ingredients_router
from .menu_items import router as menu_items_router
from .ratings_reviews import router as ratings_reviews_router

def load_routes(app):
    app.include_router(orders_router)
    app.include_router(order_details_router)
    app.include_router(customer_router)
    app.include_router(promotion_router)
    app.include_router(ingredients_router)
    app.include_router(menu_items_router)
    app.include_router(ratings_reviews_router)
