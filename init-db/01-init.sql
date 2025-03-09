-- ایجاد جدول کاربران
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    bio TEXT,
    profile_image_url VARCHAR(255),
    is_artist BOOLEAN DEFAULT false,
    is_admin BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ایجاد جدول آثار هنری
CREATE TABLE artworks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    artist_id INTEGER REFERENCES users(id),
    image_url VARCHAR(255) NOT NULL,
    price DECIMAL(10,2),
    medium VARCHAR(50),  -- نوع اثر (نقاشی، عکس، مجسمه و...)
    dimensions VARCHAR(50), -- ابعاد اثر
    year_created INTEGER,
    is_available BOOLEAN DEFAULT true,
    views_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ایجاد جدول دسته‌بندی‌ها
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    parent_id INTEGER REFERENCES categories(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ایجاد جدول ارتباطی آثار و دسته‌بندی‌ها
CREATE TABLE artwork_categories (
    artwork_id INTEGER REFERENCES artworks(id),
    category_id INTEGER REFERENCES categories(id),
    PRIMARY KEY (artwork_id, category_id)
);

-- ایجاد جدول نظرات
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    artwork_id INTEGER REFERENCES artworks(id),
    user_id INTEGER REFERENCES users(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ایجاد جدول لایک‌ها
CREATE TABLE likes (
    user_id INTEGER REFERENCES users(id),
    artwork_id INTEGER REFERENCES artworks(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, artwork_id)
);

-- ایجاد جدول سفارش‌ها
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL, -- 'pending', 'paid', 'cancelled'
    shipping_address TEXT,
    tracking_number VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ایجاد جدول جزئیات سفارش
CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders(id),
    artwork_id INTEGER REFERENCES artworks(id),
    price DECIMAL(10,2) NOT NULL,
    quantity INTEGER DEFAULT 1,
    PRIMARY KEY (order_id, artwork_id)
);

-- اضافه کردن برخی دسته‌بندی‌های پایه
INSERT INTO categories (name, description) VALUES
('نقاشی', 'آثار نقاشی با تکنیک‌های مختلف'),
('عکاسی', 'عکس‌های هنری و مستند'),
('مجسمه‌سازی', 'آثار حجمی و مجسمه'),
('خوشنویسی', 'آثار خوشنویسی و خط'),
('گرافیک', 'آثار گرافیکی و دیجیتال');

-- ایجاد یک کاربر ادمین
INSERT INTO users (username, email, password_hash, full_name, is_admin) 
VALUES ('admin', 'admin@ma2ta.com', '$2a$10$kbGR1PxpdPeiVPv4P5Z6C.C3I1hgnY2Y8Y8K9X8K8Y8K9X8K8Y8K9', 'مدیر سیستم', true);