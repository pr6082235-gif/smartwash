-- SmartWash Pro - MySQL Database Schema
-- Owner: sureshgopi
-- Version: 1.0

CREATE DATABASE IF NOT EXISTS smartwash_pro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE smartwash_pro;

-- Users Table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role ENUM('admin', 'staff') DEFAULT 'staff',
    phone VARCHAR(15),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    INDEX idx_role (role),
    INDEX idx_active (is_active)
);

-- Customers Table
CREATE TABLE customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(100),
    address TEXT,
    total_visits INT DEFAULT 0,
    total_spent DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_phone (phone),
    INDEX idx_name (name)
);

-- Orders Table
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id VARCHAR(20) UNIQUE NOT NULL,
    customer_id INT NOT NULL,
    created_by INT NOT NULL,
    service_type ENUM('wash', 'dry_clean', 'iron', 'wash_iron', 'dry_clean_iron') NOT NULL,
    dress_quantity INT NOT NULL DEFAULT 1,
    total_amount DECIMAL(10,2) NOT NULL,
    gst_amount DECIMAL(10,2) DEFAULT 0.00,
    discount DECIMAL(10,2) DEFAULT 0.00,
    final_amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'processing', 'ready', 'delivered', 'cancelled') DEFAULT 'pending',
    priority ENUM('normal', 'express') DEFAULT 'normal',
    delivery_date DATE NOT NULL,
    pickup_date TIMESTAMP NULL,
    delivery_date_actual TIMESTAMP NULL,
    notes TEXT,
    barcode VARCHAR(50) UNIQUE NOT NULL,
    pdf_path VARCHAR(255),
    whatsapp_sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE RESTRICT,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT,
    INDEX idx_order_id (order_id),
    INDEX idx_status (status),
    INDEX idx_delivery_date (delivery_date),
    INDEX idx_created_at (created_at),
    INDEX idx_customer_id (customer_id)
);

-- Order Items Table
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    item_type VARCHAR(50) NOT NULL,
    service_type ENUM('wash', 'dry_clean', 'iron', 'wash_iron') NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(8,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    INDEX idx_order_id (order_id)
);

-- Payments Table
CREATE TABLE payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method ENUM('cash', 'upi', 'card', 'bank_transfer', 'credit') DEFAULT 'cash',
    payment_status ENUM('pending', 'paid', 'partial', 'refunded') DEFAULT 'pending',
    transaction_id VARCHAR(100),
    paid_at TIMESTAMP NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE RESTRICT,
    INDEX idx_order_id (order_id),
    INDEX idx_payment_status (payment_status),
    INDEX idx_paid_at (paid_at)
);

-- Expenses Table
CREATE TABLE expenses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    category ENUM('utilities', 'supplies', 'salary', 'maintenance', 'rent', 'marketing', 'other') NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    expense_date DATE NOT NULL,
    added_by INT NOT NULL,
    receipt_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (added_by) REFERENCES users(id) ON DELETE RESTRICT,
    INDEX idx_category (category),
    INDEX idx_expense_date (expense_date)
);

-- Activity Logs Table
CREATE TABLE logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    module VARCHAR(50) NOT NULL,
    description TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_module (module),
    INDEX idx_created_at (created_at)
);

-- Service Pricing Table
CREATE TABLE service_pricing (
    id INT PRIMARY KEY AUTO_INCREMENT,
    service_name VARCHAR(100) NOT NULL,
    item_type VARCHAR(100) NOT NULL,
    service_type ENUM('wash', 'dry_clean', 'iron', 'wash_iron') NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert default admin user (password: Admin@123)
INSERT INTO users (username, email, password_hash, full_name, role) VALUES 
('sureshgopi', 'suresh@smartwashpro.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMaygI1p9XCXH7vQQvM/YBKQ.e', 'Suresh Gopi', 'admin'),
('staff1', 'staff1@smartwashpro.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMaygI1p9XCXH7vQQvM/YBKQ.e', 'Staff Member', 'staff');

-- Insert default pricing
INSERT INTO service_pricing (service_name, item_type, service_type, price) VALUES
('Shirt Wash', 'shirt', 'wash', 30.00),
('Shirt Dry Clean', 'shirt', 'dry_clean', 80.00),
('Shirt Iron', 'shirt', 'iron', 15.00),
('Shirt Wash+Iron', 'shirt', 'wash_iron', 40.00),
('Pant Wash', 'pant', 'wash', 40.00),
('Pant Dry Clean', 'pant', 'dry_clean', 100.00),
('Pant Iron', 'pant', 'iron', 20.00),
('Saree Wash', 'saree', 'wash', 60.00),
('Saree Dry Clean', 'saree', 'dry_clean', 150.00),
('Saree Iron', 'saree', 'iron', 25.00),
('Suit Dry Clean', 'suit', 'dry_clean', 250.00),
('Blanket Wash', 'blanket', 'wash', 150.00),
('Curtain Wash', 'curtain', 'wash', 100.00),
('T-Shirt Wash', 'tshirt', 'wash', 25.00),
('T-Shirt Iron', 'tshirt', 'iron', 12.00);
