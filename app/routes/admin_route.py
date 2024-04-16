from app import app
from app import db
from app.models.admin_model import Admin


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'Hello World!'