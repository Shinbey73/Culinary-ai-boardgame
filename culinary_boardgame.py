"""
Description: This file has the code to run the culinary boardgame
             A fun and strategic board game, "You Can't Spell Culinary Without A & I" revolves around the goal of building the ultimate culinary empire through the acquisition of a wide variety of eateries.
"""

########IMPORT STATEMENTS#########

#add all your import statements here
import restaurant_small      #importing the files
import restaurant_medium
from restaurant_medium import csv_data as data, delimiter as delimiter, board_size as board_size
from restaurant_small import csv_data as data, delimiter as delimiter, board_size as board_size
from abc import ABC, abstractmethod
import random
##############TASK 1##############

def print_game_board(size, dictionary):
    """
    The function prints the square game board
    Parameter:
    Size: an integer value that tells us the number of rows and coloumns
    Dictionary: keys as positions of the board and values as a list of the symbols occupying the board
    No return
    """

    print(" _____" * size)  # prints the top line of the board
    for row_line in range(size):
        print("|     " * size + "|")  # to divide the columns
        print("|", end="")  # this is only for the second line of each box
        for column_line in range(size):
            key = row_line * size + column_line
            try:
                value = dictionary[key]
                if not value:
                    print("    ", end=" |")  # Print empty space for an empty position
                else:
                    if len(value) == 1:
                        print(f'  {value[0]} ', end=" |")
                    elif len(value) == 2:
                        print(f'{value[0]}', f'{value[1]}', end="  |")
                    else:
                        print(f'{value[0]}', f'{value[1]}', f'{value[2]}', end="|")
            except KeyError:
                print("", end=" |")  # Handle KeyError
        print()
        print("|_____" * size + "|")  # printing the last line of each box
    
##############TASK 2##############

def retrieve_restaurant_details(csv_data, delimiter,board_size):
    """
    Retrieve restaurant details based on given parameters.

    Parameters:
    - delimiter: A string representing the delimiter used in the CSV data.
    - csv_data: A list containing restaurant data in CSV format.
    - board_size: An integer representing the board size.

    Returns:
    - A dictionary of restaurant details based on the board size.
    """
    restaurant_dictionary = {}   #make an empty dictionary
    for row in csv_data:         #iterate each row of the csv_data
        if row == csv_data[0]:   #the first row is string of headers
            row = row.split(delimiter) #split the string using the delimiter
            indexBP = row.index("Board Position") #we find the index number of each header so that we can arrange the things in the dictionary accordingly
            indexT = row.index("Type")
            indexRN = row.index("Restaurant Name")
            indexP = row.index("Price")

    key = 0  # we set key as 0, the variable 'key', is the actual key of dictionary 
    row_index = 1  # Start from the second row

    while row_index < len(csv_data):
        restaurant_detail = csv_data[row_index].split(delimiter)  #We take each row and split the string

        if key % (board_size - 1) == 0 and key != 0 and key != (board_size * board_size - 1): #this is used for the key values that need to be left empty
            key += 1
        else:  #this is used otherwise
            key = key

        value = [str(restaurant_detail[indexRN]),str(restaurant_detail[indexT]),str(restaurant_detail[indexP])] #the variable "value" is a list which represents the actual value of the dictionary
        restaurant_dictionary[key] = value #We assign the value to their respective key in the dictionary
        key += 1  # We add one to the key, so that we can use the next one
        row_index += 1 #We add one to the row_index, so that we can move to the next row of the csv_data

    return restaurant_dictionary  #finally return the dictionary

###########TASK 3, 5, 7###########

