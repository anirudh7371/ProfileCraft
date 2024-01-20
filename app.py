from flask import Flask, render_template, request
import pymongo
import logging
import certifi
logging.basicConfig(filename="scrapper.log", level=logging.INFO)

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home_page():
    return render_template("index.html")

@app.route('/details', methods=['GET', 'POST'])
def personal_details():
    form_data = {}
    if request.method == "POST":
        try:
            name = request.form.get("fname")
            password = request.form.get("pass")
            emailid = request.form.get("email")
            gender = request.form.get("gender")
            contact = request.form.get("contact")
            degree = request.form.get("degree")
            engineering = request.form.get("engineering")
            hobbies = request.form.getlist("hobbies")
            address = request.form.get("address")
            resume_file = request.form.get("resumefile") if 'resumefile' in request.files else None

            form_data = {
                "name": name,
                "password": password,
                "email": emailid,
                "gender": gender,
                "contact": contact,
                "degree": degree,
                "engineering": engineering,
                "hobbies": hobbies,
                "address": address,
                "resume_file": resume_file,
            }
        except Exception as e:
            logging.error(e)
        

        uri = "mongodb+srv://anirudh7371:phoenix2509@cluster0.nzme8dh.mongodb.net/?retryWrites=true&w=majority"

        # Create a new client and connect to the server
        client = pymongo.MongoClient(uri, tlsCAFile=certifi.where())

        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            db=client["personal_details"]
            col=db["detials_data"]
            col.insert_one(form_data)
        except Exception as e:
            print(e)

        return render_template("result.html", form_data= form_data)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
