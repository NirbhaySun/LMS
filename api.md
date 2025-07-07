# LibSys REST API Documentation

Base URL: /api/

## Authentication
- All endpoints require session authentication (login via Django admin or web UI).
- Librarian-only endpoints require the user to be staff/admin.

---

## Books
- **List all books**
  - GET `/api/books/`
- **Retrieve a book**
  - GET `/api/books/{id}/`
- **Create a book** (librarian only)
  - POST `/api/books/`
  - Fields: book_name, book_author, book_genre, isAvailable, book_photo
- **Update a book** (librarian only)
  - PUT/PATCH `/api/books/{id}/`
- **Delete a book** (librarian only)
  - DELETE `/api/books/{id}/`

---

## Users
- **List all users** (librarian only)
  - GET `/api/users/`
- **Retrieve a user** (librarian only)
  - GET `/api/users/{id}/`

---

## Wishlist
- **Get a user's wishlist**
  - GET `/api/users/{id}/wishlist/`
- **Add to wishlist**
  - POST `/api/users/{id}/wishlist/`
  - Body: `{ "book_id": <book_id> }`
- **Remove from wishlist**
  - DELETE `/api/users/{id}/wishlist/`
  - Body: `{ "book_id": <book_id> }`

---

## Book Logs (Notifications)
- **List all borrow/return logs** (librarian only)
  - GET `/api/logs/`

---

## Librarian Actions
- **Assign a book to a user (borrow)**
  - POST `/api/librarian/assign/`
  - Body: `{ "user_id": <user_id>, "book_id": <book_id> }`
  - Response: `{ "status": "username borrowed bookname" }`
- **Return a book for a user**
  - POST `/api/librarian/return/`
  - Body: `{ "user_id": <user_id>, "book_id": <book_id> }`
  - Response: `{ "status": "username returned bookname" }`

---

## Example: Assign Book
```
POST /api/librarian/assign/
{
  "user_id": 2,
  "book_id": 5
}
```

## Example: Add to Wishlist
```
POST /api/users/2/wishlist/
{
  "book_id": 5
}
```

## Example: Get Logs
```
GET /api/logs/
```

---

For more details, use the DRF browsable API at `/api/` while logged in. 