# Author: Dhaval Patel. Codebasics YouTube Channel

import mysql.connector
global cnx

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="abc123",
    database="pizzamania_food_items"
)




# Function to call the MySQL stored procedure and insert an order item

# Function to fetch the order status from the order_tracking table]

def get_order_status(order_id):
    cursor = cnx.cursor()

    # Executing the SQL query to fetch the order status
    query = f"SELECT status FROM order_tracking WHERE order_id = {order_id}"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()



    # Returning the order status
    if result:
        return result[0]
    else:

        return None






def insert_order_item(order_id, food_name, quantity_pizza):
    try:
        # Fetch the price of the food item

        item_id = get_food_id(food_name)
        food_price = get_food_price(item_id)

        print(food_name, order_id, quantity_pizza,item_id, food_price)

        if food_price is None:
            print("Unable to insert order due to missing food price.")
            return

        # Calculate the total price
        total_price = quantity_pizza * food_price
        print(total_price)
        # Connect to the MySQL database


        cursor = cnx.cursor()

        # SQL query to insert data into the orders table
        insert_query = "INSERT INTO orders (order_id, item_id, quantity_pizza, total_price) VALUES (%s, %s, %s, %s);"

        # Execute the query
        cursor.execute(insert_query, (order_id, item_id, quantity_pizza, total_price))

        # Commit the transaction
        cnx.commit()

        cursor.close()



        print(f"Order {order_id} inserted successfully with total price {total_price}!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        cnx.rollback()








def total_order(order_id):
    try:
        cursor = cnx.cursor()
        # SQL query to fetch the total price for all items with the given order_id
        query = "SELECT quantity_pizza, total_price FROM orders WHERE order_id = %s"
        cursor.execute(query, (order_id,))
        result = cursor.fetchall()  # Fetch all the results


        if result:
            # Summing up the total price for all items
            total_price = sum(item[1] for item in result)  # item[1] is the total_price of each item
            cursor.close()
            return total_price

        else:
            cursor.close()
            return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        cnx.rollback()
        return None




def get_food_price(item_id):
    """
    Fetch the price of the food item from the `food` table using the item_id.
    """
    try:
        cursor = cnx.cursor()
        # SQL query to fetch the price of the food item
        fetch_query = "SELECT price FROM foods WHERE id = %s;"

        # Execute the query
        cursor.execute(fetch_query, (item_id,))

        # Fetch the result
        result = cursor.fetchone()

        if result:
            cursor.close()
            return result[0]  # Return the price
        else:
            cursor.close()
            return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        cnx.rollback()
        return None



def get_item_id(order_id: int):
    """
    Fetch the price of the food item from the `food` table using the item_id.
    """
    try:


        cursor = cnx.cursor()

        # SQL query to fetch the price of the food item
        fetch_query = "SELECT id FROM foods WHERE order_id = %s;"

        # Execute the query
        cursor.execute(fetch_query, (order_id,))

        # Fetch the result
        result = cursor.fetchone()

        if result:
            cursor.close()
            return result[0]  # Return the price
        else:
            print(f"No item found with item_id {order_id}.")
            cursor.close()
            return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        cnx.rollback()
        return None

def get_food_id(food_items):
    """
    Fetch the price of the food item from the `food` table using the item_id.
    """
    try:


        cursor = cnx.cursor()

        # SQL query to fetch the price of the food item
        fetch_query = "SELECT id FROM foods WHERE name = %s;"

        # Execute the query
        cursor.execute(fetch_query, (food_items,))

        # Fetch the result
        result = cursor.fetchone()

        if result:
            cursor.close()
            return result[0]  # Return the price
        else:
            print(f"No item found with item_id {food_items}.")
            cursor.close()
            return None


    except mysql.connector.Error as err:
        print(f"Error: {err}")
        cnx.rollback()
        return None



# # Function to insert a record into the order_tracking table
def insert_order_tracking(order_id, status):
    cursor = cnx.cursor()

    # Inserting the record into the order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))

    # Committing the changes
    cnx.commit()

    # Closing the cursor
    cursor.close()


# def get_total_order_price(number: int):
#     cursor = cnx.cursor()
#
#     # Executing the SQL query to get the total order price
#     query = f"SELECT get_total_order_price({number})"
#     cursor.execute(query)
#
#     # Fetching the result
#     result = cursor.fetchone()[0]
#
#     # Closing the cursor
#
#
#     return result

# Function to get the next available order_id
def get_next_order_id():
    cursor = cnx.cursor()

    # Executing the SQL query to get the next available order_id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]



    # Returning the next available order_id
    if result is None:
        return 1
    else:
        return result + 1


# if __name__ == "__main__":
#     # print(get_total_order_price(56))
#     # insert_order_item('Samosa', 3, 99)
#     # insert_order_item('Pav Bhaji', 1, 99)
#     # insert_order_tracking(99, "in progress")
#     print(get_next_order_id())