class RestaurantManager:
    """ A blueprint for all managers that will fight to purchase the restaurants"""

    INITIAL_CAPITAL = 1000  # a class variable- money (Bitecoins) a manager has at the beginning of the game

    def __init__(self, name):
        """
        constructor method
        arguments:
            name: string name of manager
        instance variables:
            name: string name of manager
            symbol: the first capital letter of the name of manager
            bitecoins: an integer representing how much BiteCoins does manager have initially
            restaurant_managed:a list containing all restaurants managed by a manager
            manager_positions: list containing all board positions from the start to the current round of the game for the manager
        """
        self.name = name  # initiallizing the name
        self.symbol = name[0].upper()  # initiallizing the symbol as the capital letter
        self.bitecoins = RestaurantManager.INITIAL_CAPITAL  # initializing the bitecoins as class variable(=1000)
        self.restaurants_managed = []  # initializing it as an empty list
        self.manager_positions = []  # initializing it as an empty list

    def get_name(self):
        """
        returns the name of the manager
        """
        return self.name

    def get_symbol(self):
        """
        returns the upper case letter of the manager's name
        """
        return self.symbol

    def get_bitecoins(self):
        """
        returns the integer number of bitecoins the manager has
        """
        return self.bitecoins

    def get_restaurants_managed(self):
        """
        returns the list of restaurants managed by the manager
        """
        return self.restaurants_managed

    def get_manager_positions(self):
        """
        returns the list of board positions from start to the current round of game for the manager
        """
        return self.manager_positions

    def update_bitecoins(self, change):
        """
        adds the amount of gain or loss of bitecoins
        Arguments:
            change: an integer number (may be positive or negative)
        No return
        """
        self.bitecoins += change
        return self.bitecoins

    def update_position(self, BP):
        """
        keeps a track of the positions that the manager is managing
        Arguments:
            BP: an integer board position
        No return
        """
        self.manager_positions.append(BP)  # this adds the board position into the empty list

    def get_current_position(self):
        """
        simply returns the current position of the manager
        """
        return self.manager_positions[-1]  # this extracts the last element of the list, which is basically the current position

    def undo_position(self):
        """
        removes the current position of the manager from the manager_positions list
        returns the previous round's position
        """
        self.manager_positions.remove(self.manager_positions[-1])  # this removes the latest position from the list
        return self.manager_positions

    def update_restaurants_managed(self, Restaurant):
        """
        takes in a Restaurant instance and add it to the restaurants_managed list if it does not already exist.
        Arguments:
            the Restaurant instance
        no returns
        """
        if Restaurant not in self.restaurants_managed:  # if the instance already exists in the list, it will not add it again
            self.restaurants_managed.append(Restaurant)

    def buy_restaurant(self, restaurant_dictionary, board_position):
        """
        Attempts to buy a restaurant at the manager's appointed board position.

        Arguments:
            restaurant_dictionary: A dictionary containing restaurant information.
            board_position: An integer indicates the board position of the restaurant.

        Returns:
            A string indicating the purchase status or any errors encountered during the purchase process.
        """

        # Validation check if board position in the estaurant dictionary returned by Task 2's function retrieve_restaurant_details
        if board_position not in restaurant_dictionary:
            return "It is not possible to access the restaurant. Please enter a valid number"

        # retrieves the information related to a restaurant from the restaurant_dictionary based on the board_position provided.
        restaurant_info = restaurant_dictionary[board_position]

        # Check if it's a list of restaurant details
        if isinstance(restaurant_info, list):

            # unpack the values stored in the restaurant_info variable into three separate variables: restaurant_name, restaurant_type, and restaurant_price.
            restaurant_name, restaurant_type, restaurant_price = restaurant_info

            # create Restaurant Object called restaurant1 with specific attributes such as restaurant_name, restaurant_type, restaurant_price, and board_position.
            restaurant1 = Restaurant(restaurant_name, restaurant_type, restaurant_price, board_position)

            # Update the restaurant_dictionary with the newly created Restaurant object.
            restaurant_dictionary[board_position] = restaurant1

            # Check if the restaurant is available for purchase based on manager availability.
            if not restaurant1.has_manager_availability():
                return f"Sorry, Restaurant {restaurant_name} is no longer available."

            # Check if the manager has enough BiteCoins to afford the restaurant.
            elif self.get_bitecoins() < int(restaurant_price):
                return f"Sorry, insufficient BiteCoins. You cannot afford {restaurant_name}."

            # Perform purchase and update manager details
            restaurant1.add_new_comanager(self)
            amount_shares = restaurant1.get_managerial_share(self)
            self.update_bitecoins(-int(restaurant_price))
            self.update_restaurants_managed(restaurant1)

            # Determine manager's position based on shares
            if amount_shares == 100:
                position = "sole manager"
            elif amount_shares == 40:
                position = "the first manager"
            elif amount_shares == 70 or amount_shares == 60:
                position = "head manager"
            elif amount_shares == 30:
                position = "co-manager"

            # Update manager's position and return status
            self.update_position(position)
            return f"{self.name} becomes {position} of {restaurant_name}"
            return f"{self.name} has {self.get_bitecoins()} BiteCoins and manages {len(self.restaurants_managed)} restaurant(s)"

        # Handle purchase if the restaurant information is already a Restaurant object
        elif isinstance(restaurant_info, Restaurant):

            restaurant_name = restaurant_info.get_restaurant_name()
            restaurant_price = restaurant_info.get_restaurant_price()
            restaurant_type = restaurant_info.get_restaurant_type()

            # Check if the restaurant is available for purchase based on manager availability.
            if not restaurant_info.has_manager_availability():
                return f"Sorry, Restaurant {restaurant_name} is no longer available."

            # Check if the manager has enough BiteCoins to afford the restaurant.
            elif self.get_bitecoins() < int(restaurant_price):
                return f"Sorry, insufficient BiteCoins. You cannot afford {restaurant_name}."

            # Perform purchase and update manager details
            restaurant_info.add_new_comanager(self)
            amount_shares = restaurant_info.get_managerial_share(self)
            self.update_bitecoins(-restaurant_price)
            self.update_restaurants_managed(restaurant_info)

            # Determine manager's position based on shares
            if amount_shares == 70 or amount_shares == 60:
                position = "head-manager"
            elif amount_shares == 30:
                position = "co-manager"

            # Update manager's position and return status
            self.update_position(position)
            return f"{self.name} becomes {position} of {restaurant_name}"
            return f"{self.name} has {self.get_bitecoins()} BiteCoins and manages {len(self.restaurants_managed)} restaurant(s)"

        else:
            return "Restaurant information is not in the correct format."

    def display_restaurants_managed(self):
        """
        Displays the list of managed restaurants categorized by types and overall values.
        """
        # Check if there are no restaurants managed by the manager
        if not self.restaurants_managed:
            print("No restaurants managed.")

        # Initialize categories dictionary to categorize restaurants by type
        categories = {
            'DESSERTS & BEVERAGES': [],
            'FARM-TO-TABLE': [],
            'FAST FOOD': [],
            'FUSION CUISINE': []
        }

        # Initialize variables to track total restaurant and managerial share values
        total_restaurant_value = 0
        total_managerial_share_value = 0

        # Loop through managed restaurants
        for restaurant in self.restaurants_managed:
            # Categorize restaurants based on their type and append to respective categories
            if restaurant.get_restaurant_type().upper() in categories.keys():
                categories[restaurant.get_restaurant_type().upper()].append(restaurant)

            # Calculate and accumulate total restaurant and managerial share values
            total_restaurant_value += restaurant.get_restaurant_price()
            managerial_share_value = (restaurant.get_managerial_share(self) / 100) * restaurant.get_restaurant_price()
            total_managerial_share_value += (managerial_share_value)
            # Round the total managerial share value
            total_managerial_share_value = round(total_managerial_share_value)

        # Display managed restaurants categorized by type
        for key in categories.keys():
            if categories[key]:
                print(key)
                number = 1
                for value in categories[key]:
                    print(
                        f"{number}. {value.get_restaurant_name()} ({value.get_restaurant_price()} BiteCoins, {value.get_managerial_share(self)}%)")
                    number += 1
        # Display overall values of managed restaurants
        print("OVERALL")
        print(f"Restaurants worth {total_restaurant_value} BiteCoins")
        print(f"Managerial shares worth {total_managerial_share_value} BiteCoins")

    def lose_bitecoin(self, restaurant_dictionary):
        """
        Constructs a BiteCoin loss simulation for the management according to their present board standing.

        Arguments:
            restaurant_dictionary: A dictionary with information on restaurants displayed on the board.
        """
        # Get the current position of the manager on the board
        current_position = self.get_current_position()

        # Check if the current position is present in the restaurant dictionary
        if current_position in restaurant_dictionary:
            # Retrieve the restaurant information at the current position
            restaurant_info = restaurant_dictionary[current_position]

            # Check if the restaurant information is an instance of the Restaurant class
            if isinstance(restaurant_info, Restaurant):
                managers_list = []

                # Loop through the managers managing the restaurant and gather unique instances
                for managers in restaurant_info.get_managers_list():
                    if managers not in managers_list:
                        managers_list.append(managers)

                # Calculate the payment for losing the BiteCoins
                restaurant_price = restaurant_info.get_restaurant_price() / 2
                my_payment = 0

                # Calculate and distribute payments to the managers of the restaurant
                for manager in managers_list:
                    manager_share = restaurant_info.get_managerial_share(manager)
                    payment = manager_share / 100 * restaurant_price
                    # Adjust the payment if it's in fractional amounts
                    if payment % 1.0 == 0.5:
                        payment += 0.5
                    payment = round(payment)
                    # Update the BiteCoins for each manager and accumulate the total payment
                    manager.update_bitecoins(payment)
                    my_payment += payment

                # Deduct the total payment from the current manager's BiteCoins
                self.update_bitecoins(my_payment * -1)

    def check_winning_conditions(self, number_needed_restaurant=4, average_managerial_share_needed=0,
                                 number_of_restaurant_types_needed=1):
        """
        Verifies whether the management has fulfilled the winning requirements by using predetermined criteria.

        Parameters:
            number_needed_restaurant: Minimum number of restaurants needed to win.
            average_managerial_share_needed: Minimum average share required for the manager to win.
            number_of_restaurant_types_needed: Minimum number of different restaurant types required.

        Returns:
            False if the winning conditions are not met, but True otherwise.
        """
        # Get the number of restaurants managed by the manager
        number_of_restaurant_managed = len(self.get_restaurants_managed())
        # Lists to store unique restaurant types and to calculate total share
        restaurant_types = []
        total_share = 0

        # Check if there are no managed restaurants, return False
        if number_of_restaurant_managed == 0:
            return False

        # Calculate total share and gather unique restaurant types
        for restaurant in self.get_restaurants_managed():
            total_share += restaurant.get_managerial_share(self)

            if restaurant.get_restaurant_type() not in restaurant_types:
                restaurant_types.append(restaurant.get_restaurant_type())

        # Calculate average share, number of unique types, and check winning conditions
        average_share = round(total_share / number_of_restaurant_managed)
        number_of_types = len(restaurant_types)

        if (number_of_restaurant_managed >= number_needed_restaurant
                and average_share >= average_managerial_share_needed
                and number_of_types >= number_of_restaurant_types_needed):
            return True

        else:
            return False
    
    def get_next_positions(self, restaurant_details_dict):
        """
        This prints out the next possible positions that the user can choose for the manager
        Parameter:
        restaurant_details_dict: this is the dictionary that we get from task 2
        Return:
        the next valid positions that the manager can go to
        """
        # Get current manager position and board size
        current_position = self.get_current_position()
        column_size = int(len(restaurant_details_dict) ** 0.5)
        valid_next_positions=[]#an empty list 
        if Restaurant.has_sole_manager == True:
            next_positions= [current_position - (column_size - 2),current_position - (column_size+1), current_position - (column_size + 2),
            current_position - 1, current_position +1, current_position + (column_size - 2),current_position+(column_size+1), current_position + (column_size + 2)]

            for position in next_positions:
                if 0 <= position <= (column_size**2):
                    valid_next_positions.append(position)
            return valid_next_positions
        
        else:
            next_positions= [current_position - (column_size+1),current_position - 1, current_position +1,current_position +(column_size+1)]

            for position in next_positions:
                if 0 <= position <= (column_size**2):
                    valid_next_positions.append(position)
            return valid_next_positions

    def __str__(self):
        return "{} has {} BiteCoins and manages {} restaurant(s)".format(self.name, self.bitecoins,
                                                                         len(self.restaurants_managed))

    def __repr__(self):
        return self.__str__()

