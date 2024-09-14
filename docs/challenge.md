First of all we explore the data and subsequent analysis of the data. Several errors were found, like the use of deprecated functions or functions used in a wrong way. After running the notebook, the xgboost model with balance and feature selection was used. This model was implemented in model.py just like it was implemented on the exploration notebook. 

Then for the api implementation, the model is run before the api setup, the api responds to GET ("/"), GET ("/health"). For solicitating predictions a POST request must be made to "/predict" including flights features such as: 
{
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas", 
                    "TIPOVUELO": "N", 
                    "MES": 3
                },
                {
                    "OPERA": "Copa Air", 
                    "TIPOVUELO": "I", 
                    "MES": 4
                }
            ]
}

The api was deployed into GCP using a docker image. 

https://api-737530635174.southamerica-east1.run.app