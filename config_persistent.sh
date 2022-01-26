#!/bin/bash

source .env

curl -X POST -H "Content-Type: application/json" -d '{
    "get_started": {
        "payload": "get_started"
    }
}' https://graph.facebook.com/v12.0/me/messenger_profile?access_token=$AMET_ACCESS_TOKEN
  
  


curl -X POST -H "Content-Type: application/json" -d '{ 
    "persistent_menu": [
        {
            "locale": "default",
            "composer_input_disabled": false,
            "call_to_actions": [
                {
                    "type": "postback",
                    "title": "📄 MENU PRINCIPAL",
                    "payload": "__MENU"
                },
                {
                    "type": "postback",
                    "title": "ℹ️ DECONNEXION ADMIN OU PART",
                    "payload": "__DECONNEXION"
                }
            ]
        }
    ]
}'"https://graph.facebook.com/v12.0/me/messenger_profile?access_token=$AMET_ACCESS_TOKEN"
  
  