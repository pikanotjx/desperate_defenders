# Kwok Jing Xuan (S10243296B) - CICTP02 / P13
# Programming 1 - Assignment
# July - August 2022

import random
import math
import os.path
import os
from select import select

# =================================================================================
#                                   GAME VARIABLES
# =================================================================================

game_vars = {
    "turn": 1,  # Current Turn
    "monster_kill_target": 20,  # Number of kills needed to win
    "monsters_killed": 0,  # Number of monsters killed so far
    "num_monsters": 0,  # Number of monsters in the field
    "gold": 10,  # Gold for purchasing units
    "threat": 0,  # Current threat metre level
    "max_threat": 5,  # Length of threat metre
    "danger_level": 1,  # Rate at which threat increases
}

field = [[None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None]]  # Playing field

rows_list = ["A", "B", "C", "D", "E"]  # List of rows on the field

defenders_dict = {"ARCHR": {"name": "Archer",  # Name to print when showing user
                            "maxHP": 5,  # Max HP
                            "min_damage": 1,  # Min damage
                            "max_damage": 4,  # Max damage
                            "price": 5,  # Price
                            "sell_price": 2,
                            "upgrade_price": 8
                            },

                  "WALL": {"name": "Wall",
                           "maxHP": 20,
                           "min_damage": 0,
                           "max_damage": 0,
                           "price": 3,
                           "sell_price": 0,
                           "upgrade_price": 6
                           },

                  "CANON": {"name": "Cannon",
                            "maxHP": 8,
                            "min_damage": 3,
                            "max_damage": 5,
                            "price": 7,
                            "sell_price": 3,
                            "upgrade_price": 10
                            },

                  "MINE": {"name": "Mine",
                           "maxHP": "",
                           "damage": 10,
                           "price": 8,
                           "sell_price": 4,
                           "upgrade_price": 13
                           },

                  "FARMR": {"name": "Farmer",
                            "maxHP": 3,
                            "min_damage": 0,
                            "max_damage": 0,
                            "price": 6,
                            "gold_given": 2,
                            "sell_price": 0,
                            "upgrade_price": 9
                            },

                  "HEAL": {"name": "Heal",
                           "maxHP": 5,
                           "mxn_damage": 0,
                           "max_damage": 0,
                           "price": 5}
                  }

defenders_list = list(defenders_dict.keys())

monsters_dict = {"ZOMBI": {"name": "Zombie",  # Name to print when showing user
                           "maxHP": 15,  # Max HP
                           "min_damage": 3,  # Minimum damage
                           "max_damage": 6,  # Maximum damage
                           "moves": 1,  # Number of moves each turn
                           "reward": 2  # Reward when killed
                           },

                 "WWOLF": {"name": "Werewolf",
                           "maxHP": 10,
                           "min_damage": 1,
                           "max_damage": 4,
                           "moves": 2,
                           "reward": 3
                           },

                 "SKELE": {"name": "Skeleton",
                           "maxHP": 10,
                           "min_damage": 1,
                           "max_damage": 3,
                           "moves": 1,
                           "reward": 1
                           },

                 "PEKKA": {"name": "Pekka",
                           "maxHP": 3,
                           "min_damage": 10,
                           "max_damage": 12,
                           "moves": 3,
                           "reward": 2
                           }
                 }

monsters_list = list(monsters_dict.keys())


# ========================================================================================================
#                                         GAME FUNCTIONS
# ========================================================================================================
# Prints the given list of options
def print_options(arguments):
    print("")
    print(*arguments, sep="\n")

    
# Prompts user to enter Y or N, and return the corresponding boolean value
def confirmation():
    while True:
        confirm = input("Enter Yes(Y) or No(N): ")
        if confirm.capitalize() == "Y":
            return True
        elif confirm.capitalize() == "N":
            return False
        else:
            print("Please enter Yes(Y) or No(N)!")


# Prompts user to select from a range of numbers
def select_option(num_choices):
    while True:
        try:
            choice = int(input(f"Enter number choice 1 - {num_choices}: "))
            assert 1 <= choice <= num_choices
            return choice

        except (AssertionError, ValueError):
            print(f"\nInvalid input! Please enter number choice 1 - {num_choices}!\n")


