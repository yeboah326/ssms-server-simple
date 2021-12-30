# Setup
- On new deployment click `Run console` from the `More` dropdown menu
- Create all your tables with `flask db init && flask db migrate && flask db upgrade`
- Create a new flask shell first with `flask shell`
- Create your super user account by running the following code
  <pre>
from api import db
from api.auth.models import SuperUser
super_user = SuperUser(name='Super User', username='s_user', email='gasante713@gmail.com')
super_user.password = 'dafda48951'
db.session.add(super_user)
db.session.commit()
  </pre>
