from flask import Flask ,jsonify

def success_response(data,message='Success',status_code=200):

    return jsonify({
      "Success":True,
      "message": message,
      "data" : data
    }),status_code