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
    d = request.__dict__
  except:
    d = "ERROR"

  try:
    data = request.get_data()
  except:
    data = "ERROR"

  try:
    my_json = request.get_json()
  except:
    my_json = "ERROR"

  try:
    body = request.body
  except:
    body = "ERROR"

  try:
    body2 = request['body']
  except:
    body2 = "ERROR"

  try:
    body3 = request.values.get('Body', None)
  except:
    body3 = "ERROR"

  msg = f'request={request}, type(request)={type(request)}, request.__dict__={d}, dir(request)={dir(request)}, ' + \
    f'request.get_data()={data}, request.get_json()={my_json}, request.body={body}, request[\'body\']={body2}, request.values.get(\'Body\', None)={body3}'

  return { 
       'msg': msg,
       'response': "success"
   }


if __name__ == "__main__":
   app.run(host="0.0.0.0", port=8080)
