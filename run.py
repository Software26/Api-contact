from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.db'
db = SQLAlchemy(app)

#crear Modelo de base de datos

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True) #Llave primaria
    name = db.Column(db.String(80), nullable=False) #
    email = db.Column(db.String(120), unique=True)   #Correo electronico con restric        
    phone = db.Column(db.String(80), nullable=False)  #Telefono
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }
        
#Crear las tablas
with app.app_context():
    db.create_all()
 
 
 # Crear rutas   
@app.route("/contacts", methods=["GET"])
def get_contact():
    contacts = Contact.query.all()
    list_contact = []
    for cantact in contacts:
        list_contact.append(cantact.serialize())
    return jsonify({'contacs':[contact.serialize() for contact in contacts]})
    
@app.route("/contacts", methods=["POST"])
def create_contact():
    data = request.get_json()
    contact = Contact(name =  data['name'], email = data["email"], phone = data["phone"])
    db.session.add(contact)
    db.session.commit()
    
    
    return jsonify({"menssage":"contacto creado con exito", "contact": contact.serialize()})
    
    
if __name__ == "__main__":
    app.run(debug=True)