##############TASK 4##############

class Restaurant:
    """
    A blueprint for all the restaurants that are managed on the board
    """
    RESTAURANT_TYPES = ["Desserts & Beverages","Farm-to-Table","Fast Food","Fusion Cuisine"]

    def __init__(self,restaurant_name,restaurant_type,restaurant_price,board_position):
        """
        constructor method
        arguments:
            restaurant_name: string name of manager
            restaurant_type:string representing the type of the restaurant
            restaurant_price: integer representing the amount of BiteCoins needed to become a manager of the restaurant
            board_position:integer board position of the restaurant
        instance variables:
            restaurant_name: string name of manager
            restaurant_type:string representing the type of the restaurant
            restaurant_price: integer representing the amount of BiteCoins needed to become a manager of the restaurant
            board_position:integer board position of the restaurant
            managers_list: list containing all RestaurantManager objects representing the manager(s) managing the restaurant
        """
        self.restaurant_name = restaurant_name
        self.restaurant_type = restaurant_type
        self.restaurant_price = int(restaurant_price)
        self.board_position = int(board_position)
        self.managers_list = [] # Initialized as an empty list for RestaurantManager objects

    def get_restaurant_name(self):
        """
        returns the name of the restaurant
        """
        return self.restaurant_name
    
    def get_restaurant_type(self):
        """
        returns the type of the restaurant
        """
        return self.restaurant_type
    
    def get_restaurant_price(self):
        """
        returns the price of restaurant
        """
        return self.restaurant_price
    
    def get_board_position(self):
        """
        returns the board position of the restaurant
        """
        return self.board_position

    def get_managers_list(self):
        """
        returns a list of all RestaurantManager objects representing the manager(s) managing the restaurant
        """
        return self.managers_list

    def has_manager_availability(self):
        """
        checks if there is space for more shareholders in the restaurant
        returns a boolean value
        """
        if len(self.managers_list)< 3: #if the number of managers are less than 3, it  means there is still space
            return True
        else:
            return False
    
    def add_new_comanager(self,comanager):
        """
        adds in another manager to the list of managers
        Arguments:
            comanager: the new manager of the restaurant
        No return
        """
        self.managers_list.append(comanager)
    
    def has_sole_manager(self):
        """
        checks if the restaurant is completely owned by only one manager
        returns a boolean value
        """
        if len(self.managers_list)== 3 and self.managers_list[0] == self.managers_list[1] and self.managers_list[0] == self.managers_list[2]:
            return True  #the above statement checks if the three managers are the same
        else:
            return False
    
    def get_managerial_share(self, manager):
        """
        This function computes and provides the allotment of shares for a particular manager based on their presence in the list of managers.

        Parameters:
        The name of the manager for whom the share allocation is to be determined.

        Returns:
        The share allocation designated for the specified manager. If the manager's name is not in the list, it returns 0.

        Share Allocation Guidelines:
        When the manager is listed:
        - The first appearance of the manager receives 40 shares.
        - Successive occurrences of the same manager receive 30 shares each.
        - For additional occurrences beyond the first one, each subsequent appearance results in an extra 30 shares being allocated.
        """

        if manager in self.managers_list:
            count_manager = self.managers_list.count(manager)

            if manager == self.managers_list[0]:  # Assign 40 to the first occurrence, 30 to subsequent occurrences
                share = 40  
            else:
                share = 30

            if count_manager > 1:
                share += (count_manager - 1) * 30  # Add additional shares for multiple occurrences
                
            return share
    
        else:
            return 0

    def __str__(self):
        return Restaurant.get_restaurant_name(self)
    
    def __repr__(self):
        return self.__str__()

