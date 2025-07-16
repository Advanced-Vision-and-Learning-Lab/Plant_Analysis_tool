# models.py
from typing import Optional, Any
from datetime import datetime, date # Import datetime for DateTime column type

from sqlalchemy import String, Date, DateTime, UniqueConstraint, ForeignKey, Float, Enum
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB # Specific to PostgreSQL
from sqlalchemy.sql import func # For default values like current date/time

import enum

class VegetationIndexEnum(enum.Enum):
    ARI = "ARI"
    ARI2 = "ARI2"
    AVI = "AVI"
    CCCI = "CCCI"
    CIgreen = "CIgreen"
    CIRE = "CIRE"
    CVI = "CVI"
    DSWI4 = "DSWI4"
    DVI = "DVI"
    EVI2 = "EVI2"
    ExR = "ExR"
    GEMI = "GEMI"
    GNDVI = "GNDVI"
    GOSAVI = "GOSAVI"
    GRNDVI = "GRNDVI"
    GRVI = "GRVI"
    GSAVI = "GSAVI"
    IPVI = "IPVI"
    LCI = "LCI"
    MCARI = "MCARI"
    MCARI1 = "MCARI1"
    MCARI2 = "MCARI2"
    MGRVI = "MGRVI"
    MSAVI = "MSAVI"
    MSR = "MSR"
    MTVI1 = "MTVI1"
    MTVI2 = "MTVI2"
    NDRE = "NDRE"
    NDVI = "NDVI"
    NDWI = "NDWI"
    NGRDI = "NGRDI"
    NLI = "NLI"
    OSAVI = "OSAVI"
    PVI = "PVI"
    RDVI = "RDVI"
    RI = "RI"
    RRI1 = "RRI1"
    SIPI2 = "SIPI2"
    SR = "SR"
    TCARI = "TCARI"
    TCARIOSAVI = "TCARIOSAVI"
    TNDVI = "TNDVI"
    TSAVI = "TSAVI"
    WDVI = "WDVI"

Base = declarative_base()

class Plant(Base):
    __tablename__ = "plants"
    id: Mapped[str] = mapped_column(String(50), primary_key=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    species: Mapped[Optional[str]] = mapped_column(String(100), nullable=False)
    # Add other metadata as needed (location, planting date, etc.)
    vegetation_indices = relationship("VegetationIndexTimeSeries", back_populates="plant")
    processed_data = relationship("ProcessedData", back_populates="plant")

    def __repr__(self) -> str:
        return f"<Plant(id={self.id}, name='{self.name}', species='{self.species}')>"
        

class ProcessedData(Base):
    __tablename__ = "processed_data"

   # Define table-level arguments like unique constraints
    # The UniqueConstraint now applies to the 'id' (which is your plant identifier)
    # and the 'date_processed' to ensure uniqueness per plant per day.
    __table_args__ = (
        UniqueConstraint('id', 'date_captured', name='_unique_plant_image_per_day'),
    )

    # Primary Key - A String like "Sorghum_plant1_2024-12-04", "Sorghum_plant2_2024-06-01", etc.
    id: Mapped[str] = mapped_column(String(50), primary_key=True, index=True)

    # Column for a user-customizable name.
    # It's nullable=True because the user might not provide one.
    name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Column for the plant identifier.
    # It's nullable=False because the plant identifier is required.
    plant_id: Mapped[str] = mapped_column(String(50), ForeignKey("plants.id"), nullable=False, index=True)

    # Column for the image key.
    # It's nullable=False because the image key is required.
    image_key: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Using DateTime for more precision, with a default to the current UTC time
    date_processed: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now()) 

    # Column for the date the image was captured.
    # It's nullable=False because the capture date is required.
    date_captured: Mapped[date] = mapped_column(Date, nullable=False)

    vegetation_features: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    morphology_features: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    texture_features: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    plant = relationship("Plant", back_populates="processed_data")

    def __repr__(self) -> str:
        return f"<ProcessedImage(id={self.id}, plant_id='{self.plant_id}', date_processed={self.date_processed})>"


class VegetationIndexTimeSeries(Base):
    __tablename__ = "vegetation_index_time_series"
    #Composite Primary Key: plant_id, date_captured, index_type
    plant_id: Mapped[str] = mapped_column(String(50), ForeignKey("plants.id"), primary_key=True)
    date_captured: Mapped[date] = mapped_column(Date, primary_key=True)
    index_type: Mapped[VegetationIndexEnum] = mapped_column(Enum(VegetationIndexEnum), primary_key=True)
    mean: Mapped[float] = mapped_column(Float, nullable=False)
    median: Mapped[float] = mapped_column(Float, nullable=False)
    std: Mapped[float] = mapped_column(Float, nullable=False)
    q25: Mapped[float] = mapped_column(Float, nullable=False)
    q75: Mapped[float] = mapped_column(Float, nullable=False)
    min: Mapped[float] = mapped_column(Float, nullable=False)
    max: Mapped[float] = mapped_column(Float, nullable=False)
    index_image_key: Mapped[str] = mapped_column(String(255), nullable=False)
    plant = relationship("Plant", back_populates="vegetation_indices")

# Example: Get NDVI time series for plant 'plant1'
# results = (
#     session.query(VegetationIndexTimeSeries)
#     .filter_by(plant_id="plant1", index_type="NDVI")
#     .order_by(VegetationIndexTimeSeries.date_captured)
#     .all()
# )

#Convert the results into lists for plotting (e.g., with matplotlib, Plotly, or for sending to a frontend)
# dates = [r.date_captured for r in results]
# means = [r.mean for r in results]
# medians = [r.median for r in results]
# stds = [r.std for r in results]
# q25s = [r.q25 for r in results]
# q75s = [r.q75 for r in results]
# mins = [r.min for r in results]
# maxs = [r.max for r in results]

