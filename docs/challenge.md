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

##The stress test results:


### Requests Summary

| Name         | # reqs | # fails | Avg  | Min | Max  | Median | req/s | failures/s |
|--------------|--------|---------|------|-----|------|--------|-------|------------|
| POST /predict| 3343   | 0 (0.00%)| 527  | 137 | 9624 | 420    | 56.40 | 0.00       |
| **Aggregated**| 3343   | 0 (0.00%)| 527  | 137 | 9624 | 420    | 56.40 | 0.00       |

### Response Time Percentiles (Approximated)

| Type | Name         | 50%  | 66%  | 75%  | 80%  | 90%  | 95%  | 98%  | 99%  | 99.9% | 99.99% | 100% | # reqs |
|------|--------------|------|------|------|------|------|------|------|------|-------|--------|------|--------|
| POST | /predict     | 420  | 560  | 660  | 690  | 880  | 1100 | 1200 | 1700 | 9400  | 9600   | 9600 | 3343   |
| None | Aggregated   | 420  | 560  | 660  | 690  | 880  | 1100 | 1200 | 1700 | 9400  | 9600   | 9600 | 3343   |