##############TASK 6##############

class DiagonalGrid(ABC):
    def __init__(self, board_position, details_dictionary):
        """
        Constructor for the DiagonalGrid class.

        Parameters:
        - board_position: integer representing the position of the grid on the board.
        - details_dictionary: dictionary containing details relevant to the game.
        """
        self.grid_name = ""  # Initialize the grid name as an empty string
        self.board_position = board_position  # Set the board position based on the parameter
        self.details_dictionary = details_dictionary  # Store the details dictionary for the grid
    
    @abstractmethod
    def receive_grid_effect(self, manager):
        """
        Abstract method to receive grid effect.

        Parameters:
        - manager: object representing the game manager.
        """
        pass

    def __str__(self):
        """ Returns the name of the grid. """
        return self.grid_name  
    
    def __repr__(self):
        """ Returns the string representation of the grid. """
        return self.__str__()

class StartGrid(DiagonalGrid):
    def __init__(self, board_position, details_dictionary):
        """
        Constructor for the StartGrid class.

        Parameters:
        - board_position: integer representing the position of the grid on the board.
        - details_dictionary: dictionary containing details relevant to the game.
        """
        super().__init__(board_position, details_dictionary)  # Call the constructor of the parent class with board position and details dictionary
        self.grid_name = "Start Grid"  # Set the grid name as "Start Grid" for the StartGrid instance
    
    def receive_grid_effect(self, manager):
        """
        Method to receive the grid effect for the start grid.

        Parameters:
        - manager: object representing the game manager.

        Returns:
        - A string representing the grid effect for the start grid.
        """
        manager.update_bitecoins(200)  # Increase the manager's bitecoins by 200
        return "GRID EFFECT: Collected 200 BiteCoins"  # Return a message indicating the collection of 200 BiteCoins as the grid effect


