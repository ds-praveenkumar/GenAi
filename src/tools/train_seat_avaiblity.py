#===============================================================================
#  File Name    : train_seat_status.py
#  Project Name : Project Name
#  Description  : 
#    Description of this file

#  Author       : Praveen Kumar
#  Created On   : 2025-07-23
#  Last Updated : 2025-07-23
#  Version      : v1.0.0

#  Language     : Python
#  File name    : train_seat_status.py
#  Dependencies : 
#    - Dependency 1
#    - Dependency 2

#  Inputs       : Expected inputs
#  Outputs      : Expected outputs
#  Usage        : 
#    Example usage

#  Notes        : 
#    - Notes or TODOs
#===============================================================================
import sys
sys.path.append('.')
import requests
from dotenv import load_dotenv
load_dotenv(".env")
import os 

class TrainSeatStatus:
    def __init__(self, train_number, train_date, class_type, quota, source_station, destination_station ): 
        self.api_key = os.getenv("RAPID_API")
        self.train_number = train_number
        self.date = train_date
        self.class_type = class_type
        self.quota = quota
        self.source_station = source_station
        self.destination_station = destination_station
        self.url = "https://irctc1.p.rapidapi.com/api/v2/checkSeatAvailability"
        
        
    def _get_header( self ):
        headers = {
                "x-rapidapi-key": self.api_key,
                "x-rapidapi-host": "irctc1.p.rapidapi.com"
            }
        return headers
    
    def _get_query_string( self ):
        querystring = { "classType":self.class_type,
                       "fromStationCode":self.source_station,
                       "quota":"GN",
                       "toStationCode": self.destination_station,
                       "trainNo":self.train_number,
                       "date":self.date}
        return querystring

    def get_seat_status( self ):
        headers = self._get_header()
        querystring = self._get_query_string()
        response = response = requests.get( self.url, 
                                           headers=headers, 
                                           params=querystring)
        return response
        
    def main( self ):
        response = self.get_seat_status()
        return response
    
if __name__ == "__main__":
    train_number = "12101"
    train_date = "2025-08-15"
    class_type = "3a"
    quota = "GN"
    source_station = "LTT"
    destination_station = "TATA"
    train_seat_status = TrainSeatStatus(train_number, train_date, class_type, quota, source_station, destination_station)
    response = train_seat_status.main()
    print(response.json())
    
        
    