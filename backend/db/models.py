# models.py

from sqlalchemy import Column, Integer, String, Date, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProcessedImage(Base):
    __tablename__ = "processed_images"

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(String, index=True)
    image_key = Column(String)
    date = Column(Date)
    vegetation_features = Column(JSON)
    morphology_features = Column(JSON)
    texture_features = Column(JSON)