class ChanceGrid(DiagonalGrid):
    def __init__(self, board_position, details_dictionary):
        """
        Constructor for the ChanceGrid class.

        Parameters:
        - board_position: integer representing the position of the grid on the board.
        - details_dictionary: dictionary containing details relevant to the game.
        """
        super().__init__(board_position, details_dictionary)  # Call the parent class constructor with board position and details dictionary
        self.grid_name = "Chance Grid"  # Set the grid name as "Chance Grid"

    
    def receive_grid_effect(self, manager):
        """
        Method to receive the grid effect for the chance grid.

        Parameters:
        - manager: object representing the game manager.

        Returns:
        - A string representing the grid effect for the chance grid.
        """
        grid_effect = random.choice(["get_reward", "get_penalty", "get_randomly_transported"])  # Choose a random grid effect
        return getattr(self, grid_effect)(manager)  # Execute the chosen grid effect with the manager as an argument


    def get_reward(self, manager):
        """
        Method to provide a reward grid effect.

        Parameters:
        - manager: object representing the game manager.

        Returns:
        - A string representing the reward grid effect.
        """
        reward = 100  # Define the reward amount
        manager.update_bitecoins(reward)  # Update manager's BiteCoins with the reward
        return "GRID EFFECT: Collected 100 BiteCoins"  # Return the effect message after updating the BiteCoins

    
    def get_penalty(self, manager):
        """
        Method to apply a penalty grid effect.

        Parameters:
        - manager: object representing the game manager.

        Returns:
        - A string representing the penalty grid effect.
        """
        penalty = 50  # Define the penalty amount
        if penalty <= int(manager.get_bitecoins()):  # Check if manager has enough BiteCoins to incur the penalty
            manager.update_bitecoins(-penalty)  # Deduct the penalty from manager's BiteCoins
            return "GRID EFFECT: Lost 50 BiteCoins"  # Return the effect message for the penalty
        else:
            return "You don't have enough to lose"  # Return a message indicating insufficient BiteCoins for the penalty

    
    def get_randomly_transported(self, manager):
        """
        Method to apply a random transport grid effect.

        Parameters:
        - manager: object representing the game manager.

        Returns:
        - A string representing the random transport grid effect.
        """
        # Calculate a random position within the range of available positions
        max_position = len(self.details_dictionary) - 1  # Get the maximum position index in the dictionary
        new_position = random.randint(0, max_position)   # Generate a random number within that range for a new position
        manager.update_position(new_position)  # Update the manager's position to the newly generated position
                
        return "GRID EFFECT: {} moved to position {}".format(manager.get_name(), new_position)  # Return a message indicating the movement to the new position

