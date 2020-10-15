# -*- coding: utf-8 -*-

import json

from flask import Flask, request
from jinja2 import Environment

app = Flask(__name__)
environment = Environment()


def jsonfilter(value):
    return json.dumps(value)

environment.filters["json"] = jsonfilter

with open('call_john/contacts.json' , 'r') as json_file:
  CONTACT_LIST = json.load(json_file)

CONTACT_LIST["contact_john"]["mobile"] = "0701234567"
CONTACT_LIST["contact_john"]["work"] = "0736582934"
CONTACT_LIST["contact_john"]["home"] = "031122363"
CONTACT_LIST["contact_mary"]["mobile"] = "0706574839"
CONTACT_LIST["contact_mary"]["work"] = "0784736475"
CONTACT_LIST["contact_mary"]["home"] = "031847528"

'''
with open('call_john/contacts.json' , 'w') as json_file:
    json.dump(CONTACT_LIST, json_file)
'''

def error_response(message):
    response_template = environment.from_string("""
    {
      "status": "error",
      "message": {{message|json}},
      "data": {
        "version": "1.0"
      }
    }
    """)
    payload = response_template.render(message=message)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


def query_response(value, grammar_entry):
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.1",
        "result": [
          {
            "value": {{value|json}},
            "confidence": 1.0,
            "grammar_entry": {{grammar_entry|json}}
          }
        ]
      }
    }
    """)
    payload = response_template.render(value=value, grammar_entry=grammar_entry)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response

'''
def multiple_query_response(results):
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.0",
        "result": [
        {% for result in results %}
          {
            "value": {{result.value|json}},
            "confidence": 1.0,
            "grammar_entry": {{result.grammar_entry|json}}
          }{{"," if not loop.last}}
        {% endfor %}
        ]
      }
    }
     """)
    payload = response_template.render(results=results)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response
'''

def validator_response(is_valid):
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.0",
        "is_valid": {{is_valid|json}}
      }
    }
    """)
    payload = response_template.render(is_valid=is_valid)
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/dummy_query_response", methods=['POST'])
def dummy_query_response():
    response_template = environment.from_string("""
    {
      "status": "success",
      "data": {
        "version": "1.1",
        "result": [
          {
            "value": "dummy",
            "confidence": 1.0,
            "grammar_entry": null
          }
        ]
      }
    }
     """)
    payload = response_template.render()
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/action_success_response", methods=['POST'])
def action_success_response():
    response_template = environment.from_string("""
   {
     "status": "success",
     "data": {
       "version": "1.1"
     }
   }
   """)
    payload = response_template.render()
    response = app.response_class(
        response=payload,
        status=200,
        mimetype='application/json'
    )
    return response



@app.route("/call", methods=['POST'])
def call():
  payload = request.get_json()
  contact_name = payload["context"]["facts"]["contact_name"]["value"]
  contact_number = payload["context"]["facts"]["contact_number"]["value"]
  getting_number = CONTACT_LIST[contact_name][contact_number]
  print(payload)

  return action_success_response()

'''
    with open('call_john/contacts.json', "w") as json_file:
        json.dump(CONTACT_LIST, json_file)
'''

@app.route("/asking_for_phone_number", methods=['POST'])
def asking_for_phone_number():
  payload = request.get_json()
  contact_name = payload["context"]["facts"]["contact_name"]["value"]
  contact_number = payload["context"]["facts"]["contact_number"]["value"]
  getting_number = CONTACT_LIST[contact_name][contact_number]
  return query_response(value=getting_number, grammar_entry=None)
