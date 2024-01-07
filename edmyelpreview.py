import pymssql
import random
import string
from prettytable import PrettyTable

server1 = input("Enter your server name: ");
database_name = input("Enter database name: ");
username1 = input("Enter your SQL server authentication username: ");
password1 = input("Enter your SQL server authentication password: ");

conn = pymssql.connect(host=server1, database=database_name, user=username1, password=password1);

def valid_uid(id): #checks user id
    query = f"SELECT COUNT(*) FROM user_yelp WHERE user_id = '{id}'";
    cursor = conn.cursor();
    cursor.execute(query);
    user_count = cursor.fetchone()[0];
    cursor.close();
    if (user_count >= 1):
        return True;
    else:
        return False;

def valid_bid(id): #checks business id
    query = f"SELECT COUNT(*) FROM business WHERE business_id = '{id}'";
    cursor = conn.cursor();
    cursor.execute(query);
    count = cursor.fetchone()[0];
    cursor.close();
    if (count >= 1):
        return True;
    else:
        return False;

def login():
    flag = False
    while flag == False:
        name = input('Enter a user ID: ');
        flag = valid_uid(name);
        if (flag == False):
            print('invalid user ID');
    return name;

def search_bus():
    cursor = conn.cursor();
    # Collect user input
    print('You may leave any of the answers blank.');
    stars = input('Minimum number of stars: ');
    city = input('City: ').lower();
    name = input('Name contains: ').lower();
    order = input('Type 0 to order by name, 1 to order by city, and 2 to order by stars: ');

    # Construct the base SQL query
    # the 1=1 is a placeholder to add the next conditions
    query = "SELECT * FROM business WHERE 1=1";

    # Add conditions based on user input
    if stars:
        query += f" AND stars >= {stars}";
    if city:
        query += f" AND LOWER(city) = '{city}'";
    if name:
        query += f" AND LOWER(name) LIKE '%{name}%'";

    # Add order by clause based on user input
    if order == '0':
        query += " ORDER BY name";
    elif order == '1':
        query += " ORDER BY city";
    elif order == '2':
        query += " ORDER BY stars";
    else:
        print("Invalid order type. Defaulting to order by name.");

    # Execute the query
    cursor.execute(query)

    # Fetch and display the results
    results = cursor.fetchall()

    if results:
        print("\nResults:");
        table = PrettyTable();
        table.field_names = ["business id", "business name", "address", "city", "postal code", "stars", "review count"];
        for row in results:
            table.add_row(row);
        print(table);
    else:
        print("No results");
    cursor.close();
    print("\n");

def search_user():
    cursor = conn.cursor();
    #gather information from user
    print('you may leave any of the answers blank');
    subname = input('name contains: ').lower();
    reviews = input('minimum review count: ');
    avg_stars = input('minimum average stars: ');

    query = "SELECT * FROM user_yelp WHERE 1=1";

    #add stuff specified by user
    if subname:
        query += f" AND LOWER(name) LIKE '%{subname}%'";
    if avg_stars:
        query += f" AND average_stars >= '{avg_stars}'";
    if reviews:
        query += f" AND review_count >= '{reviews}'";
    query += "ORDER BY name"; #order by name like the instruction stated

    cursor.execute(query);
    results = cursor.fetchall();
    if results:
        print("\nResults:");
        table = PrettyTable();
        table.field_names = ["user id", "name", "review count", "yelping since", "useful", "funny", "cool", "fans", "average stars"];
        for row in results:
            table.add_row(row);
        print(table);
    else:
        print("No results");
    cursor.close();        
    print("\n");

def friendship_exists(user, friend):
    cursor = conn.cursor();
    query = f"SELECT COUNT (*) FROM friendship WHERE user_id = '{user}' AND friend = '{friend}'";
    cursor.execute(query);
    friend_count  = cursor.fetchone()[0];
    cursor.close();
    if (friend_count >= 1):
        return True;
    else:
        return False;

def make_friend(logged_in_user_id):
    friend = input('Enter a user_id to befriend: ');
    if (friend == logged_in_user_id):
        print("You cannot be your own friend");
        return;
    if (valid_uid(friend) == False):
        print("Friend's ID is not valid");
        return;
    if (friendship_exists(logged_in_user_id, friend)):
        print("Friendship already exists");
        return;
    cursor = conn.cursor();
    query = f"INSERT INTO friendship VALUES ('{logged_in_user_id}', '{friend}')";
    cursor.execute(query);
    conn.commit();
    cursor.close();
    print("");
    print("Friend added successfully");
    print("");

def generate_random_string(length): #helper function for creating new review IDs
    characters = string.ascii_letters + string.digits 
    random_string = ''.join(random.choice(characters) for i in range(length))
    #check if random_string already exists in the database
    query = f"SELECT COUNT (*) FROM review WHERE review_id = '{random_string}'";
    cursor = conn.cursor();
    cursor.execute(query);
    count = cursor.fetchone()[0];
    if (count >= 1): #create a new string if id already exists
        return generate_random_string(length);
    else:
        return random_string

def review_bus(logged_in_user_id):
    bus_id = input('Enter business id: ');
    if not valid_bid(bus_id):
        print("Invalid business ID");
        return;
    stars = input('Enter your rating from 1 to 5: ');
    try:
        int_stars = int(stars);
    except ValueError:
        print("Rating must be an integer");
        return;
    if (int_stars < 1 or int_stars > 5):
        print("Rating must be between 1 and 5");
        return;
    cursor = conn.cursor();
    new_r_id = generate_random_string(22);
    query = f"INSERT INTO review (review_id, user_id, business_id, stars, date) VALUES ('{new_r_id}', '{logged_in_user_id}', '{bus_id}', {int_stars}, GETDATE())";
    cursor.execute(query);
    conn.commit();
    cursor.close();
    print("");
    print("Review added succesfully");
    print("");

def choices():
    print("Type the associated number to perform the action or type 'exit' to quit");
    print("0: Search business");
    print("1: Search users");
    print("2: Make friend");
    print("3: Review business");
    ret = input('Response: ');
    if (ret == "exit"):
        return None;
    else:
        return ret;

id = login();
action = choices();
while (action != None):
    if (action == "0"):
        search_bus();
    elif (action == "1"):
        search_user();
    elif (action == "2"):
        make_friend(id);
    elif (action =="3"):
        review_bus(id);
    else:
        print("invalid response");
    action = choices();