####ADDITIONAL HELPER FUNCTIONS####

#add all your additional helper functions here

########MAIN GAME FUNCTION#########

def run():
    """
    Function to initialize and run the 'You Can't Spell Culinary Without A & I' board game.
    """
    print("""You Can't Spell Culinary Without A & I is a board game where the goal is
            to fight to build the best food empire by acquiring a diverse collection
            of food establishments.\n""")
    print("LET'S BEGIN\n")
    
    # User input to choose board size and manager names
    users_choice_size = int(input("Choose a board - restaurant_small [0] restaurant_medium [1] restaurant_large [2]:\n"))
    manager1_name = input("Enter Manager 1's name:\n")
    manager2_name = input("Enter Manager 2's name:\n")
    print()
    print("GAME STARTS\n")
    print()
    
    # Initializing managers and defining board size based on user choice
    manager1 = RestaurantManager(manager1_name)
    manager1_symbol = manager1.get_symbol()
    manager2 = RestaurantManager(manager2_name)
    manager2_symbol = manager2.get_symbol()
    
    # Assigning board size and data based on user choice
    if users_choice_size == 0:
        board_size = restaurant_small.board_size
        data = restaurant_small.csv_data
        delimiter = restaurant_small.delimiter
        restaurant_details_dict = retrieve_restaurant_details(data, delimiter,board_size)
        
    elif users_choice_size == 1:
        board_size = restaurant_medium.board_size
        data = restaurant_medium.csv_data
        delimiter = restaurant_medium.delimiter
        restaurant_details_dict = retrieve_restaurant_details(data, delimiter,board_size)
    else:
        print("Invalid board choice. Please select a valid option.")
        return
    
    # Game Loop
    current_manager = manager1  # Starting with Manager 1
    manager1.update_position(0)  # Set initial position for manager1
    manager2.update_position(0)  # Set initial position for manager2

    while True:
        print_game_board(board_size, restaurant_details_dict)  # Print the game board
        
        if current_manager == manager1:
            print(f"--------------- {manager1_name}'s Turn ---------------")
        else:
            print(f"--------------- {manager2_name}'s Turn ---------------")

        positions = current_manager.get_next_positions(restaurant_details_dict)
        print(f"Available positions: {positions}")


        # Check for winning conditions
        if manager1.check_winning_conditions():
            print(f"Congratulations! {manager1_name} wins!")
            break
        elif manager2.check_winning_conditions():
            print(f"Congratulations! {manager2_name} wins!")
            break
        # Switch to the other manager for the next turn
        current_manager = manager2 if current_manager == manager1 else manager1

    print("Game over. Thanks for playing!")

# Call the run() function to start the game
if __name__ == "__main__":
    run()
