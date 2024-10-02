CREATE TABLE "Users" (
    "UserId" SERIAL PRIMARY KEY,  -- Automatically generated unique UserId
    "Username" VARCHAR(255) NOT NULL UNIQUE,  -- Username cannot be blank and must be unique
    "Email" VARCHAR(255) NOT NULL UNIQUE,  -- Email cannot be blank and must be unique
    "PasswordHash" TEXT NOT NULL,  -- Password cannot be blank
    "CreatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Automatically set timestamp when a new record is created
);
