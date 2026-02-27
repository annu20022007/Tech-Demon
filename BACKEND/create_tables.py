from fin_ai.database import engine
from fin_ai.models import models as m

m.Base.metadata.create_all(bind=engine)
print('Created tables from models.Base')
