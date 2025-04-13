# E-Commerce API Assignment Solution

## Solution Overview
This implementation provides a functional e-commerce API with client-facing cart operations and admin management features, built with FastAPI (Python) and Vite (frontend). The solution demonstrates:

- RESTful API design
- Business logic implementation
- Discount management system
- Basic frontend integration
- Unit testing

## Implemented Features
# E-Commerce API - Core Endpoints

## Client Endpoints
- `POST /cart/add` - Add item to cart
- `POST /cart/update` - Update item quantity
- `GET /discount/available` - Get active discount codes 
- `POST /checkout` - Process order with discount

## Admin Endpoints
- `POST /admin/discount/generate` - Manually create discount code
- `GET /admin/status` - View store statistics

For complete API documentation including request/response formats and examples, visit the interactive Swagger UI at:  
`http://localhost:8000/docs` when the server is running.

> Note: All endpoints use JSON format for requests and responses. The Swagger documentation provides full details on required parameters and response structures.

### Technical Implementation
- **Backend**: FastAPI with Pydantic validation
- **Frontend**: Vite + React (stretch goal)
- **Testing**: pytest coverage
- **Containerization**: Docker support
- **Storage**: In-memory (no persistence)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yogesh2k21/Assignment.git
    cd Assignment
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS and Linux
    venv\Scripts\activate  # On Windows
    ```

3.  **Install the required dependencies:**
    ```bash
    cd ./backend/
    pip install -r requirements.txt
    ```

## Running the Application Backend

1.  Run the FastAPI application:
    ```bash
    uvicorn app.main:app --reload     
    ```

    * `main`: The name of your main Python file (where the FastAPI instance is created).
    * `app`: The name of the FastAPI application instance in `main.py`.

2. If you find any difficulty then you can use docker also,
   ```bash
   docker network create ecom_network
   docker-compose up --build -d
   ```

Once the server is running, open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for built-in Swagger API documentation.

## Running the Application Frontend
1.  Navigate to the `frontend` directory:
cd ./frontend/

2.  **Install the dependencies:**
    ```bash
    npm install

2.  **Start the development server:**
    ```bash
    npm run dev
    ```

    This will start the dev server at `http://localhost:3000`. Now open it on browser.



## Testing the Application

1.  Make sure you are in the `backend` folder.

2.  Run the unit tests using the following command:
    ```bash
    pytest .\tests\test.py
    ```

    This will run all the test functions in the `tests/test.py` file. The output result whether the tests passed or failed.
