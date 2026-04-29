CREATE TABLE contracts (
                           id BIGSERIAL PRIMARY KEY,
                           contract_name VARCHAR(255) NOT NULL,
                           vendor_name VARCHAR(255),
                           description TEXT,
                           summary TEXT,
                           status VARCHAR(50),
                           risk_score DOUBLE PRECISION,
                           file_name VARCHAR(255),
                           created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                           updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);