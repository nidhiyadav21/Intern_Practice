# Tasks
## Create Customer Account
- [ ] Design and implement the customer account creation feature
  - Create a user interface for customers to enter their details
  - Validate user input to ensure all required fields are filled
  - Create a new customer account and store the user's details in the database

## Browse and Search Books
- [ ] Develop the book browsing and searching functionality
  - Display a list of available books
  - Implement a search function that allows customers to search for books by title, author, or genre
  - Return a list of search results that match the customer's query

## Add Books to Shopping Cart
- [ ] Implement the shopping cart functionality
  - Allow customers to add books to their shopping cart
  - Update the shopping cart to reflect the added book
  - Prevent customers from adding more than one of each book to their cart

## Check Out Books
- [ ] Develop the checkout functionality
  - Allow customers to check out their shopping cart
  - Decrement the stock of the purchased books in the inventory
  - Update the customer's order history

## Manage Inventory
- [ ] Implement the inventory management feature
  - Allow managers to create new book entries
  - Allow managers to retrieve and view book details
  - Allow managers to update book details, including stock quantities and prices
  - Allow managers to delete book entries

## Interact with Promotion System
- [ ] Develop the promotion system
  - Allow customers to view available promotions
  - Allow customers to apply a promotion to their order
  - Apply the promotion to the order and update the total cost

## Send Promotions and Low-Stock Notifications
- [ ] Implement the notification system
  - Send promotions to customers via email
  - Send low-stock notifications to managers via email
  - Trigger low-stock notifications when the stock of a book falls below a certain threshold

## Specify Stop-Order for a Book
- [ ] Implement the stop-order feature
  - Allow managers to set a stop-order for a book
  - Prevent customers from purchasing the book when the stock reaches the stop-order level
  - Notify managers when the stock of a book reaches the stop-order level

## Notify Managers of Reorder Needs
- [ ] Develop the reorder notification system
  - Track the stock levels of books
  - Notify managers when the stock of a book falls below a certain threshold
  - Provide managers with a list of books that need to be reordered

## Update Stock Quantities and Prices
- [ ] Implement the stock update feature
  - Allow managers to update stock quantities
  - Allow managers to change book prices
  - Update the inventory and reflect the changes in the system

## View Transaction Logs
- [ ] Develop the transaction log feature
  - Provide managers with access to transaction logs
  - Display a list of all transactions, including sales and inventory changes
  - Allow managers to filter and search transaction logs

## Create Promotions
- [ ] Implement the promotion creation feature
  - Allow managers to create new promotions
  - Allow managers to specify the details of the promotion, including the discount percentage and duration
  - Add the new promotion to the list of available promotions

## System Availability
- [ ] Ensure system availability
  - Make the system accessible from the Computer Science Department's provided computer resources
  - Ensure the system is compatible with the department's hardware and software
  - Ensure the system is available for use during the department's operating hours

## Browser Compatibility
- [ ] Ensure browser compatibility
  - Make the system compatible with Internet Explorer
  - Make the system compatible with Mozilla Firefox
  - Ensure the system functions correctly in both browsers

## Credit Card Processing
- [ ] Implement alternative payment methods
  - Do not store credit card information
  - Do not process credit card transactions
  - Provide alternative payment methods, such as cash or check

## Manager and Customer Roles
- [ ] Implement role-based access control
  - Prevent managers from creating customer accounts
  - Restrict managers to their managerial roles
  - Ensure that managers and customers have separate accounts and permissions

## Promotion Limitations
- [ ] Implement promotion limitations
  - Limit each shopping cart to one promotion
  - Prevent customers from applying multiple promotions to a single order
  - Ensure that promotions are applied fairly and consistently

## Cart Item Limitations
- [ ] Implement cart item limitations
  - Limit each item in the shopping cart to a quantity of one
  - Prevent customers from adding multiple instances of the same item to their cart
  - Ensure that customers can only purchase one of each item per order

## Password and Account Security
- [ ] Implement account security measures
  - Do not provide a password retrieval feature
  - Do not allow users to edit their account details
  - Ensure that user accounts are secure and protected

## Security Considerations
- [ ] Prioritize security
  - Note: The acceptance criteria for this user story are not secure and should not be implemented in a real-world system.
  - In a real-world system, passwords should be stored securely using a hashing algorithm, and additional security measures such as encryption and firewalls should be implemented.

## Browser Compatibility Limitations
- [ ] Implement browser compatibility limitations
  - Make the system incompatible with browsers other than Firefox and Internet Explorer
  - Note: This is not a recommended approach, as it may limit the accessibility of the system.
  - In a real-world system, it is recommended to make the system compatible with as many browsers as possible.