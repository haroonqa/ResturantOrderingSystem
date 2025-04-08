uvicorn api.main:app --reload --port 8000

# Restaurant Ordering System

Welcome to the Restaurant Ordering System! This project provides a streamlined platform for managing restaurant menus and processing customer orders efficiently.

## Features

- **Menu Management**: Easily add, update, and remove menu items.
- **Order Processing**: Handle customer orders with real-time updates.
- **Database Integration**: Utilizes SQLite for data storage.

## Getting Started

Follow these steps to set up and run the project on your local machine.

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- `pip` (Python package installer)

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/haroonqa/ResturantOrderingSystem.git
   ```


2. **Navigate to the Project Directory**:

   ```bash
   cd ResturantOrderingSystem
   ```


3. **Install Required Packages**:

   ```bash
   pip install -r requirements.txt
   ```


### Database Setup

Initialize the database and apply migrations:

1. **Initialize the Database**:

   ```bash
   python initialize_db.py
   ```


2. **Apply Migrations**:

   ```bash
   alembic upgrade head
   ```


3. **Add Sample Menu Items** (Optional):

   ```bash
   python add_sample_menu.py
   ```


### Running the Application

Start the application using Uvicorn:


```bash
uvicorn api.main:app --reload --port 8000
```


The application will be accessible at `http://localhost:8000`.

## API Endpoints

- **`GET /menu`**: Retrieve all menu items.
- **`POST /menu`**: Add a new menu item.
- **`PUT /menu/{item_id}`**: Update an existing menu item.
- **`DELETE /menu/{item_id}`**: Remove a menu item.
- **`POST /order`**: Place a new order.
- **`GET /order/{order_id}`**: Retrieve details of a specific order.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.



