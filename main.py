import sys
import datetime

import SimulateAccount
from random import randbytes, randint
from datetime import date
import SimulateAccount
from logger import setup_logger
from mysql_conn import mysql_conn_class
from faker import Faker


faker = Faker()
statuses = ["low","moderate","high"]


app_logger = setup_logger('app_logger', './app.log')
DatabaseConn = mysql_conn_class(app_logger) 

def main(sys_args):   

    try: # to get args from command line
        account_id = sys_args[1]
        N = abs(int(sys_args[2]))

        date_delta = datetime.timedelta(days = N)
        date_delta = date.today() - date_delta

        simulation = SimulateAccount.SimulateTransactions( earner_status=sys_args[3], spender_status=sys_args[4], N=N )

        global_transaction_count = DatabaseConn.get_count_of_table("alinefinancial", "transaction") 

        CONSECUTIVE_DAYS = []
        for i in range(N):
            CONSECUTIVE_DAYS.append((lambda x: x + datetime.timedelta(days = i))(date_delta))
            
    except Exception as e:
        return print(e)
    if simulation.spender_status not in statuses and simulation.earner_status not in statuses:
        return print("Proper earning or spending statuses not specified...\nMust be low, moderate or high.")



    try: #to make sure vendors table is populated
        vendors =[faker.company() for x in range(5)]
        vendors_count = DatabaseConn.get_count_of_table("alinefinancial", "vendor")
        if vendors_count == 0:
            vendorslist = []
            for index, vendor in enumerate(vendors, start=vendors_count):
                vendorslist.append( (index+1,vendor) )       
            DatabaseConn.insert_vendors_into_database("alinefinancial", vendorslist)
            vendors_count = vendors_count[-1][0]
    except Exception as e:
        return print("Failed to insert into empty vendor table")
    

    try: #to simualte
    
        simulation_list = []
        for day in CONSECUTIVE_DAYS:
            
            random_vendor = randint(1, vendors_count)
            money_earned = simulation.money_earned
            money_spent = simulation.money_spent * -1

            if money_earned != 0:
                global_transaction_count = global_transaction_count + 1
                simulation_list.append( (global_transaction_count, 1, 6, randint(1,2), money_earned, day, faker.sentence()) )

                


            simulation.simulate_one_day()

        net_balance = round( sum(transaction[4] for transaction in simulation_list) , 2)
        account_transactions = [ (account_id, transaction[0]) for transaction in simulation_list ]
        current_balance = DatabaseConn.find_balance_by_id("alinefinancial", "account", account_id)[0]
    except Exception as e:
        return print(e)

    input(f"About to add transactions for account id of {account_id}. Net change to account: {net_balance}\nPress enter to proceed")

    try: #to get results into database
        DatabaseConn.insert_transactions_into_database("alinefinancial", simulation_list)
    except Exception as e:
        return print(f"Nice try...\n{e}")
    
    else:
        try:
            DatabaseConn.insert_transactions_into_database("alinefinancial", simulation_list)
            DatabaseConn.insert_account_transactions_into_database("alinefinancial", account_transactions)
        except Exception as e:
            return print(f"There was an issue adding Transactions to the databse beforehand \nStack trace: {e}")
        else:
            DatabaseConn.update_account_balance_in_database("alinefinancial", (current_balance + net_balance, account_id))
            print("Added everything, updated account")

if __name__ =="__main__":
    main(sys.argv)