# Check if the placement that user entered is valid. Returns row and column if valid, otherwise returns False
def placement_valid(placement):
    try:
        assert len(placement) == 2
        row = rows_list.index(placement[0].capitalize())
        column = int(placement[1]) - 1
        assert 0 <= column <= 3
        return [row, column]

    except (AssertionError, ValueError):
        print("Invalid input! Enter the row followed by the column 1 - 4 (E.g. A3)\n")
        return False
    

# Prints start menu and gets start option from user
def start_option():
    print("\n\nDesperate Defenders")
    print("===============================================")
    print("Defend the city from undead monsters!\n")
    print_options(["1. Start new game",
                   "2. Saved games",
                   "3. Game instructions",
                   "4. Quit"])

    return select_option(4)


# Resets game_vars and field
def new_game():
    game_vars["turn"] = 1
    game_vars["monster_kill_target"] = 20
    game_vars["monsters_killed"] = 0
    game_vars["num_monsters"] = 0
    game_vars["gold"] = 10
    game_vars["threat"] = 0
    game_vars["danger_level"] = 1

    field = [[None, None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None, None],
             [None, None, None, None, None, None, None, None, None]]


# Get name to save game file as
def save_game():
    try:
        name = input("Enter the name you would like to save the game file as (x to cancel) ")
        assert name.isalnum()
        return False if name.capitalize() == "X" else [True, name]
    
    except AssertionError:
        print("Please only enter alphabets and numbers for your file name.\n")
        return [False]


# Write game variables, field, defenders and monsters information to txt file. 
def save_to_file(file):
    with open(file, "w") as data:
        for i in game_vars:
            data.write(str(game_vars[i]))
            data.write("\n")

        for row in range(len(field)):
            for column in range(len(field[row])):
                if field[row][column] is None:
                    data.write("Empty\n")
                else:
                    for unit_information in range(len(field[row][column])):
                        data.writelines([str(field[row][column][unit_information]), "\n"])

        for monster in monsters_dict:
            for info in monsters_dict[monster]:
                data.write(str(monsters_dict[monster][info]))
                data.write("\n")

        for defender in defenders_dict:
            for info in defenders_dict[defender]:
                data.write(str(defenders_dict[defender][info]))
                data.write("\n")

    print(f"The game has been saved as {name}.txt \n")
    print_options(["1. Return to game", "2. Quit game", "3. Return to start menu"])

    option = select_option(3)
    if option == 2:
        quit_game(True)

    elif option == 3:
        global play_game, start_game
        play_game = False
        start_game = True
        
    return True


# Get path of savedgames folder. Get game list
def access_saved_games():
    current_path = os.path.dirname(os.path.realpath('__file__'))
    saved = os.listdir(current_path + "\\savedgames")

    print_options(["1. Open saved game", "2. View list of saved games", "3. Return to start menu"])
    option = select_option(3)

    if option == 1:
        return [False, current_path]

    elif option == 2:
        return print_game_list(saved, current_path)

    else:
        return [False, None]


# Prints game list
def print_game_list(saved, current_path):
    print("\nList of saved games: ")
    for count, game in enumerate(saved, start=1):
        print(f"{count}. {game[:-4]}")
    print_options(["1. Open saved game", "2. Return to start menu"])
    option = select_option(2)
    return [False, current_path] if option == 1 else [False, None]


# Load game based on name given
def load_game(current_path):
    filename = input("Enter saved game file (x to cancel) ")

    if filename.capitalize() == "X":
        access_saved_games()

    relative_path = "savedgames\\" + filename + ".txt"
    file = os.path.join(current_path, relative_path)

    global game_vars, field, monsters_dict, defenders_dict

    try:
        data = open(file, "r")

    except FileNotFoundError:
        print("No file with that name found! Please check your spelling!")
        load_game(current_path)
        return

    for variable in game_vars:
        information = int(data.readline().strip())
        game_vars[variable] = information

    for row in range(len(field)):
        for column in range(len(field[row])):
            field_item = data.readline().strip()
            field[row][column] = None if field_item == "Empty" else [field_item, int(data.readline().strip()), int(data.readline().strip())]

    for monster in monsters_dict:
        for info in monsters_dict[monster]:
            monster_data = data.readline().strip()
            monsters_dict[monster][info] = int(monster_data) if monster_data.isdigit() else monster_data

    for defender in defenders_dict:
        for info in defenders_dict[defender]:
            defender_data = data.readline().strip()
            defenders_dict[defender][info] = int(defender_data) if defender_data.isdigit() else defender_data


