# HROne Ecommerce Backend

This is a sample backend application built with FastAPI and Python, using MongoDB as the database. It implements basic ecommerce APIs for products and orders.

## Features

- Create Products API (`POST /products`)
- List Products API with filtering and pagination (`GET /products`)
- Create Order API (`POST /orders`)
- List Orders for a user with pagination (`GET /orders/{user_id}`)

## Tech Stack

- Python 3.10+
- FastAPI
- Motor (async MongoDB driver)
- MongoDB (can use MongoDB Atlas free tier)
- Pydantic for data validation

## Setup Instructions

1. Clone the repository.

2. Navigate to the project directory:

```bash
cd hro_backend
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure MongoDB connection:

- By default, the app connects to `mongodb://localhost:27017`.
- To use MongoDB Atlas or other MongoDB instances, update the `MONGO_URI` variable in `main.py`.

5. Run the FastAPI server:

```bash
uvicorn main:app --reload
```

6. The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### Create Product

- **Endpoint:** `/products`
- **Method:** POST
- **Request Body:**

```json
{
  "name": "string",
  "size": "string (optional)",
  "price": float,
  "description": "string (optional)"
}
```

- **Response Body:**

```json
{
  "_id": "string",
  "name": "string",
  "size": "string",
  "price": float,
  "description": "string"
}
```

- **Status Code:** 201 Created

### List Products

- **Endpoint:** `/products`
- **Method:** GET
- **Query Parameters (optional):**
  - `name`: string (regex or partial search)
  - `size`: string
  - `limit`: int (default 10)
  - `offset`: int (default 0)

- **Response Body:**

```json
{
  "products": [
    {
      "_id": "string",
      "name": "string",
      "size": "string",
      "price": float,
      "description": "string"
    }
  ]
}
```

- **Status Code:** 200 OK

### Create Order

- **Endpoint:** `/orders`
- **Method:** POST
- **Request Body:**

```json
{
  "user_id": "string",
  "items": [
    {
      "product_id": "string",
      "quantity": int
    }
  ]
}
```

- **Response Body:**

```json
{
  "_id": "string",
  "user_id": "string",
  "items": [
    {
      "product_id": "string",
      "quantity": int
    }
  ]
}
```

- **Status Code:** 201 Created

### List Orders for User

- **Endpoint:** `/orders/{user_id}`
- **Method:** GET
- **Query Parameters (optional):**
  - `limit`: int (default 10)
  - `offset`: int (default 0)

- **Response Body:**

```json
{
  "orders": [
    {
      "_id": "string",
      "user_id": "string",
      "items": [
        {
          "product_id": "string",
          "quantity": int
        }
      ]
    }
  ]
}
```

- **Status Code:** 200 OK

## Testing

- Run the FastAPI server.
- Use the provided test scripts (`test_api_thorough.py`, `test_api_extended.py`, `test_api_full_coverage.py`) to verify functionality.
- Run tests with:

```bash
python test_api_full_coverage.py
```

## Deployment

- You can deploy this app on free hosting platforms like Render or Railway.
- Make sure to update the `MONGO_URI` to point to your MongoDB Atlas cluster or other accessible MongoDB instance.
- Share the base URL of your deployed app for automated testing.

## Notes

- The app uses Motor for async MongoDB operations.
- ObjectId fields are serialized as strings in responses.
- Pagination is implemented using `limit` and `offset` query parameters.
- Filtering supports regex search on product names.

## Author

Your Name
