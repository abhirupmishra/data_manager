"""
Database engine connections that the application would connect to. 
AUTO-GENERATED, please run: 

from data_manager import db_models 
 get_db_engines(<options>) 
to generate connection strings and orm objects """
# pylint: skip-file 

import os 
from sqlalchemy import create_engine 

quant_database_engine = create_engine('postgres://' + os.environ['quant_user'] + ':' + os.environ['quant_password'] + '@' + os.environ['quant_host'] + ':5432/' + os.environ['quant_database'])

