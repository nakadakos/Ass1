# ShopLite Microservices

Services:
- `gateway`: customer-facing UI and API gateway (public)
- `product-service`: product catalogue and its SQLite database
- `cart-service`: cart API and its SQLite database
- `order-service`: order API and its SQLite database

Only the gateway is published to the host. Other services communicate on the private Docker Compose network.

Local: `docker compose up --build -d`, then open http://localhost:8081
GCP: `docker compose -f docker-compose.yml -f docker-compose.gcp.yml up --build -d`, then open `http://VM_EXTERNAL_IP/`.
