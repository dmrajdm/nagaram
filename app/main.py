from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os

# Initialize FastAPI app
app = FastAPI(title="Nagaram Masala", description="A simple ecommerce site for Nagaram Masala products")

# Mount static files directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup template directory
templates = Jinja2Templates(directory="app/templates")

# Define Product model
class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image_url: Optional[str] = None
    stock: int = 0
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Nagaram Garam Masala",
                "description": "A blend of ground spices used in Indian cuisine",
                "price": 5.99,
                "image_url": "https://example.com/garam-masala.jpg",
                "stock": 10
            }
        }

# Sample product data
sample_product = Product(
    id=1,
    name="Nagaram Garam Masala",
    description="A premium blend of ground spices including cardamom, cinnamon, cloves, and black pepper. This authentic mix adds rich flavor to any Indian dish.",
    price=5.99,
    image_url="https://via.placeholder.com/150",
    stock=100
)

# Home route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "product": sample_product}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# For running the app directly
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

