# Product Warranty Claim Processing Platform

## Project Overview

The Product Warranty Claim Processing Platform is a web-based application developed using Flask and MySQL. It allows users to register products, track warranty periods, submit warranty claims, and enables administrators to manage claims efficiently.

The system minimizes manual paperwork and provides a centralized platform for warranty management.

---

## Features

### User

- User Registration
- User Login
- Dashboard
- Register Product
- View Registered Products
- Check Warranty Status
- Submit Warranty Claim

### Admin

- Admin Login
- Admin Dashboard
- View Warranty Claims
- Approve Claims
- Reject Claims
- Search Warranty Claims

---

## Technology Stack

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- AOS Animation Library

### Backend

- Python
- Flask

### Database

- MySQL

### Tools

- VS Code
- Git
- GitHub

---

## Project Structure

```
Product_Warranty_Claim/
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── admin_dashboard.html
│   ├── add_product.html
│   ├── view_products.html
│   ├── warranty_status.html
│   ├── claim.html
│   └── view_claims.html
│
├── docs/
│   ├── Problem_Statement.md
│   └── diagram/
│
├── app.py
├── config.py
├── README.md
└── .gitignore
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Pratheesh007-code/Product-Warranty-Claim-Processing-Platform.git
```

### Open Project

```bash
cd Product_Warranty_Claim
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

### Install Required Packages

```bash
pip install flask mysql-connector-python
```

### Run Project

```bash
python app.py
```

---

## Database

Database Name

```
warranty_db
```

Tables

- users
- products
- claims

---

## Future Enhancements

- Email Notifications
- QR Code Product Registration
- Product Image Upload
- PDF Warranty Certificate
- Analytics Dashboard
- Cloud Deployment

---

## Author

**Pratheesh**

B.Tech Student

JJ College of Engineering

GitHub:

https://github.com/Pratheesh007-code

---

## License

This project is developed for educational purposes.