# Jandsheic: ID & Password Generator

A small étude  that generates user IDs and random passwords from a person's name. Built for first-time access scenarios such as training phases, onboarding, etc.

The applicable environments can be human resources, schools and training centers, libraries,  customer service lockers among others.

This program is presented in 2 versions: CLI and  decorated.

<img width="1414" height="396" alt="image" src="https://github.com/user-attachments/assets/ceb1d0cb-1acb-4600-9f42-d38fe5bd7660" />

## How it works

The user or administrator enters a first and last name, and the program generates:

**User ID** – built from:
1. First 2 letters of the first name
2. Last 2 letters of the last name
3. Month of registration (2 digits)
4. 3 random characters as a differentiator
> **Example:** Peter Smith, registered on October 1st → `pesm10476`

**Password** – 6 random characters generated with Python's [`secrets`](https://docs.python.org/3/library/secrets.html) module.

## Modes

### Admin mode
Designed for **bulk registration** of new members (e.g., teachers, facilitators, HR staff).

- The program asks how many users will be registered.
- It returns an ID and password for each one, to be used as first-time access credentials.
- After pressing **F5** the results are exported to a file.

<img width="1040" height="210" alt="image" src="https://github.com/user-attachments/assets/0e37df99-3d55-4189-9fac-609389d1c424" />

### Terminal mode
Designed for **individual use** (e.g., students or anyone who needs a password).

- Takes a first and last name and generates a user ID and password.
- Can automatically create a file that logs all activity for the day.

- <img width="667" height="187" alt="image" src="https://github.com/user-attachments/assets/16de72b6-d559-46dd-9ce7-ca835f080c60" />

## Output

Currently, credentials are saved locally as a `.csv` file.
## Future steps

- [ ] Test with a SQL database
- [ ] Test in an AWS environment

