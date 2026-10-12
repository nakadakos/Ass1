# Assignment 1: E-commerce Architecture Comparison

This bundle contains two independently deployable Flask e-commerce demos:
- `ecommerce-monolithic/`: one Flask application and one SQLite database.
- `ecommerce-microservices/`: a public web/API gateway plus product, cart, and order services, each with its own SQLite database.

## Local prerequisites
- Docker Desktop running on Windows
- Git
- VS Code

## Run the monolithic app locally
```powershell
cd ecommerce-monolithic
docker compose up --build -d
```
Open http://localhost:8080

## Run the microservices app locally
```powershell
cd ecommerce-microservices
docker compose up --build -d
```
Open http://localhost:8081

## Stop either app
Run `docker compose down` from that app's folder. To remove saved demo database volumes too, use `docker compose down -v`.

## Deploy on GCP without gcloud CLI
1. In the Google Cloud Console, create two Ubuntu 24.04 Compute Engine VMs. Enable HTTP traffic on both VMs.
2. Use each VM's browser-based SSH button.
3. Install Docker Engine and the Docker Compose plugin on each VM, following Docker's official Ubuntu instructions.
4. Clone your public GitHub repository on each VM.
5. On VM 1:
   ```bash
   cd <repo-folder>/ecommerce-monolithic
   HOST_PORT=80 docker compose up --build -d
   ```
6. On VM 2:
   ```bash
   cd <repo-folder>/ecommerce-microservices
   HOST_PORT=80 docker compose up --build -d
   ```
7. Visit `http://VM1_EXTERNAL_IP/` and `http://VM2_EXTERNAL_IP/`.

Only the microservices gateway is published by its Compose file; the product, cart, and order services remain on the private Docker network. If your VM's firewall does not permit HTTP, add a narrowly scoped TCP port 80 ingress rule for the relevant VM/network in the Google Cloud Console.

For coursework demonstration only. Do not use this demo for real payments or production customer data. This is a teaching example, not a production-secure commerce system.