# Quits game
def quit_game(played):

    if played:
        print("Are you sure you want to quit?")

        if confirmation():
            print("Thank you for playing! Goodbye!")
            exit()

        else:
            print("Returning to combat menu\n\n")
            return

    else:
        print("Quitting game...")
        exit()


# Upgrades given unit, returns gold if not enough gold
def upgrade_unit(unit):
    if game_vars["gold"] <= defenders_dict[unit]["upgrade_price"]:
        print("You do not have enough gold to upgrade this unit! ")
        print(f"Required: {defenders_dict[unit]['upgrade_price']} gold")
        print(f"Available: {game_vars['gold']} gold")
        return False

    elif unit in ["ARCHR", "CANON"]:
        defenders_dict[unit]["maxHP"] += 1
        defenders_dict[unit]["min_damage"] += 1
        defenders_dict[unit]["max_damage"] += 1

    elif unit == "WALL":
        defenders_dict["WALL"]["maxHP"] += 5

    elif unit == "MINE":
        defenders_dict["MINE"]["min_damage"] += 1
        defenders_dict["MINE"]["max_damage"] += 1

    elif unit == "FARMR":
        defenders_dict["FARMR"]["gold_given"] += 1

    game_vars["gold"] -= defenders_dict[unit]["upgrade_price"]
    defenders_dict[unit]["upgrade_price"] += 2
    print(f"Upgrade of {defenders_dict[unit]['name']} successful! \n")
    return True


# Prints combat menu and gets option
def combat_menu():
    draw_field()

    print("Turn  {:<4}  Threat = [{:<5}]     Danger Level  {:<}".format(game_vars["turn"], game_vars["threat"] * "-", game_vars["danger_level"]))
    print("Gold = {:<3}  Monsters killed = {}/{}".format(game_vars["gold"], game_vars["monsters_killed"], game_vars["monster_kill_target"]))

    print_options(["1. Open Shop        2. Sell Defender",
                   "3. Upgrade Unit     4. End Turn",
                   "5. Save Game        6. Quit Game"])

    return select_option(6)


# Sell defender unit
def sell_unit():
    while True:
        placement = input("\nPlease enter the placement of the unit that you wish to sell (X to cancel) ")
        if placement.capitalize() == "X":
            return

        elif placement_valid(placement) is not False:
            [row, column] = placement_valid(placement)

            if field[row][column] is None:
                print("There is nothing there to sell! Please select another location! ")
        
            else:
                unit = field[row][column][0]
                if unit in monsters_dict:
                    print("You cannot sell a monster! Ensure that the correct placement has been entered! ")

                else:
                    print(f"Would you like to sell the {defenders_dict[unit]['name']} in lane {rows_list[row]} for {defenders_dict[unit]['sell_price']} gold?")
                    if confirmation():
                        field[row][column] = None
                        game_vars["gold"] += defenders_dict[unit]["sell_price"]
                        print(f"{defenders_dict[unit]['name']} in lane {rows_list[row]} has been sold for {defenders_dict[unit]['sell_price']}! ")

                    else:
                        print("Cancelled! Returning to combat menu! ")
                    return


# Prints game instructins from file gameplay.txt
def game_instructions():
    current_path = os.path.dirname(os.path.realpath("__file__"))
    try:
        datafile = open(current_path + "\\gameplay.txt", "r")
        print("")
        for line in datafile:
            line = line.strip()
            print(line)

    except FileNotFoundError:
        print("Error retrieving the game instructions, please ensure that there is a file titled gameplay.txt in the same directory as this program and try again. \n")


