from database import engine, Base
import models

Base.metadata.create_all(bind=engine)

print("Database created successfully!")
print("File: opportunity_hub.db")