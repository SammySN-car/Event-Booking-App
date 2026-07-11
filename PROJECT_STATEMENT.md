# Modern Application Development II
## Project Statement

# Event Ticket Booking App - V2

It is a multi-user app (one requires organizers and other users) that manages event creation, seat allocation, ticket booking, and event analytics. The platform connects event organizers who create and manage events with users who browse and book tickets.

---

## Frameworks to be used

These are the mandatory frameworks on which the project has to be built.

- **Flask** for API
- **VueJS** for UI
- **VueJS Advanced with CLI** (only if required, not necessary)
- **Jinja2 templates** if using CDN only for entry point (Not to be used for UI)
- **Bootstrap** for HTML generation and styling (No other CSS framework is allowed)
- **SQLite** for database (No other database is permitted)
- **Redis** for caching
- **Redis and Celery** for batch jobs

> **Note:** All demos should be possible on your local machine.

---

## Roles

The platform will have two roles:

### Organizer - Can create and manage events

- Register/Login with role selection
- Create a new event with details like name, venue, date, time, price, and total seats
- Each event automatically generates a seat grid based on total seats
- Organizer can view the seat map showing available/booked seats
- Organizer can view all bookings for their events
- Organizer can cancel bookings if needed
- Organizer can view summary charts (revenue per event, occupancy rate, bookings over time)

### User - Can browse events and book tickets

- Register/Login
- Browse all available events
- Select an event and choose an available seat from the seat map
- Book a ticket (auto-generates a unique ticket ID)
- Cancel a booking (seat becomes available again)
- View all booked tickets and their status

---

## Terminologies

**User:** The user will register/login and book tickets for events.

**Organizer:** A registered user with event management privileges. Organizers register through the signup form by selecting the "Organizer" role.

**Event:** A scheduled happening that users can book tickets for. The event may contain the following attributes:

- `id` - primary key
- `organizer_id` (foreign key - users)
- `name`
- `venue`
- `date`
- `time`
- `price`
- `total_seats`
- `created_at`
- etc: Additional fields (if any)

**Seat:** An individual seat within an event's venue. The seat may contain the following attributes:

- `id` - primary key
- `event_id` (foreign key - event)
- `row` (e.g., A, B, C...)
- `number` (e.g., 1, 2, 3...)
- `status` (A-available / B-booked)
- etc: Additional fields (if any)

**Booking:** Allocates a seat to a user for a specific event. This may contain the following attributes:

- `id` - primary key
- `user_id` (foreign key - users)
- `event_id` (foreign key - event)
- `seat_id` (foreign key - seat)
- `ticket_id` - unique auto-generated (e.g., TKT-A1B2C3D4)
- `status` (confirmed/cancelled)
- `created_at`
- etc: Additional fields (if any)

> **Note:** The above tables and fields are not exhaustive, students can add more tables and fields as per their requirements.

---

## Similar apps
- https://www.bookmyshow.com/
- https://www.eventbrite.com/

---

## Application Wireframe

Event Ticket Booking System

*(See wireframe image: `Event Ticket Booking.png`)*

> **Note:**
> The provided wireframe is intended only to illustrate the application's flow and demonstrate what should appear when a user navigates between pages.
> Replication of the exact views is NOT mandatory.
> Students are encouraged to work on their front-end ideas and designs while maintaining the application's intended functionality and flow.

---

## Core Functionalities

### 1. Organizer login and User login

- A login/register form with fields like name, email, password, phone, and role selection (Organizer/User)
- The application should differentiate between organizers and regular users based on their role
- You can either use Flask security (session or token) or JWT based Token based authentication to implement role-based access control
- The app must have a suitable model to store and differentiate all types of users

### 2. Organizer Dashboard - for the Organizer

- The organizer can create/edit/delete events. **Note:** Delete only if no confirmed bookings exist for the event.
- When an event is created, the system automatically generates a seat grid (e.g., rows A-J with seats 1-10) based on total_seats.
- The organizer can view a visual seat map for each event, showing which seats are available (green) and which are booked (red).
- The organizer can view all bookings for their events with attendee details.
- The organizer can cancel bookings, which frees up the seat.
- The organizer can view summary charts showing revenue per event, occupancy percentage, and booking trends.

