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
- **Upload/change book photo** (librarian only)
  - PUT/PATCH `/api/books/{id}/photo/`
  - Form-data: book_photo (file)
- **Issue a book to a user** (librarian only)
  - POST/PATCH `/api/books/{id}/issue/`
  - Body: `{ "user_id": <user_id> }`
  - Response: `{ "status": "Book issued to username" }`

---

## Users
- **List all users** (librarian only)
  - GET `/api/users/`
- **Retrieve a user** (librarian only)
  - GET `/api/users/{id}/`
- **Edit user profile** (self or librarian)
  - PUT/PATCH `/api/users/{id}/profile/`
  - Fields: username, email, userdob, profile_pic
- **Change password** (self or librarian)
  - POST `/api/users/{id}/change_password/`
  - Body: `{ "password": "newpassword" }`
- **List books borrowed by a user**
  - GET `/api/users/{id}/borrowed/`
- **Get a user's notifications/logs**
  - GET `/api/users/{id}/logs/`

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
- **List all users with their borrowed books**
  - GET `/api/librarian/users_borrowed/`

---

## Example: Issue Book via Book API
```
POST /api/books/5/issue/
{
  "user_id": 2
}
```

## Example: Edit User Profile
```
PATCH /api/users/2/profile/
{
  "username": "newname",
  "userdob": "2000-01-01"
}
```

## Example: Upload Book Photo
```
PATCH /api/books/5/photo/
(form-data: book_photo=<file>)
```

## Example: Get User's Borrowed Books
```
GET /api/users/2/borrowed/
```

## Example: Change Password
```
POST /api/users/2/change_password/
{
  "password": "newpassword"
}
```

## Example: Get User Logs
```
GET /api/users/2/logs/
```

## Example: List All Users with Borrowed Books (Librarian)
```
GET /api/librarian/users_borrowed/
```

---

For more details, use the DRF browsable API at `/api/` while logged in. 