# Prints playing field
def draw_field():
    # column headers for first 3 columns
    print("    {:<6}{:<6}{:<6}{:<6}".format(1, 2, 3, 4))

    for row in range(len(rows_list)):
        print(f' +{"-----+" * len(field[0])}')
        # Print row header
        print(f"{rows_list[row]}|", end="")
        # For number of columns
        for column in range(len(field[row])):
            # If there is nothing in the field
            if field[row][column] is None:
                print("     |", end="")

            else:
                print("{:^5}|".format(field[row][column][0]), end="")
        # Print second row of the same field
        print("\n |", end="")
        # For number of columns
        for column in range(len(field[row])):
            # If there is nothing in the field
            if field[row][column] is None or field[row][column][0] == "MINE":
                print("     |", end="")

            else:
                print("{:>2}/{:<2}|".format(field[row][column][1], field[row][column][2]), end="")

        # Prints new line after end of each line
        print("")
    # Prints the final border
    print(f' +{"-----+" * len(field[0])}')


# Heals defenders in range selected
def heal(row, column):
    heal_count = 0
    for healing_row in range(row - 1, row + 2):
        for healing_column in range(column - 1, column + 2):
            if field[healing_row][healing_column] is not None and field[healing_row][healing_column][0] in defenders_dict:
                defender_healed = field[healing_row][healing_column][0]
                heal_amount = defenders_dict["HEAL"]["maxHP"]
                field[healing_row][healing_column][1] += heal_amount
                print(f"*** {defenders_dict[defender_healed]['name']} in lane {rows_list[row]} has been healed by {heal_amount}.")
                heal_count += 1
    
    if heal_count > 0:
        game_vars["gold"] -= defenders_dict["HEAL"]["price"]
        print(f"Heal has successfully been used for {defenders_dict['HEAL']['price']} gold. {heal_count} defenders have been healed. ")
        return True

    else: 
        print("There are no defenders in the vicinity to heal! No gold has been spent. ")
        return False


# Spawn a new monster
def spawn_monster():
    row = random.randint(0, 4)
    while field[row][-1] is not None:
        row = random.randint(0, 4)

    monster = random.choice(monsters_list)

    field[row][len(field[0]) - 1] = [monster, monsters_dict[monster]["maxHP"], monsters_dict[monster]["maxHP"]]


# Place defender that was purchased
def place_defender(unit, row, column):
    if unit == "HEAL":
        return heal(row, column)

    elif field[row][column] is None:
        if unit != "MINE":
            field[row][column] = [unit, defenders_dict[unit]["maxHP"], defenders_dict[unit]["maxHP"]]
        else:
            field[row][column] = [unit, ]
        game_vars["gold"] -= defenders_dict[unit]["price"]
        print(f'\nPurchase of {unit} is successful! {defenders_dict[unit]["price"]} gold spent')
        return True

    else:
        if field[row][column][0] in defenders_list:
            print(f"There is a {defenders_dict[field[row][column][0]]['name']} there! Please select another location. \n")

        else:
            print(f"There is a {monsters_dict[field[row][column][0]]['name']} there! Please select another location. \n")

        return False


# Win game
def win():
    print_options(["You have protected the city! You win", "1. Start new game", "2. Quit game"])
    option = select_option(2)
    new_game() if option == 1 else quit_game(True)


# Lose game
def lose(unit):
    global play_game 
    play_game = False
    print_options([f"\nA {unit} has reached the city! All is lost",
                   "You have lost the game :(",
                   "1. Start Menu",
                   "2. Quit game"])

    if select_option(2) == 1:
        global start_game
        start_game = True

    else:
        quit_game(True)


# When a defender attacks
def defender_attack(defender, row, column):
    for current_column in range(column + 1, len(field[0])):
        if field[row][current_column] is not None and field[row][current_column][0] in monsters_dict:
            monster = field[row][current_column][0]
            damage = random.randint(defenders_dict[defender]["min_damage"], defenders_dict[defender]["max_damage"])
            if defender == "ARCHR" and monster == "SKELE":
                damage = math.ceil(damage / 2)
            field[row][current_column][1] -= damage
            print(f"*** {defenders_dict[defender]['name']} in lane {rows_list[row]} dealt {damage} damage to {monsters_dict[monster]['name']}")
            if field[row][current_column][1] <= 0:
                monster_killed(defender, monster, row, current_column)

            elif defender == "CANON" and random.choice([True, False]) == True and column + 1 < len(field[0]) and field[row][current_column + 1] is None:
                field[row][current_column + 1], field[row][current_column] = field[row][current_column], None
                print(f"*** Canon in lane {rows_list[row]} has knocked back the {monsters_dict[monster]['name']}.")
                
            return


