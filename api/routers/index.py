from . import orders, order_details, customer, staff, transactions, promotion, ratings_reviews, ingredients, menu_items, recipes, sandwiches, ingredient_tracking, menu_analytics, ingredient_tracking


def load_routes(app):
    app.include_router(customer.router)
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(transactions.router)
    app.include_router(staff.router)
    app.include_router(promotion.router)
    app.include_router(ratings_reviews.router)
    app.include_router(ingredients.router)
    app.include_router(menu_items.router)
    app.include_router(recipes.router)
    app.include_router(sandwiches.router)
    app.include_router(ingredient_tracking.router)
    app.include_router(menu_analytics.router)
    app.include_router(ingredient_tracking.router)
    