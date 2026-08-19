CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(15) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE tasks(
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(15) DEFAULT 'todo'
        CHECK (status IN ('todo', 'in-progress', 'completed')),
    completed BOOLEAN DEFAULT FALSE,
    priority VARCHAR(10) DEFAULT 'medium'
        CHECK (priority IN ('low', 'medium', 'high')),
    user_id INTEGER NOT NULL
        REFERENCES users(id)
        ON DELETE CASCADE
);