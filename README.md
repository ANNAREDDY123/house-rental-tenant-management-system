# house-rental-tenant-management-system
A FastAPI-based House Rental &amp; Tenant Management System with JWT Authentication, Role-Based Authorization, House Management, Tenant Management, Rent Payment Tracking, Reports, Search, Pagination, SQLAlchemy ORM, Docker Support, Logging, and Unit Testing.
# House Rental & Tenant Management System

## Features

- JWT Authentication
- Role-Based Authorization
- House Management
- Tenant Management
- Rent Payment Management
- Search & Filter
- Pagination
- Payment History
- Overdue Rent Report

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- JWT
- Pydantic

## Installation


pip install -r requirements.txt


Run the project


uvicorn main:app --reload


Swagger UI


http://127.0.0.1:8000/docs


## Roles

- Admin
- Owner
- Tenant

## Business Rules

- One active tenant per house
- One house per tenant
- Rent amount > 0
- Duplicate monthly payment not allowed
- House status auto-updates
- Aadhaar and Email must be unique
