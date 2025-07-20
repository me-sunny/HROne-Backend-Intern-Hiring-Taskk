import asyncio
import httpx
import pytest

BASE_URL = "http://127.0.0.1:8000"

async def test_create_product_valid():
    product_data = {
        "name": "Test Product",
        "size": "large",
        "price": 100.0,
        "description": "Test description"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/products", json=product_data)
        assert response.status_code == 201, f"Create product failed: {response.text}"
        data = response.json()
        assert data["name"] == product_data["name"]
        assert data["size"] == product_data["size"]
        return data["_id"]

async def test_create_product_invalid():
    # Missing required field 'name'
    product_data = {
        "size": "large",
        "price": 100.0,
        "description": "Test description"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/products", json=product_data)
        assert response.status_code == 422, f"Invalid product creation should fail: {response.text}"

async def test_list_products_filters():
    async with httpx.AsyncClient() as client:
        # Test no filters
        response = await client.get(f"{BASE_URL}/products")
        assert response.status_code == 200, f"List products failed: {response.text}"
        data = response.json()
        assert "products" in data

        # Test name filter with regex
        response = await client.get(f"{BASE_URL}/products", params={"name": "Test"})
        assert response.status_code == 200

        # Test size filter
        response = await client.get(f"{BASE_URL}/products", params={"size": "large"})
        assert response.status_code == 200

        # Test pagination
        response = await client.get(f"{BASE_URL}/products", params={"limit": 1, "offset": 0})
        assert response.status_code == 200

async def test_create_order_valid(product_id):
    order_data = {
        "user_id": "testuser",
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
        data = response.json()
        assert data["user_id"] == order_data["user_id"]
        return data["_id"]

async def test_create_order_invalid():
    # Missing user_id
    order_data = {
        "items": [
            {
                "product_id": "000000000000000000000000",
                "quantity": 2
            }
        ]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/orders", json=order_data)
        assert response.status_code == 422, f"Invalid order creation should fail: {response.text}"

async def test_list_orders(user_id):
    async with httpx.AsyncClient() as client:
        # Test list orders for user
        response = await client.get(f"{BASE_URL}/orders/{user_id}")
        assert response.status_code == 200, f"List orders failed: {response.text}"
        data = response.json()
        assert "orders" in data

        # Test pagination
        response = await client.get(f"{BASE_URL}/orders/{user_id}", params={"limit": 1, "offset": 0})
        assert response.status_code == 200

async def main():
    await test_create_product_invalid()
    product_id = await test_create_product_valid()
    await test_list_products_filters()
    await test_create_order_invalid()
    order_id = await test_create_order_valid(product_id)
    await test_list_orders("testuser")
    print("All thorough tests passed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
