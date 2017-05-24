import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

from database_utils import DBSession
from database import PersonRel
dbs = DBSession().session

data = []
db_entries = dbs.query(PersonRel.count).filter(PersonRel.count > 1).all()
for entry in db_entries:
#     data.append([str(entry.person1) + " - " + str(entry.person2), entry.count])
    data.append(entry[0])
data.sort()
dmean = np.mean(data)
dstd = np.std(data)
pdf = stats.norm.pdf(data, dmean, dstd)

# Plot the data
plt.plot(data, pdf)

# Add a legend

# Show the plot
plt.show()

