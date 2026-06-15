from flask import Flask, render_template, jsonify
import boto3
from boto3.dynamodb.conditions import Key
import random

app = Flask(__name__)

# IAM Şifrelerini buraya yapıştır
dynamodb = boto3.resource(
    'dynamodb', 
    region_name='us-east-1',
    aws_access_key_id='BURAYA_KENDI_ACCESS_KEYINIZI_YAZIN',
    aws_secret_access_key='BURAYA_KENDI_SECRET_KEYINIZI_YAZIN'
)
table = dynamodb.Table('AkilliCopKutusuVerileri')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/veri')
def get_data():
    try:
        # Sistemde kayıtlı 10 çöp kutusundan rastgele birini seçip son verisini çekiyoruz
        kutu_no = random.randint(1, 10)
        rastgele_kutu = f"AkilliCopKutusu_{kutu_no:02d}"
        
        response = table.query(
            KeyConditionExpression=Key('cihaz_id').eq(rastgele_kutu),
            ScanIndexForward=False, 
            Limit=1 
        )
        
        if response['Items']:
            son_veri = response['Items'][0]
            son_veri['doluluk_orani'] = int(son_veri['doluluk_orani'])
            return jsonify(son_veri)
        else:
            return jsonify({"hata": "Veri bekleniyor", "cihaz_id": rastgele_kutu, "doluluk_orani": 0, "durum": "Normal"}), 200
            
    except Exception as e:
        return jsonify({"hata": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)