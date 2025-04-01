# 🗺️ Travel Planner Backend

This is a Flask-based backend for a travel planning application. It calculates the shortest route covering all user-provided destinations and returning to the starting point using the **Held-Karp Algorithm** (Dynamic Programming with Bitmasking). The backend fetches coordinates for each location using the OpenCage API and computes distances between locations using the **geodesic distance formula**.

---

## 🚀 Features
- 📍 **Fetches Coordinates**: Retrieves latitude and longitude of input locations via OpenCage API.
- 📏 **Computes Distances**: Uses geodesic distance to create a graph of inter-location distances.
- 🔍 **Optimized Route Calculation**: Implements the **Held-Karp Algorithm** (TSP solution) for the shortest path.
- 🌍 **CORS Enabled**: Allows frontend applications to make API requests.
- 🖥 **Deployed on Render**: Uses dynamic port allocation for hosting.

---

## 🏗️ Tech Stack
- **Python** (Flask, asyncio, httpx)
- **Flask-CORS** (for cross-origin requests)
- **Geopy** (for geodesic distance calculation)
- **OpenCage API** (for geocoding)
- **Dynamic Programming with Bitmasking** (Held-Karp Algorithm)

---

## 🛠️ Installation

### 🔹 Prerequisites
- Python 3.8+
- `pip` (Python package manager)
- OpenCage API Key (get one from [OpenCage Geocoder](https://opencagedata.com/))

### 🔹 Setup & Run
1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/travel-planner-backend.git
   cd travel-planner-backend
