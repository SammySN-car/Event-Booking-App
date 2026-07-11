# Event Ticket Booking System

A premium full-stack web application designed for browsing, booking, and managing ticket sales for events. Styled with a gorgeous glassmorphic Cyberpunk/Neon theme (featuring purple, pink, and cyan neon glows), this system lets organizers manage show listings and seat layouts while users select seats on an interactive grid.

---

## Features

### 1. User Roles & Authentication
*   **Organizer**: Register via signup with the role "organizer". Enables creating, editing, and deleting events with automated seat maps.
*   **User**: Register via signup with the role "user". Allows browsing open events, picking seats interactively from a visual grid, and downloading booking receipts.
*   **JWT Security**: Secure endpoints using Flask-JWT-Extended token headers.

### 2. Event & Seating Grid Management (Organizer)
*   **CRUD Operations**: Full create, edit, and delete support for events (name, venue, date, start_time, end_time, price, capacity).
*   **Automated Seat Generation**: Automatically creates seat maps (Rows A-Z, 10 seats per row) when publishing events.
*   **Seat Alteration Restrictions**: Prevents editing event details or seat maps if active bookings are confirmed.

### 3. Interactive Seat Booking (User)
*   **Visual Grid**: Beautiful seat-selection matrix showing available (green), selected (cyan), and booked (red) seats.
*   **Booking Validation**: Restricts booking once an event's date and start time are reached. Displays "Ended" dynamically if the end time is passed.

### 4. Background Jobs & Analytics
*   **Organizers Dashboard**: Track real-time sales and bookings count.
*   **CSV Exports**: User-triggered background job that compiles order history to CSV and lets users download it.

---

## Tech Stack
*   **Backend**: Flask, Flask-SQLAlchemy, Flask-RESTful, Flask-JWT-Extended
*   **Frontend**: Vue 3 (Composition API), Axios, Bootstrap 5 (CDN), Chart.js
*   **Database**: SQLite

---

## Installation & Setup

### 1. Backend Setup
1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Start the Flask server:
    ```bash
    python -m backend.run
    ```
    *The server runs at `http://localhost:5000` and automatically initializes the SQLite database.*

### 2. Frontend Setup
1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install Node dependencies:
    ```bash
    npm install
    ```
3.  Start the Vite dev server:
    ```bash
    npm run dev
    ```
    *The frontend will run at `http://localhost:5173`.*

---

## API Documentation

### Authentication
*   `POST /register` - Registers a new user (role: 'organizer' or 'user').
*   `POST /login` - Log in and receive a JWT access token, user role, and ID.

### Organizer Event & Seat Controls
*   `GET /admin/home` - Retrieve all events with real-time seat states.
*   `POST /admin/add_lot` - Create a new event.
*   `PUT /admin/edit_lot/<id>` - Modify event details.
*   `DELETE /admin/delete_lot/<id>` - Remove event (only if 0 bookings exist).

### User Bookings & Actions
*   `POST /user/book/<id>` - Confirm a booking for a specific event and seat.
*   `PUT /user/release/<id>` - Cancel an existing booking.
*   `GET /user/home` - Retrieve user's booking history.
*   `GET /user/export_csv` - Trigger Celery job for exporting CSV.
*   `GET /user/export_csv/<file_name>` - Download completed CSV export.
