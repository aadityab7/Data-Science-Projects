DROP TABLE IF EXISTS batches CASCADE;                    
DROP TABLE IF EXISTS images CASCADE;                     
DROP TABLE IF EXISTS models CASCADE;            
DROP TABLE IF EXISTS extracted_texts CASCADE;  
DROP TABLE IF EXISTS batch_model_progress CASCADE;            

CREATE TABLE IF NOT EXISTS batches (
    batch_id SERIAL PRIMARY KEY, 
    num_images INTEGER DEFAULT 0,
    models_list INTEGER[] DEFAULT ARRAY[]::integer[],
    processed_models_list INTEGER[] DEFAULT ARRAY[]::integer[],
    creation_datetime timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS images (
    image_id SERIAL PRIMARY KEY, 
    batch_id INTEGER REFERENCES batches(batch_id), 
    url TEXT
);

CREATE TABLE IF NOT EXISTS models (
    model_id SERIAL PRIMARY KEY, 
    name TEXT, 
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS extracted_texts (
    image_id INTEGER REFERENCES images(image_id), 
    model_id INTEGER REFERENCES models(model_id), 
    extracted_text TEXT,
    creation_datetime timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (image_id, model_id)
);

CREATE TABLE IF NOT EXISTS batch_model_progress (
    batch_id INTEGER REFERENCES batches(batch_id),
    model_id INTEGER REFERENCES models(model_id),
    num_processed INTEGER DEFAULT 0,
    PRIMARY KEY (batch_id, model_id)
);

INSERT INTO models 
    (name, available) 
VALUES 
    ('easy_ocr', true), 
    ('keras_ocr', false), 
    ('pix2text', false), 
    ('pytesseract', true), 
    ('google_document_ai', false),
    ('meta_nougat', false);