# DoorDash Automation System - Milestone 2

## System Overview

This document outlines the implementation of an automated DoorDash ordering system with account chain management.

## Core Components

### 1. Database Schema

#### Accounts Table
```sql
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    chain_id INTEGER,
    position_in_chain INTEGER,
    referral_link TEXT,
    status VARCHAR(50), -- 'available', 'in_use', 'used'
    created_at TIMESTAMP,
    last_used_at TIMESTAMP
);
```

#### VCC Table
```sql
CREATE TABLE vccs (
    id SERIAL PRIMARY KEY,
    card_number VARCHAR(255),
    expiry VARCHAR(10),
    cvv VARCHAR(5),
    account_id INTEGER REFERENCES accounts(id),
    status VARCHAR(50), -- 'active', 'used'
    created_at TIMESTAMP
);
```

#### Orders Table
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(id),
    group_order_link TEXT,
    delivery_address TEXT,
    delivery_instructions TEXT,
    customer_name VARCHAR(255),
    customer_phone VARCHAR(20),
    order_status VARCHAR(50), -- 'pending', 'placed', 'delivered', 'failed'
    doordash_order_id VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### Chains Table
```sql
CREATE TABLE chains (
    id SERIAL PRIMARY KEY,
    status VARCHAR(50), -- 'active', 'completed'
    created_at TIMESTAMP
);
```

### 2. Account Chain Creation System

#### Chain Creation Process
1. Initialize new chain in database
2. For each account in chain (e.g., 10 accounts):
   - Create account starting from last position
   - Generate email and password
   - Register on DoorDash
   - Get referral link
   - Create next account using referral link
   - Assign VCC to account
   - Store all information in database

### 3. API Endpoints

#### Place Order Endpoint
```
POST /api/placeOrder
```

Request Body:
```json
{
    "groupOrderLink": "https://doordash.com/group-order/...",
    "deliveryAddress": "123 Main St, City, State ZIP",
    "deliveryInstructions": "Leave at door",
    "customerName": "John Doe",
    "customerPhone": "1234567890"
}
```

Response:
```json
{
    "success": true,
    "orderId": "12345",
    "message": "Order placed successfully"
}
```

### 4. Order Processing Flow

1. Receive order request
2. Validate input data
3. Parse group order link
4. Select available account from chain
   - Check chain rules
   - Verify previous order delivery
5. Login to DoorDash
6. Create regular cart
7. Add items with options
8. Apply promo code
9. Set delivery details
10. Process payment with VCC
11. Update database
12. Return order confirmation

## Implementation Guidelines

### Account Chain Management

- Create chains in sequence (E → D → C → B → A)
- Track position in chain (1 to N)
- Maintain chain status
- Monitor account usage

### Security Considerations

- Encrypt sensitive data (passwords, VCC details)
- Secure API endpoints
- Log all operations
- Handle errors gracefully

### Testing Strategy

1. Chain Creation Testing
   - Verify account creation sequence
   - Validate referral link usage
   - Check VCC assignment

2. Order Processing Testing
   - Test group order link parsing
   - Verify account selection logic
   - Validate order placement
   - Check payment processing

## Error Handling

### Common Error Scenarios

1. Account Creation Failures
   - DoorDash registration issues
   - Referral link problems
   - VCC assignment failures

2. Order Processing Failures
   - Invalid group order link
   - No available accounts
   - Payment failures
   - DoorDash system errors

## Monitoring and Logging

- Track account usage
- Monitor chain status
- Log all operations
- Track order success/failure rates

## Future Enhancements

1. Automatic chain replenishment
2. Advanced error recovery
3. Performance optimization
4. Additional payment methods