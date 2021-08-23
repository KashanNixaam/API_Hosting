from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import JSON
import jsonschema
from sqlalchemy.sql.sqltypes import Boolean, DateTime, JSON , Integer
from jsonschema import validate
from jsonschema import validate, ValidationError, SchemaError
from sqlalchemy.sql.schema import Sequence
# from datetime import datetime
import datetime
schema = {

    "type": "object",
    "properties": {

        "MSH": {

            "type": "object",
            "properties": {

                "Sending App": {"type": "string"},
                "Sending Facility Name": {"type": "string", "maxlength": 60},
                "Sending Facility ID": {"type": "string", "maxlength": 12},
                "Receiving App CollaborateMD": {"type": "string"},
                "Customer Name": {"type": "string", "maxlength": 120},
                "Customer Number": {"type": "string", "maxlength": 9},
                "Date Time of Message": {"type": "string"},
                "Message Control Number": {"type": "string"},

                # "required":["Receiving App CollaborateMD","Customer Name","Customer Number", "Date Time of Message","Message Control Number"]
            }

        },

        "EVN": {

            "type": "object",
            "properties": {

                "Date Time Of Event": {"type": "string"},

                # "required":["Date Time Of Event"]

            }

        },

        "PID": {

            "type": "object",
            "properties": {

                "Sequence ID": {"type": "string"},
                "Patient Account Number in CollaborateMD": {"type": "string"},
                "Patient Account Number in Sending System": {"type": "string", "maxlength": 20},
                "Patient Social Security Number": {"type": "string", "maxlength": 9},
                "Patient Last Name": {"type": "string", "maxlength": 30},
                "Patient First Name": {"type": "string", "maxlength": 20},
                "Patient Middle Name/Initial": {"type": "string", "maxlength": 20},
                "Customer Number": {"type": "string"},
                "Patient Birth Date": {"type": "string"},
                "Patient Sex": {"type": "string"},
                "Patient Race": {"type": "string"},
                "Patient Address1": {"type": "string", "maxlength": 40},
                "Patient Address2": {"type": "string", "maxlength": 40},
                "Patient City": {"type": "string", "maxlength": 28},
                "Patient State": {"type": "string", "maxlength": 2},
                "Patient Zip Code": {"type": "string", "maxlength": 10},
                "Patient Home Phone": {"type": "string"},
                "Patient Email": {"type": "string", "maxlength": 100},
                "Patient Work Phone": {"type": "string"},
                "Patient Language": {"type": "string"},
                "Patient Marital Status": {"type": "string"},
                "Patient Account Number in Sending System (update)": {"type": "string", "maxlength": 20},
                "Patient Social Security Number (update)": {"type": "string", "maxlength": 9},
                "Patient Ethnicity": {"type": "string"},

                # "required":["Sequence ID","Patient Last Name","Patient First Name","Patient Birth Date","Patient Sex"]
            }

        },

        "NK1": {

            "type": "object",
            "properties": {

                "Set ID": {"type": "string"},
                "Next of Kin / Associated Party Last Name": {"type": "string", "maxlength": 30},
                "Next of Kin / Associated Party First Name": {"type": "string", "maxlength": 20},
                "Next of Kin / Associated Party Middle initial": {"type": "string", "maxlength": 20},
                "Next of Kin / Associated Party Relationship": {"type": "string"},
                "Next of Kin / Associated Party Address 1": {"type": "string", "maxlength": 40},
                "Next of Kin / Associated Party Address 2": {"type": "string", "maxlength": 40},
                "Next of Kin / Associated Party City": {"type": "string", "maxlength": 28},
                "Next of Kin / Associated Party State": {"type": "string", "maxlength": 2},
                "Next of Kin / Associated Party Zip": {"type": "string", "maxlength": 10},
                "Next of Kin / Associated Contact Phone": {"type": "string"},
                "Next of Kin / Associated E-Mail": {"type": "string", "maxlength": 50},
                "Next of Kin / Other-Email": {"type": "string", "maxlength": 50},

                # "required":["Set ID"]

            }
        },

        "PV1": {

            "type": "object",
            "properties": {

                "Sequence ID": {"type": "string"},
                "Patient Class": {"type": "string"},
                "Provider Reference ID": {"type": "string", "maxlength": 12},
                "Provider ID": {"type": "string"},
                "Provider Last Name": {"type": "string", "maxlength": 60},
                "Provider First Name": {"type": "string", "maxlength": 35},
                "Provider Middle Initial": {"type": "string"},
                "Provider Credentials": {"type": "string", "maxlength": 15},
                "Provider Office Location Code": {"type": "string"},
                "Referring ID": {"type": "string"},
                "Referring Last Name": {"type": "string", "maxlength": 35},
                "Referring First Name": {"type": "string", "maxlength": 20},
                "Referring Credentials": {"type": "string", "maxlength": 15},
                "Ordering ID": {"type": "string"},
                "Ordering Last Name": {"type": "string", "maxlength": 35},
                "Ordering First Name": {"type": "string", "maxlength": 20},
                "Ordering Middle Initial": {"type": "string"},
                "Ordering Credentials": {"type": "string", "maxlength": 15},

                # "required":["Sequence ID","Provider ID","Provider Last Name","Provider First Name"]

            }
        },

        "GT1": {

            "type": "object",
            "properties": {

                "Sequence ID": {"type": "string"},
                "Guarantor Last Name": {"type": "string", "maxlength": 30},
                "Guarantor First Name": {"type": "string", "maxlength": 20},
                "Guarantor Middle Initial": {"type": "string", "maxlength": 20},
                "Guarantor Address1": {"type": "string", "maxlength": 40},
                "Guarantor Address2": {"type": "string", "maxlength": 40},
                "Guarantor City": {"type": "string", "maxlength": 28},
                "Guarantor State": {"type": "string", "maxlength": 2},
                "Guarantor Zip Code": {"type": "string", "maxlength": 10},
                "Guarantor Home Phone": {"type": "string"},
                "Guarantor Work Phone": {"type": "string"},
                "Guarantor Relation to Patient": {"type": "string"},

            }
        },

        "ACC": {

            "type": "object",
            "properties": {

                "Accident Date": {"type": "string"},
                "Accident Type": {"type": "string"},
                "Accident State": {"type": "string"},

            }
        },

        "IN1": {

            "type": "object",
            "properties": {

                "Sequence ID": {"type": "string"},
                "Payer ID in Sending System": {"type": "string", "maxlength": 12},
                "Payer ID CollaborateMD internal ID": {"type": "string"},
                "Payer Name": {"type": "string", "maxlength": 80},
                "Payer Address1": {"type": "string", "maxlength": 42},
                "Payer Address2": {"type": "string", "maxlength": 42},
                "Payer City": {"type": "string", "maxlength": 28},
                "Payer State": {"type": "string", "maxlength": 2},
                "Payer Zip Code": {"type": "string", "maxlength": 10},
                "Payer Phone": {"type": "string"},
                "Payer Group Name": {"type": "string", "maxlength": 60},
                "Insurance Group Number": {"type": "string", "maxlength": 29},
                "Insured Policy Effective Date": {"type": "string"},
                "Insured Policy Termination Date": {"type": "string"},
                "Insured’s Last Name": {"type": "string", "maxlength": 30},
                "Insured’s First Name": {"type": "string", "maxlength": 20},
                "Insured’s Middle Initial": {"type": "string", "maxlength": 20},
                "Insured Relationship to Patient": {"type": "string"},
                "Insured’s Date of Birth": {"type": "string"},
                "Insurance Policy Number": {"type": "string", "maxlength": 25},
                "Insured’s Address line 1": {"type": "string", "maxlength": 40},
                "Insured’s Address line 2": {"type": "string", "maxlength": 40},
                "Insured’s City": {"type": "string", "maxlength": 28},
                "Insured’s State": {"type": "string"},
                "Insured’s Zip Code": {"type": "string"},
                "Insured’s Employment Status": {"type": "string"},
                "Insured’s Middle Initial": {"type": "string"},
                "Insured's Sex": {"type": "string"},
                "Insured Employer Address Line 1": {"type": "string", "maxlength": 40},
                "Insured Employer Address Line 2": {"type": "string", "maxlength": 40},
                "Insured Employer City": {"type": "string", "maxlength": 28},
                "Insured Employer State": {"type": "string"},
                "Insured Employer Zip Code": {"type": "string", "maxlength": 10},

                # "required":["Insured’s Last Name","Insured’s First Name","Insured Relationship to Patient"]

            }

        },

        "IN2": {

            "type": "object",
            "properties": {

                "Insured Employer Name": {"type": "string", "maxlength": 35},

            }

        },

        "DG1": {

            "type": "object",
            "properties": {

                "Patient Default Diagnosis Index": {"type": "string"},
                "ICD Code": {"type": "string", "maxlength": 8},
                "ICD Description": {"type": "string", "maxlength": 250},
                "ICD Version": {"type": "string"},

                # "required":["ICD Code","ICD Version"]

            }

        }

    }

}
app = Flask(__name__)
POSTGRES = {
    'user': 'postgres',
    'pw': 'postgresql',
    'db': 'test1',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # "postgresql://postgres:postgresql@localhost:5432/APi"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class ADT_Model(db.Model):
    __tablename__ = 'ADT'

    id = db.Column(db.Integer, primary_key=True)
    # id=db.Column(Integer, Sequence('seq_ADT_id', start=1, increment=1), primary_key=True)
    data = db.Column(JSON)
    timestamp= db.Column(db.DateTime)
    processed = db.Column(db.Boolean)

    def __init__(self, data, timestamp, processed):
        self.data= data
        self.timestamp = timestamp
        self.processed= processed

    def __repr__(self):
        return f"<ADT {self.data}>"

@app.route('/')
def hello_world():
    return 'API'
@app.route('/api', methods=['POST'])

def validateJson():
    data= request.get_json()
    try:
        validate(data,schema)
        a= True
        
    # except jsonschema.exceptions.ValidationError as err:
    except jsonschema.ValidationError as e:

        # print(e.message)
        a = False
    if a==True:
        print('Valid Data')
        now = datetime.datetime.now()
        new_data = ADT_Model(data=data, timestamp=now, processed=True)
        db.session.add(new_data)
        db.session.commit()

        return "Sucess"
    else:
        print("Data is inValid")
        return "Failed"


if __name__ == '__main__':
    db.create_all()
    app.run()