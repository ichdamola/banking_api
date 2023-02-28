## Setup

git clone https://github.com/ichdamola/banking_api.git

cd into the banking_api directory

python3 -m venv umba_env

source umba_env/bin/activate

bash setup.sh


## API shot:

<img width="1280" alt="Screen Shot 2023-02-28 at 11 56 35 AM" src="https://user-images.githubusercontent.com/20647487/221834421-8a2d79f1-c80b-4434-bcd5-f39133e0e179.png">


## Entity Diagram:
- This diagram represents three entities - User, Account, and Transaction. The User entity is connected to the Account entity through a one-to-many relationship, and the Account entity is connected to the Transaction entity through another one-to-many relationship.

```
+------------------+         +------------------+         +---------------------+
| User             |         | Account          |         | Transaction         |
+------------------+         +------------------+         +---------------------+
| - first_name     |         | - user           |         | - account           |
| - last_name      |         | - account_name   |         | - amount            |
| - email          |-------1 | - account_number |-------1 | - description       |
| - phone_number   |         | - amount         |         | - type              |
| - password       |         |                  |         | - ip_address        |
|                  |         |                  |         | - timestamp         |
+------------------+         +------------------+         +---------------------+
```

## UML diagram:
- This UML diagram is similar to the entity diagram, with the addition of data types for each attribute, and the inclusion of cardinality indicators. The cardinality indicators indicate the relationship between entities and the number of objects that can be involved in that relationship.

```
+---------------------+           +-------------------------+           +---------------------+
|      User           |           |     Account             |           |     Transaction     |
+---------------------+           +-------------------------+           +---------------------+
| -first_name: str    |           | -account_name: str      |           | -amount: decimal    |
| -last_name: str     |           | -account_number: str    |           | -description: str   |
| -email: str         |<>--------1|                         |<>---------| -type: str          |
| -phone_number: str  |           | -amount: decimal        |1--------->| -ip_address: str    |
| -password: str      |           | -user: User             |           | -timestamp: datetime|
|                     |1--------->| -transactions: QuerySet |           |                     |
+---------------------+           +-------------------------+           +---------------------+
```

## Use case diagram:
- The use case diagram shows the different actions that a user can perform in the system. The user can sign up for an account, log in to their account, view their account details, deposit money, withdraw money, and transfer money to another account.

- Note: The use case diagram does not show any actors or external systems that interact with the banking application. It is focused on the actions that a user can perform within the system.

```
+-------------------------------------------+
|            Banking Application            |
+-------------------------------------------+
|                 User                      |
+-------------------------------------------+
| - Sign Up                                 |
| - Log In                                  |
| - View Account                            |
| - Deposit Money                           |
| - Withdraw Money                          |
| - Transfer Money                          |
+-------------------------------------------+
```

