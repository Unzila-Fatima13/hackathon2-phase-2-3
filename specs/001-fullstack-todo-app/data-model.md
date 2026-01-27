# Data Model: Full-Stack Multi-User Todo Application

## Entity: User

**Description:** Represents a registered user in the system

**Fields:**
- `id` (UUID/Integer): Unique identifier for the user
- `email` (String): User's email address (unique, required)
- `password_hash` (String): Hashed password for authentication
- `created_at` (DateTime): Timestamp when user account was created
- `updated_at` (DateTime): Timestamp when user account was last updated
- `is_active` (Boolean): Whether the account is active (default: true)

**Relationships:**
- One-to-Many: User → Tasks (user owns multiple tasks)

**Validation Rules:**
- Email must be a valid email format
- Email must be unique across all users
- Password must meet security requirements (min length, complexity)
- Email and password required for registration

## Entity: Task

**Description:** Represents a todo item created by a user

**Fields:**
- `id` (UUID/Integer): Unique identifier for the task
- `title` (String): Task title or subject (required)
- `description` (Text): Detailed description of the task (optional)
- `is_completed` (Boolean): Whether the task is completed (default: false)
- `created_at` (DateTime): Timestamp when task was created
- `updated_at` (DateTime): Timestamp when task was last updated
- `due_date` (DateTime): Optional deadline for the task
- `user_id` (UUID/Integer): Foreign key linking to the owning user

**Relationships:**
- Many-to-One: Task → User (task belongs to one user)

**Validation Rules:**
- Title is required and must be between 1-255 characters
- Description, if provided, must be less than 10000 characters
- User_id must reference an existing user
- Due date, if provided, must be in the future
- Only the owner can modify or delete the task

## State Transitions

### Task State Transitions
- **Created**: When a task is first added (is_completed = false)
- **Completed**: When user marks task as completed (is_completed = true)
- **Reopened**: When user reopens a completed task (is_completed = false)
- **Deleted**: When user deletes the task (removed from active tasks)

## Access Control Rules

### User-Specific Access
- Users can only view, modify, or delete their own tasks
- Users cannot access tasks owned by other users
- API requests must validate that user_id in JWT matches task's user_id
- Unauthorized access attempts return HTTP 401 or 403

## Indexes

### Recommended Database Indexes
- User.email (for authentication lookups)
- Task.user_id (for user-specific queries)
- Task.created_at (for chronological ordering)
- Task.is_completed (for filtering completed/incomplete tasks)