import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Load environment variables
load_dotenv()

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, index=True)
    password = Column(String, unique=True, index=True)
    account_url = Column(String, unique=True, index=True)

    products = relationship("Product", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.login})>"


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to users table
    title = Column(String, index=True)
    price = Column(String, index=True)
    company = Column(String, index=True)
    size = Column(String, index=True)
    condition = Column(String, index=True)
    color = Column(String, index=True)
    location = Column(String, index=True)
    payment_method = Column(String, index=True)
    description = Column(String, index=True)
    category = Column(String, index=True)
    unique_identifier = Column(String, index=True)

    images = relationship("ProductImage", back_populates="product")
    user = relationship("User", back_populates="products")

    def __repr__(self):
        return f"<Product(id={self.id}, title={self.title})>"


class ProductImage(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), index=True)  # Foreign key to products table
    main_images_path = Column(String, index=True)
    original_image_path = Column(String, index=True)
    fake_image_path = Column(String, index=True)

    product = relationship("Product", back_populates="images")

    def __repr__(self):
        return f"<ProductImage(id={self.id}, product_id={self.product_id}, image_path={self.original_image_path})>"


# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(engine)





