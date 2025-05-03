# 🌍 The Perfect Reunion: Finding the Best Destination for Friends Around the World

**The Perfect Reunion** is a backend application designed to help groups of friends—living in different parts of the world—easily plan a reunion by finding the ideal meeting destination.

Imagine a group of friends who live in different locations and want to meet in the perfect destination. But where should they go? This project provides a **user-friendly, collaborative travel planner** where everyone has a say in the final decision.

---

## 🎯 Project Goals

The backend is built to:

- Register and manage users
- Create and manage groups
- Send email notifications to group members
- Set the foundation for future destination matching based on preferences and real-time data

---

## ✨ Destination Criteria (Upcoming Features)

These criteria will help suggest the best destination for the group:

- **🌱 Green Travel** – optimize for eco-friendly routes to reduce carbon footprints.
- **🎯 Interests-Based Recommendations** – take into account each member’s interests (art, culture, food, weather, outdoor activities).
- **🎟️ Local Events** – recommend destinations with concerts, sports events, festivals, etc.
- **💰 Cheapest Option** – find the most cost-effective location based on flight/train data.

---

## 🛠️ Tech Stack

- **Python 3.12**
- **Flask** – Web framework
- **SQLAlchemy** – ORM for database operations
- **PostgreSQL** – Relational database
- **Docker & Docker Compose** – Containerization and environment orchestration

---

## 🚀 Getting Started

### 📦 Requirements

- Docker
- Docker Compose

### ⚙️ First-Time Setup

To build the backend for the first time, run:
```bash
./build-backend.sh #For Linux/Mac
```
or
```bash
build-backend.bat #For Windows
```
This script will build the Docker image using docker-compose.

### ▶️ Run the Backend

To start the backend after the initial build, run:
```bash
./run-backend.sh #For Linux/Mac
```
or
```bash
run-backend.bat #For Windows
```
### 🔗 Access the API
Once running, access the backend at:
```bash
http://localhost:5000/
```
If Swagger UI is enabled, the documentation will be available at:
```bash
http://localhost:5000/api-docs
```


