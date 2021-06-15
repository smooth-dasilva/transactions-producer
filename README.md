# Data Simulation
Python script to generate random but logically sound transactions over some days. 

Will generate transactions data, add correpsponding transactions to account-transaction joint table and alter balance to reflect new changes. 

Config with:
mysql_user = ""
mysql_pwd = ""
mysql_host = ""
mysql_port = int
mysql_db = ""

Run main example:
python -m main <account_id> <Number of Days> <Earner status> <Spending status>

