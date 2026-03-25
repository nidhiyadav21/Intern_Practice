## Create Customer Account
**Description:** As a user, I want to create an account to become a customer, so that I can browse and purchase books.
    
**Acceptance Criteria:**
- [ ] The system allows users to enter their details to create an account.
- [ ] The system validates user input to ensure all required fields are filled.
- [ ] The system creates a new customer account and stores the user's details.

---
## Browse and Search Books
**Description:** As a customer, I want to browse and search for books, so that I can find and purchase the books I need.
    
**Acceptance Criteria:**
- [ ] The system displays a list of available books.
- [ ] The system allows customers to search for books by title, author, or genre.
- [ ] The system returns a list of search results that match the customer's query.

---
## Add Books to Shopping Cart
**Description:** As a customer, I want to add books to my shopping cart, so that I can purchase them later.
    
**Acceptance Criteria:**
- [ ] The system allows customers to add books to their shopping cart.
- [ ] The system updates the shopping cart to reflect the added book.
- [ ] The system prevents customers from adding more than one of each book to their cart.

---
## Check Out Books
**Description:** As a customer, I want to check out the books in my shopping cart, so that I can complete my purchase.
    
**Acceptance Criteria:**
- [ ] The system allows customers to check out their shopping cart.
- [ ] The system decrements the stock of the purchased books in the inventory.
- [ ] The system updates the customer's order history.

---
## Manage Inventory
**Description:** As a manager, I want to manage the inventory with full create, retrieve, update, and delete (CRUD) functionality, so that I can keep the book stock up to date.
    
**Acceptance Criteria:**
- [ ] The system allows managers to create new book entries.
- [ ] The system allows managers to retrieve and view book details.
- [ ] The system allows managers to update book details, including stock quantities and prices.
- [ ] The system allows managers to delete book entries.

---
## Interact with Promotion System
**Description:** As a customer or manager, I want to interact with a promotion system that handles percentage-off promotions, so that I can apply promotions to orders.
    
**Acceptance Criteria:**
- [ ] The system allows customers to view available promotions.
- [ ] The system allows customers to apply a promotion to their order.
- [ ] The system applies the promotion to the order and updates the total cost.

---
## Send Promotions and Low-Stock Notifications
**Description:** As a manager, I want the system to send promotions to customers and low-stock notifications to me, so that I can keep customers informed and manage the inventory.
    
**Acceptance Criteria:**
- [ ] The system sends promotions to customers via email.
- [ ] The system sends low-stock notifications to managers via email.
- [ ] The system triggers low-stock notifications when the stock of a book falls below a certain threshold.

---
## Specify Stop-Order for a Book
**Description:** As a manager, I want to specify a stop-order for a book, so that I can prevent further sales when the stock reaches a certain level.
    
**Acceptance Criteria:**
- [ ] The system allows managers to set a stop-order for a book.
- [ ] The system prevents customers from purchasing the book when the stock reaches the stop-order level.
- [ ] The system notifies managers when the stock of a book reaches the stop-order level.

---
## Notify Managers of Reorder Needs
**Description:** As a manager, I want the system to notify me when books need to be reordered, so that I can maintain the inventory.
    
**Acceptance Criteria:**
- [ ] The system tracks the stock levels of books.
- [ ] The system notifies managers when the stock of a book falls below a certain threshold.
- [ ] The system provides managers with a list of books that need to be reordered.

---
## Update Stock Quantities and Prices
**Description:** As a manager, I want to update stock quantities and change book prices, so that I can keep the inventory up to date.
    
**Acceptance Criteria:**
- [ ] The system allows managers to update stock quantities.
- [ ] The system allows managers to change book prices.
- [ ] The system updates the inventory and reflects the changes in the system.

---
## View Transaction Logs
**Description:** As a manager, I want to view transaction logs, so that I can track sales and inventory changes.
    
**Acceptance Criteria:**
- [ ] The system provides managers with access to transaction logs.
- [ ] The system displays a list of all transactions, including sales and inventory changes.
- [ ] The system allows managers to filter and search transaction logs.

---
## Create Promotions
**Description:** As a manager, I want to create promotions, so that I can offer discounts to customers.
    
**Acceptance Criteria:**
- [ ] The system allows managers to create new promotions.
- [ ] The system allows managers to specify the details of the promotion, including the discount percentage and duration.
- [ ] The system adds the new promotion to the list of available promotions.

---
## System Availability
**Description:** As a user, I want the system to be available on the Computer Science Department's provided computer resources, so that I can access the system from the MSU Engineering Building.
    
**Acceptance Criteria:**
- [ ] The system is accessible from the Computer Science Department's provided computer resources.
- [ ] The system is compatible with the department's hardware and software.
- [ ] The system is available for use during the department's operating hours.

---
## Browser Compatibility
**Description:** As a user, I want the system to work correctly in Internet Explorer and Mozilla Firefox, so that I can access the system from different browsers.
    
**Acceptance Criteria:**
- [ ] The system is compatible with Internet Explorer.
- [ ] The system is compatible with Mozilla Firefox.
- [ ] The system functions correctly in both browsers.

---
## Credit Card Processing
**Description:** As a system, I want to not have full credit-card processing capabilities, so that I can avoid the security risks associated with storing credit card information.
    
**Acceptance Criteria:**
- [ ] The system does not store credit card information.
- [ ] The system does not process credit card transactions.
- [ ] The system provides alternative payment methods, such as cash or check.

---
## Manager and Customer Roles
**Description:** As a system, I want to not allow managers to be customers, so that I can maintain the separation of roles.
    
**Acceptance Criteria:**
- [ ] The system prevents managers from creating customer accounts.
- [ ] The system restricts managers to their managerial roles.
- [ ] The system ensures that managers and customers have separate accounts and permissions.

---
## Promotion Limitations
**Description:** As a system, I want to not allow multiple promotions to be added to a single shopping cart, so that I can prevent abuse of the promotion system.
    
**Acceptance Criteria:**
- [ ] The system limits each shopping cart to one promotion.
- [ ] The system prevents customers from applying multiple promotions to a single order.
- [ ] The system ensures that promotions are applied fairly and consistently.

---
## Cart Item Limitations
**Description:** As a system, I want to not allow customers to add more than one of each item to their cart, so that I can prevent abuse of the shopping cart system.
    
**Acceptance Criteria:**
- [ ] The system limits each item in the shopping cart to a quantity of one.
- [ ] The system prevents customers from adding multiple instances of the same item to their cart.
- [ ] The system ensures that customers can only purchase one of each item per order.

---
## Password and Account Security
**Description:** As a system, I want to not allow users to retrieve passwords or edit their user details, so that I can maintain the security of user accounts.
    
**Acceptance Criteria:**
- [ ] The system does not provide a password retrieval feature.
- [ ] The system does not allow users to edit their account details.
- [ ] The system ensures that user accounts are secure and protected.

---
## Security Considerations
**Description:** As a system, I want to prioritize security, so that I can protect user data and prevent unauthorized access.
    
**Acceptance Criteria:**
- [ ] The system stores passwords in plain text.
- [ ] The system does not implement additional security measures, such as encryption or firewalls.
- [ ] The system is not designed to be secure, as per the requirements.

---
## Browser Compatibility Limitations
**Description:** As a system, I want to not work correctly with Internet browsers other than Firefox and Internet Explorer, so that I can focus on supporting the most commonly used browsers.
    
**Acceptance Criteria:**
- [ ] The system is not compatible with browsers other than Firefox and Internet Explorer.
- [ ] The system may not function correctly in other browsers.
- [ ] The system is designed to work only with Firefox and Internet Explorer.