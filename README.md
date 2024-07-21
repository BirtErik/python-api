﻿# Python API
- Python API used for economic operators with AWS4 Signature Authorization.
- Uses Flask framework. 
- For development virtaulenv was used.
## How to Run?
To run API you need to: 
- install flask and mysql-connector-python with pip.
- configure config.py for database configuration 
- with python command execute run.py file.

## Endpoints
API provides these endpoints:
- Login	[POST] /tpd/v1/login
- Create Economic Operator [POST]	/tpd/v1/eo
- Update Economic Operator [PUT] /tpd/v1/eo/{EO_ID}
- Delete Economic Operator [DELETE] /tpd/v1/eo/{EO_ID}
- Query Economic Operator	[GET] /tpd/v1/eolist
- Query Economic Operator details	[GET] /tpd/v1/eolist/{EO_ID}

Each enpoint requiers AWS Signature Authorization header.
