from fastapi import FastAPI, HTTPException, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Optional, List
from bson import ObjectId
import re

from models import (
    ProductCreate,
    ProductInDB,
    ProductListResponse,
    OrderCreate,
    OrderInDB,
    OrderListResponse,
    PyObjectId,
)
from database import connect_to_mongo, close_mongo_connection, mongodb

app = FastAPI(title="HROne Ecommerce Backend")

MONGO_URI = "mongodb://localhost:27017"  # Change this to your MongoDB URI
DB_NAME = "hro_ecommerce"

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo(MONGO_URI)
    print("Connected to MongoDB")

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()
    print("Disconnected from MongoDB")

@app.post("/products", status_code=status.HTTP_201_CREATED, response_model=ProductInDB)
async def create_product(product: ProductCreate):
    product_dict = product.dict()
    result = await mongodb.client[DB_NAME].products.insert_one(product_dict)
    created_product = await mongodb.client[DB_NAME].products.find_one({"_id": result.inserted_id})
    if created_product:
        created_product["id"] = str(created_product["_id"])
    return ProductInDB(**created_product)

from fastapi import Request
import logging

# Add detailed logging middleware to capture request and response info
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import Response
import time

@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = f"{time.time()}"
    logging.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response: Response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = f"{process_time:.2f}"
    logging.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response

@app.get("/")
async def root():
    return {"message": "HROne Ecommerce Backend is running"}
    
@app.get("/products", response_model=ProductListResponse)
async def list_products(
    name: Optional[str] = Query(None, description="Name regex or partial search"),
    size: Optional[str] = Query(None, description="Filter by size"),
    limit: Optional[int] = Query(10, ge=1, le=100, description="Number of documents to return"),
    offset: Optional[int] = Query(0, ge=0, description="Number of documents to skip"),
    request: Request = None,
):
    try:
        query = {}
        if name:
            logging.info(f"Filtering products by name regex: {name}")
            # Use case-insensitive regex search for name
            query["name"] = {"$regex": re.compile(name, re.IGNORECASE)}
        if size:
            logging.info(f"Filtering products by size: {size}")
            query["size"] = size

        logging.info(f"MongoDB query: {query}")
        cursor = mongodb.client[DB_NAME].products.find(query).skip(offset).limit(limit).sort("_id")
        products = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            products.append(ProductInDB(**doc))
        return ProductListResponse(products=products)
    except Exception as e:
        import traceback
        logging.error(f"Error in list_products: {e}", exc_info=True)
        logging.error("Traceback:\n" + traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@app.post("/orders", status_code=status.HTTP_201_CREATED, response_model=OrderInDB)
async def create_order(order: OrderCreate):
    order_dict = order.dict(by_alias=True)
    result = await mongodb.client[DB_NAME].orders.insert_one(order_dict)
    created_order = await mongodb.client[DB_NAME].orders.find_one({"_id": result.inserted_id})
    if created_order:
        created_order["id"] = str(created_order["_id"])
    return OrderInDB(**created_order)

@app.get("/orders/{user_id}", response_model=OrderListResponse)
async def list_orders(
    user_id: str = Path(..., description="User ID"),
    limit: Optional[int] = Query(10, ge=1, le=100, description="Number of documents to return"),
    offset: Optional[int] = Query(0, ge=0, description="Number of documents to skip"),
):
    query = {"user_id": user_id}
    cursor = mongodb.client[DB_NAME].orders.find(query).skip(offset).limit(limit).sort("_id")
    orders = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        orders.append(OrderInDB(**doc))
    return OrderListResponse(orders=orders)
