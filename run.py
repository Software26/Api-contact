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
def get_contacts():
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
    
    
    return jsonify({"menssage":"contacto creado con exito", "contact": contact.serialize()}), 201
    

@app.route("/contacts/<int:id>", methods=["GET"])
def get_contact(id):
    contact = Contact.query.get(id)
    if not  contact : 
        return jsonify({"message":'Contacto no encontrado'}), 404
    return jsonify(contact.serialize() )

@app.route("/contacts/<int:id>", methods=["GET","PUT"])
def update_contact(id):
    contact = Contact.query.get_or_404(id)
    data = request.get_json()

    if 'name' in data:
        contact.name = data['name']
    if 'email' in data:
        contact.email = data['email']
    if 'phone' in data:
        contact.phone = data['phone']

    db.session.commit()

    return jsonify({"message": "Contacto actualizado con éxito", "contact": contact.serialize()}), 200

@app.route("/contacts/<int:id>", methods=["DELETE"])
def delete_contact(id):
    # Buscar el contacto por su ID
    contact = Contact.query.get_or_404(id)
    
    # Eliminar el contacto de la base de datos
    db.session.delete(contact)
    db.session.commit()
    
    # Devolver una respuesta JSON indicando que el contacto ha sido eliminado con éxito
    return jsonify({"message": "Contacto eliminado con éxito"}), 200
if __name__ == "__main__":
    app.run(debug=True)