from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, desc, case
from sqlalchemy.orm import Session
from typing import List
from ..dependencies.database import get_db
from ..models.menu_items import MenuItem
from ..models.orders import Order
from ..models.ratings_reviews import RatingsReviews
from pydantic import BaseModel
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/menu-analytics",
    tags=["Menu Analytics"]
)

class MenuItemAnalytics(BaseModel):
    menu_item_id: int
    name: str
    average_rating: float
    low_rating_count: int  # Number of ratings below 3
    status: str  # "Popular", "Average", "Needs Attention"

    class Config:
        from_attributes = True

@router.get("/item-performance", response_model=List[MenuItemAnalytics])
async def get_menu_performance(
    days: int = 30,
    db: Session = Depends(get_db)
):
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Get rating statistics
    rating_stats = db.query(
        RatingsReviews.menu_item_id,
        func.avg(RatingsReviews.rating).label('average_rating'),
        func.count(case((RatingsReviews.rating < 3, 1))).label('low_rating_count')
    ).group_by(RatingsReviews.menu_item_id).subquery()
    
    # Combine all data
    results = db.query(
        MenuItem,
        func.coalesce(rating_stats.c.average_rating, 0).label('average_rating'),
        func.coalesce(rating_stats.c.low_rating_count, 0).label('low_rating_count')
    ).outerjoin(rating_stats, MenuItem.id == rating_stats.c.menu_item_id
    ).all()
    
    # Create response
    analytics_list = []
    for item in results:
        # Determine status based on ratings
        status = "Popular" if item[1] >= 4.0 else \
                "Needs Attention" if (item[1] < 3.0 or item[2] >= 3) else \
                "Average"
        
        analytics_list.append({
            "menu_item_id": item[0].id,
            "name": item[0].name,
            "average_rating": round(item[1], 2) if item[1] else 0,
            "low_rating_count": item[2],
            "status": status
        })
    
    # Sort by average rating descending
    analytics_list.sort(key=lambda x: x["average_rating"], reverse=True)
    return analytics_list

@router.get("/needs-attention")
async def get_items_needing_attention(
    db: Session = Depends(get_db)
):
    """Get items that need attention (low ratings)"""
    analytics = await get_menu_performance(days=30, db=db)
    needs_attention = [item for item in analytics if item["status"] == "Needs Attention"]
    
    return {
        "items_needing_attention": needs_attention,
        "recommendations": [
            f"'{item['name']}' needs attention due to low ratings (avg: {item['average_rating']})"
            for item in needs_attention
        ]
    }
