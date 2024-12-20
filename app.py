# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from flask import Flask, jsonify, request, render_template
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import os
import json

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb',region_name=os.environ['AWS_REGION'])
table = dynamodb.Table(os.environ['DDB_TABLE'])


#Home Page
@app.route('/')
def home():
  return render_template('index.html')


# POST /api/whatsapp
@app.route('/api/whatsapp', methods=['POST'])
def whatsapp_reply():
  try:
    d = json.dumps(request.__dict__, sort_keys=True, indent=4)
  except:
    d = "ERROR"

  return { 
       'msg': f'request={request}\n\ntype(request)={type(request)}\n\nrequest.__dict__={d}\n\ndir(request)={dir(request)}',
       'response': "success"
   }


if __name__ == "__main__":
   app.run(host="0.0.0.0", port=8080)