# When a defender is killed
def defender_killed(defender, monster, row, column):
    field[row][column] = None
    print(f"*** {defenders_dict[defender]['name']} in lane {rows_list[row]} has been killed by {monsters_dict[monster]['name']}.")


# When a monster is killed
def monster_killed(defender, monster, row, column):
    field[row][column] = None
    print(f"*** {monsters_dict[monster]['name']} in lane {rows_list[row]} has been killed by {defenders_dict[defender]['name']}.")
    print(f"*** You gained {monsters_dict[monster]['reward']} gold as a reward.")
    game_vars["gold"] += monsters_dict[monster]["reward"]
    game_vars["threat"] += monsters_dict[monster]["reward"]
    game_vars["monsters_killed"] += 1
    if game_vars["monsters_killed"] >= game_vars["monster_kill_target"]:
        win()


# When a monster steps on a mine
def mine_activated(monster, row, column):
    print(f"*** {monsters_dict[monster]['name']} in lane {rows_list[row]} has stepped on a Mine!")
    monster_killed("MINE", monster, row, column)

    for row_damaged in range(row - 1, row + 2):
        for column_damaged in range(column - 1, column + 2):
            if field[row_damaged][column_damaged] is not None and field[row_damaged][column_damaged][0] in monsters_dict:
                monster_damaged = field[row_damaged][column_damaged][0]
                field[row_damaged][column_damaged][1] -= defenders_dict["MINE"]["damage"]
                print(f"*** Mine dealt {defenders_dict['MINE']['damage']} damage to {monsters_dict[monster_damaged]['name']} in lane {rows_list[row]}.")
                if field[row_damaged][column_damaged][1] <= 0:
                    monster_killed("MINE", monster, row_damaged, column)


# When monster advances
def monster_advance(monster, row, column):
    moves = monsters_dict[monster]["moves"]

    while moves > 0:
        if column == 0:
            lose(monster)

        elif field[row][column - 1] is None:
            print(f"*** {monsters_dict[monster]['name']} in lane {rows_list[row]} advances!")
            field[row][column - 1], field[row][column] = field[row][column], None
            moves -= 1
            column -= 1

        else:
            obstacle = field[row][column - 1][0]

            if obstacle in monsters_dict:
                print(f"*** {monsters_dict[monster]['name']} in lane {rows_list[row]} was blocked from advancing by the {monsters_dict[obstacle]['name']}")
                moves = 0

            elif obstacle == "MINE":
                mine_activated(monster, row, column - 1)
                moves = 0

            elif obstacle in defenders_dict:
                damage = random.randint(monsters_dict[monster]["min_damage"], monsters_dict[monster]["max_damage"])
                field[row][column-1][1] -= damage
                print(f"*** {monsters_dict[monster]['name']} in lane {rows_list[row]} dealt {damage} damage to {defenders_dict[obstacle]['name']}. ")
                if field[row][column-1][1] <= 0:
                    defender_killed(obstacle, monster, row, column-1)
                moves -= 1