### 3. User Dashboard - for the User

- The user can browse all available events and view details (venue, date, time, price, seats available).
- The user selects an event and is presented with a visual seat map. **Note:** The user clicks an available seat to book it.
- Upon booking, a unique ticket ID is generated (e.g., TKT-A1B2C3D4) and the seat status changes to "booked."
- The user can view all their tickets with status (confirmed/cancelled).
- The user can cancel a ticket, which changes the status to "cancelled" and frees the seat.
- Shows summary charts on booking history.

> **Note:** The database must be created programmatically (via table creation or model code) or through shell. Manual database creation, such as using DB Browser for SQLite, is NOT allowed.

---

### 4. Backend Jobs

#### a. Scheduled Job - Daily reminders
The application should send daily reminders to users on g-chat using Google Chat Webhooks or SMS or mail.

- Check if a user has not booked any events recently or if there are upcoming events they might be interested in
- If yes, then send the alert asking them to check out new events
- The reminder can be sent in the evening, every day (students can choose the time)

#### b. Scheduled Job - Monthly Activity Report
Devise a monthly report for the user created using HTML and sent via mail.

- The activity report can include events attended per month, total amount spent on tickets, most visited venue, or any relevant information to the user etc.
- For the monthly report to be sent, start a job on the first day of every month → create a report using the above parameters → send it as an email

#### c. User Triggered Async Job - Export as CSV
Devise a CSV format details for the booking history of the user till date.

- This export is meant to download the booking details (booking_id, ticket_id, event_name, venue, date, seat, status, amount etc.)
- Have a dashboard from where the user can trigger the export
- This should trigger a batch job, and send an alert once done

---

### 5. Performance and Caching

- Add caching where required to increase the performance
- Add cache expiry
- API Performance

---

## Recommended and/or Optional functionalities

- Well-designed PDF reports for Monthly activity reports (Students can choose between HTML and PDF reports)
- External APIs/libraries for creating charts, e.g. ChartJS
- Single Responsive UI for both Mobile and Desktop
- Unified UI that works across devices
- Add to desktop feature
- Implementing frontend validation on all the form fields using HTML5 form validation or JavaScript
- Implementing backend validation within your APIs
- Provide styling and aesthetics to your application by creating a beautiful and responsive front end using simple CSS or Bootstrap
- Incorporate a proper login system to prevent unauthorized access to the app using Flask extensions like flask_login, flask_security etc.
- Implement a QR code on the ticket for scanning at the venue
- Any additional feature you feel is appropriate for the application.

---

## Evaluation

Students have to create and submit a project report (not more than 5 pages) on the portal, along with the actual project submission.

The report must include the following things:
- Student details
- Project details, including the question statement and how you approached the problem statement
- Frameworks and libraries used
- ER diagram of your database, including all the tables and their relations
- API resource endpoints (if any)
- Drive link of the presentation video
- If a student has used any form of AI/LLM for the project, you will need to mention the extent of use in your report

---

## Possible folder structure:

```
event-booking/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── resources/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── event.py
│   │       ├── booking.py
│   │       └── summary.py
│   ├── celery_tasks.py
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.vue
│       ├── main.js
│       ├── router.js
│       ├── style.css
│       ├── api/
│       │   ├── auth.js
│       │   └── client.js
│       ├── components/
│       │   ├── OrganizerEvents.vue
│       │   ├── OrganizerBookings.vue
│       │   ├── OrganizerSummary.vue
│       │   ├── UserBrowse.vue
│       │   └── UserTickets.vue
│       └── views/
│           ├── OrganizerDashboard.vue
│           ├── UserDashboard.vue
│           ├── Login.vue
│           └── Signup.vue
```

---

## Video Presentation Guidelines (Advised):

1. A short Intro (not more than 30 sec)
2. How did you approach the problem statement? (30 sec)
3. Highlight key features of the application (90 sec)
4. Any Additional feature(s) implemented other than core requirements (30 sec)

> **Note:**
> 1. The final video must not exceed 5-10 minutes.
> 2. Keeping your video feed on during recording (like in a screencast) is optional but recommended.
