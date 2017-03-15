from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sandbox.alchemy_database import base, Article, Reference


engine = create_engine('sqlite:///alchemybrain.db')
base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# DBSession is de staging area waar de queries blijven tot commit()
session = DBSession()

art1_url = "https://www.brainpickings.org/2017/03/14/einstein-grieving-father-letter/"
art1_title = "Einstein’s Remarkable Letter to a Grief-Stricken Father Who Had Just Lost His Son"
art2_url = "https://www.brainpickings.org/2012/04/09/dear-professor-einstein-girl/"
art2_title = "Women in Science: Einstein’s Advice to a Little Girl Who Wants to Be a Scientist"
art3_url = "https://www.brainpickings.org/2017/03/13/letters-of-consolation/"
art3_title = "Living and Loving Through Loss: Beautiful Letters of Consolation from Great Artists, Writers, and Scientists"

# name articles
art1 = Article(url=art1_url, title=art1_title)
art2 = Article(url=art2_url, title=art2_title)
art3 = Article(url=art3_url, title=art3_title)
# insert articles
session.add(art1)
session.add(art2)
session.add(art3)

ref1_id = 1
ref1_url = "https://www.brainpickings.org/2017/03/14/einstein-grieving-father-letter/"
ref1_ref = "https://www.brainpickings.org/2012/04/09/dear-professor-einstein-girl/"
ref2_id = 2
ref2_url = "https://www.brainpickings.org/2017/03/14/einstein-grieving-father-letter/"
ref2_ref = "https://www.brainpickings.org/2017/03/13/letters-of-consolation/"

# name references
ref1 = Reference(id=ref1_id, url=ref1_url, ref=ref1_ref)
ref2 = Reference(id=ref2_id, url=ref2_url, ref=ref2_ref)
# insert references
session.add(ref1)
session.add(ref2)

# commit changes
session.commit()