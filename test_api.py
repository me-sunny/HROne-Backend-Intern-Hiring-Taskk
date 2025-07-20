import asyncio
import httpx

BASE_URL = "http://127.0.0.1:8000"

async def test_create_product():
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

async def test_list_products():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/products")
        assert response.status_code == 200, f"List products failed: {response.text}"
        data = response.json()
        assert "products" in data
        assert isinstance(data["products"], list)

async def test_create_order(product_id):
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

async def test_list_orders(user_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/orders/{user_id}")
        assert response.status_code == 200, f"List orders failed: {response.text}"
        data = response.json()
        assert "orders" in data
        assert isinstance(data["orders"], list)

async def main():
    product_id = await test_create_product()
    await test_list_products()
    order_id = await test_create_order(product_id)
    await test_list_orders("testuser")
    print("All critical-path tests passed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
