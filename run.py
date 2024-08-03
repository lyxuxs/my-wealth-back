from app import app
import http.server
import ssl

@app.route('/', methods=['GET'])
def index():
    return "Hello,this is MW back!"
 
if __name__ == '__main__':
    context = ('/root/my-wealth-back/server.crt', '/root/my-wealth-back/server.key')
    app.run(debug=True, host='0.0.0.0', port=443, ssl_context=context)