# ======================================================================================================================
#                                              M A I N   C O D E
# ======================================================================================================================
start_game = True
while True:
    while start_game:
        choice = start_option()
        if choice == 1:
            new_game()
            spawn_monster()
            play_game = True
            start_game = False

        elif choice == 2:
            view_games = True
            while view_games:
                view_games, file_path = access_saved_games()

            if file_path is not None:
                load_game(file_path)
                play_game = True
                start_game = False

        elif choice == 3:
            game_instructions()

        else:
            start_game = False
            play_game = False
            quit_game(False)

    while play_game:
        print("")
        choice = combat_menu()
        if choice == 1:
            shop = True
            while shop:
                print("\n==================================================")
                print("{:^50}".format("S  H  O  P"))
                print("==================================================")
                print(f'\nAvailable gold: {game_vars["gold"]}')

                for count, i in enumerate(defenders_dict, start=1):
                    print(f'{count}. {defenders_dict[i]["name"]} ({defenders_dict[i]["price"]} gold)')
                print("7. Return to combat menu")

                while True:
                    option = select_option(len(defenders_list) + 1) - 1

                    if 0 <= option <= 5:
                        unit = defenders_list[option]

                        if game_vars["gold"] >= defenders_dict[unit]["price"]:
                            print("")
                            draw_field()
                            while True:
                                first_run = True
                                while first_run or placement_valid(placement) is False:
                                    first_run = False
                                    placement = input(f"Where would you like to place the {defenders_dict[unit]['name']}? (X to cancel) ")
                                    if placement.capitalize() == "X":
                                        break

                                [row, column] = placement_valid(placement)
                                if place_defender(unit, row, column):
                                    break
                                
                            shop = False

                        else:
                            print(f"\nYou do not have enough gold to buy the {defenders_dict[unit]['name']}!")
                            print(f"Required: {defenders_dict[unit]['price']} gold")
                            print(f"Available: {game_vars['gold']} gold")

                    else:
                        print("Returning to combat menu\n")
                        shop = False

                    break

        elif choice == 2:
            sell_unit()

        elif choice == 3:
            print("\n==================================================")
            print("{:^50}".format("U P G R A D E  S H O P"))
            print("==================================================")

            print("\nWhich defender would you like to upgrade? ")
            for count, unit in enumerate(defenders_list, start=1):
                if unit == "HEAL":
                    break
                print(f"{count}. {defenders_dict[unit]['name']} ({defenders_dict[unit]['upgrade_price']} gold)")
            print(f"{len(defenders_list)}. Return to combat menu")

            while True:
                option = select_option(len(defenders_list))
                if option == len(defenders_list):
                    break

                unit_to_upgrade = defenders_list[option - 1]
                if upgrade_unit(unit_to_upgrade):
                    break



        elif choice == 4:
            print("")
            for row in range(len(field)):
                for column in range(len(field[row])):
                    if field[row][column] is not None and field[row][column][0] in defenders_list:
                        defender = field[row][column][0]
                        if defender == "CANON" and game_vars["turn"] % 2 == 0:
                            print(f"*** Canon in lane {rows_list[row]} dealt no damage. ")
                        elif defender == "FARMR":
                            print(f"*** Farmer in lane {rows_list[row]} has given you {defenders_dict['FARMR']['gold_given']} gold.")
                            game_vars["gold"] += defenders_dict["FARMR"]["gold_given"]

                        elif defender in ["ARCHR", "CANON"]:
                            defender_attack(defender, row, column)

                    elif field[row][column] is not None and field[row][column][0] in monsters_list:
                        monster = field[row][column][0]
                        monster_advance(monster, row, column)

            game_vars["threat"] += random.randint(1, game_vars["danger_level"])
            if game_vars["threat"] >= game_vars["max_threat"]:
                for _ in range(math.floor(game_vars["threat"] / game_vars["max_threat"])):
                    spawn_monster()
                    game_vars["threat"] -= game_vars["max_threat"]

            game_vars["turn"] += 1
            game_vars["gold"] += 1
            if game_vars["turn"] % 12 == 0:
                print("The monsters have grown stronger!")
                game_vars["danger_level"] += 1
                for i in monsters_dict:
                    monsters_dict[i]["min_damage"] += 1
                    monsters_dict[i]["max_damage"] += 1
                    monsters_dict[i]["maxHP"] += 1
                    monsters_dict[i]["reward"] += 1

            monster_count = 0
            for row in range(len(field)):
                for column in range(len(field[row])):
                    if field[row][column] is not None and field[row][column][0] in monsters_list:
                        monster_count += 1
            if monster_count == 0:
                spawn_monster()

        elif choice == 5:
            while True:
                save_success = save_game()
                if save_success is False:
                    break

                if save_success[0]:
                    name = save_success[1]
                    relative_path = f"savedgames/{name}.txt"
                    current_path = os.path.dirname(os.path.realpath("__file__"))
                    file = os.path.join(current_path, relative_path)

                    if os.path.exists(file):
                        print(f"There is already a game saved as {name}.txt. ")
                        print("Would you like to overwrite the game?")


                    else:
                        print(f"Do you want to save the game as {name}.txt? ")

                    if confirmation() and save_to_file(file):
                        break

        elif choice == 6:
            quit_game(True)