import asyncio
import httpx

BASE_URL = "http://127.0.0.1:8000"

async def test_create_product_valid():
    product_data = {
        "name": "Test Product",
        "size": "large",
        "price": 99.99,
        "description": "A test product"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/products", json=product_data)
        assert response.status_code == 201, f"Create product failed: {response.text}"
        return response.json()

async def test_create_product_invalid():
    product_data = {
        "size": "large",
        "price": 99.99
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/products", json=product_data)
        assert response.status_code == 422, f"Expected validation error, got {response.status_code}"

async def test_list_products_filters():
    async with httpx.AsyncClient() as client:
        # Test name filter with partial match
        response = await client.get(f"{BASE_URL}/products", params={"name": "Test"})
        assert response.status_code == 200, f"List products failed: {response.text}"
        data = response.json()
        assert "products" in data

        # Test size filter
        response = await client.get(f"{BASE_URL}/products", params={"size": "large"})
        assert response.status_code == 200, f"List products failed: {response.text}"

async def test_list_products_pagination():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/products", params={"limit": 1, "offset": 0})
        assert response.status_code == 200, f"Pagination failed: {response.text}"
        data = response.json()
        assert len(data["products"]) <= 1

async def test_create_order_valid(product_id):
    order_data = {
        "user_id": "user123",
        "items": [
            {
                "product_id": product_id,
                "quantity": 2
            }
        ]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/orders", json=order_data)
        assert response.status_code == 201, f"Create order failed: {response.text}"
        return response.json()

async def test_create_order_invalid_quantity():
    order_data = {
        "user_id": "user123",
        "items": [
            {
                "product_id": "000000000000000000000000",
                "quantity": 0
            }
        ]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/orders", json=order_data)
        assert response.status_code == 422, f"Expected validation error, got {response.status_code}"

async def test_list_orders_pagination(user_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/orders/{user_id}", params={"limit": 1, "offset": 0})
        assert response.status_code == 200, f"Order pagination failed: {response.text}"
        data = response.json()
        assert len(data["orders"]) <= 1

async def main():
    # Create a valid product
    product = await test_create_product_valid()
    product_id = product["_id"]

    # Test invalid product creation
    await test_create_product_invalid()

    # Test product listing filters and pagination
    await test_list_products_filters()
    await test_list_products_pagination()

    # Create a valid order
    order = await test_create_order_valid(product_id)
    user_id = order["user_id"]

    # Test invalid order creation
    await test_create_order_invalid_quantity()

    # Test order listing pagination
    await test_list_orders_pagination(user_id)

    print("All full coverage tests passed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
