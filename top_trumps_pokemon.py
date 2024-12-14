# Top trumps: Pokemon

# Import modules
import random
import requests

# Constants: minimum and maximum values for Pokemon IDs, max number of invalid responses, max number of rounds, stats
INVALID_RESPONSE = 3
MIN_ID = 1
MAX_ID = 151
MAX_ROUNDS = 10
# Playable stats
STATS_USED = ["height", "weight", "attack", "defence", "speed"] # Non-playable stats = ID and name

# Definition asking if player ready to play
def ready_to_play(counter = 0):
    response = input("Proceed with game? (Y/N): ").lower()

    if response == "y":
        return True
    elif response == "n" or response == "exit":
        return False
    # Default to "n" if invalid response recorded too many times
    elif counter >= INVALID_RESPONSE:
        print("-----------------------------------------")
        print("Invalid response recorded too many times.")
        return False
    else:
        print("Invalid response. ", end = "")
        counter += 1
        return ready_to_play(counter)

# Function for accessing Pokemon API
def get_pokemon_data(pokemon_drawn, counter = 0, counter_id = 0):
    # Generating random id between MIN and MAX
    pokemon_id = random.randint(MIN_ID, MAX_ID)

    # If ID has previously been drawn, get another id
    if pokemon_id in pokemon_drawn:
        # End program if no IDs left
        if counter_id >= INVALID_RESPONSE and len(pokemon_drawn) > MAX_ID:
            print("No more IDs available.")
            exit()
        # Else try to draw another ID
        counter_id += 1
        return get_pokemon_data(pokemon_drawn, counter, counter_id)

    # Using the Pokemon API get a Pokemon based on its ID number
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    response = requests.get(url)

    # Return data if id valid
    if response.status_code == 200:
        return response.json()
    # End game if too many errors while retrieving ID
    elif counter >= INVALID_RESPONSE:
        print("Too many errors while retrieving ID.")
        exit()
    # Get another random id if id invalid
    else:
        print("Error retrieving ID. ", end="")
        counter += 1
        return get_pokemon_data(pokemon_drawn, counter, counter_id)


# Function for creating top trump cards from Pokemon API data
def create_pokemon_dictionary(pokemon_drawn):
    # Calling get_pokemon_data() to obtain pokemon data
    data = get_pokemon_data(pokemon_drawn)

    # Access attack, defence and speed stats
    data_stats = data["stats"]
    length_stats = len(data_stats)
    attack = 0
    defence = 0
    speed = 0

    for i in range(length_stats):
        if data_stats[i]["stat"]["name"] == "attack":
            attack = data_stats[i]["base_stat"]
            break

    for i in range(length_stats):
        if data_stats[i]["stat"]["name"] == "defense":
            defence = data_stats[i]["base_stat"]
            break

    for i in range(length_stats):
        if data_stats[i]["stat"]["name"] == "speed":
            speed = data_stats[i]["base_stat"]
            break

    # Return a dictionary that contains selected stats of the Pokemon
    return {
        "name": data["name"],
        "id": data["id"],
        STATS_USED[0]: data["height"],
        STATS_USED[1]: data["weight"],
        STATS_USED[2]: attack,
        STATS_USED[3]: defence,
        STATS_USED[4]: speed,
    }


# Function asking the user which stat they want to use #TO-DO: limit incorrect input
def choose_stat(name, pokemon, player_score, opponent_score, counter=0):
    print(f">> a: {STATS_USED[0]}    b: {STATS_USED[1]}    "
          f"c: {STATS_USED[2]}   d: {STATS_USED[3]}    e: {STATS_USED[4]}")
    stat_to_play = input("Choice: ").lower()

    # Return stat if input matches corresponding letter or name of stat
    if stat_to_play == "a" or stat_to_play == STATS_USED[0]: # height
        return STATS_USED[0]

    if stat_to_play == "b" or stat_to_play == STATS_USED[1]: # weight
        return STATS_USED[1]

    if stat_to_play == "c" or stat_to_play == STATS_USED[2]: # attack
        return STATS_USED[2]

    if stat_to_play == "d" or stat_to_play == STATS_USED[3]: # defence
        return STATS_USED[3]

    if stat_to_play == "e" or stat_to_play == STATS_USED[4]: # speed
        return STATS_USED[4]

    # Exit if user types in 'exit'
    if stat_to_play == "exit":
        print_final_scores(name, player_score, opponent_score)
        exit()

    # If above fails, try to convert to int in case user typed numerical value for stat
    try:
        stat_int = int(stat_to_play)
    # Re-request input if int conversion fails
    except:
        if counter >= INVALID_RESPONSE:
            print("-----------------------------------------")
            print("Invalid input entered too many times.")
            print_final_scores(name, player_score, opponent_score)
            exit()
        # Else ask for user input again
        else:
            print("Input invalid. Please type a letter from a to e.")
            counter += 1
            return choose_stat(name, pokemon, player_score, opponent_score, counter)
    # If conversion to int successful
    else:
        # Seeing if the numerical input matches the stat value
        if stat_int == pokemon[STATS_USED[0]]: # height
            return STATS_USED[0]
        elif stat_int == pokemon[STATS_USED[1]]: # weight
            return STATS_USED[1]
        elif stat_int == pokemon[STATS_USED[2]]: # attack
            return STATS_USED[2]
        elif stat_int == pokemon[STATS_USED[3]]: # defence
            return STATS_USED[3]
        elif stat_int == pokemon[STATS_USED[4]]: # speed
            return STATS_USED[4]
        # If no match:
        else:
            # If incorrect input entered too many times, game ends
            if counter >= INVALID_RESPONSE:
                print("-----------------------------------------")
                print("Invalid input entered too many times.")
                print_final_scores(name, player_score, opponent_score)
                exit()
            # Else ask for user input again
            else:
                print("Input invalid. Please type a letter from a to e.")
                counter += 1
                return choose_stat(name, pokemon, player_score, opponent_score, counter)



# Function for opponent to choose stat
def opponent_choice():
    print("-----------------------------------------")

    stat_chosen = random.choice(STATS_USED)
    print(f"Your opponent chose to play the {stat_chosen} stat.")

    return stat_chosen

# Function asking player if they want to continue playing
def continue_play(name, player_score, opponent_score, counter = 0):
    confirmation = input("Continue playing? (Y/N) ").lower()

    if confirmation == "y":
        return True
    elif confirmation == "n" or confirmation == "exit":
        return False
    # Return false if invalid input typed too many times. This will end game.
    elif counter >= INVALID_RESPONSE:
        print("-----------------------------------------")
        print("Invalid input entered too many times.")
        return False
    else:
        print("Input invalid. ", end="")
        counter += 1
        return continue_play(name, player_score, opponent_score, counter)


# Function to print final scores
def print_final_scores(name, player_score, opponent_score):
    print("-----------------------------------------")
    print("-----------------------------------------")
    print("FINAL SCORES")
    print(f"{name}: {player_score}")
    print(f"Opponent: {opponent_score}")
    print("-----------------------------------------")

    # Print thanks
    print(f"Thanks for playing, {name}!")

# Function for one round of Top Trumps
def run_round(name, current_round, player_score, opponent_score, pokemon_drawn):
    print("-----------------------------------------")
    print("-----------------------------------------")
    print(f"ROUND {current_round}")
    print("-----------------------------------------")

    # Get a random Pokemon for the player and another for their opponent
    player_pokemon = create_pokemon_dictionary(pokemon_drawn)
    opponent_pokemon = create_pokemon_dictionary(pokemon_drawn)

    # Show player what their stats are for the Pokemon they drew
    print(f"You drew {player_pokemon["name"].title()} (Pokemon ID: {player_pokemon["id"]}). "
          f"Here are your Pokemon's stats: ")
    print(f">> {STATS_USED[0].title()}: {player_pokemon[STATS_USED[0]]}") # height
    print(f">> {STATS_USED[1].title()}: {player_pokemon[STATS_USED[1]]}") # weight
    print(f">> {STATS_USED[2].title()}: {player_pokemon[STATS_USED[2]]}") # attack
    print(f">> {STATS_USED[3].title()}: {player_pokemon[STATS_USED[3]]}") # defence
    print(f">> {STATS_USED[4].title()}: {player_pokemon[STATS_USED[4]]}") # speed

    # Opponent's choice on even rounds
    if current_round % 2 == 0:
        chosen_stat = opponent_choice()

        user_input = ""
        counter = 0
        while user_input != "y":
            # End game if user types incorrect input too many times
            if counter >= INVALID_RESPONSE:
                print("-----------------------------------------")
                print("Incorrect key typed too many times.")
                # Print final tally
                print_final_scores(name, player_score, opponent_score)
                exit()

            if user_input == "exit":
                # Print final tally
                print_final_scores(name, player_score, opponent_score)
                exit()

            user_input = input("Press 'y' to continue: ").lower()
            counter += 1

    # Player's choice on odd rounds
    else:
        # Ask player which stat they want to play
        print("Which stat do you want to use? Type a, b, c, d or e.")
        chosen_stat = choose_stat(name, player_pokemon, player_score, opponent_score)

    # Compare the player's and opponent's Pokemon on the chosen stat to decide who wins
    player_stat = player_pokemon[chosen_stat]
    opponent_stat = opponent_pokemon[chosen_stat]

    # Printing the stats
    print("-----------------------------------------")
    print(f"STAT CHOSEN: {chosen_stat}")
    print(f"You drew {player_pokemon["name"].title()} and played {player_stat}.")
    print(f"Your opponent drew {opponent_pokemon["name"].title()} and played {opponent_stat}.")

    # Displaying the results + tallying scores
    print("-----------------------------------------")
    if player_stat > opponent_stat:
        print("You win!")
        player_score += 1
    elif opponent_stat > player_stat:
        print("You lose!")
        opponent_score += 1
    elif player_stat == opponent_stat:
        print("It's a tie!")
        player_score += 1
        opponent_score += 1
    else:
        print("Invalid result.")

    # End game if maximum number of rounds has been equalled or exceeded
    if current_round >= MAX_ROUNDS:
        # Print final tally
        print_final_scores(name, player_score, opponent_score)
        exit()


    # Confirm whether player want to keep playing. If False, end game.
    keep_playing = continue_play(name, player_score, opponent_score)

    if keep_playing:
        return run_round(name, current_round + 1, player_score, opponent_score, pokemon_drawn)
    else:
        # Print final tally
        print_final_scores(name, player_score, opponent_score)
        exit()


# Function to run the game
def run_game():
    # Reset number of rounds
    rounds = 0

    # Clearing score tallies and list of Pokemon drawn so far
    player_score = 0
    opponent_score = 0
    pokemon_drawn = []

    print("-----------------------------------------")
    print("-----------------------------------------")
    print("\nWELCOME TO TOP TRUMPS: POKEMON!\n")
    print("-----------------------------------------")
    print("-----------------------------------------")

    # Asking user name (user name must be at least one character in length
    name = ""
    while len(name) < 1:
        name = input("Insert player name: ")

        if len(name) < 1:
            print("Name must be at least one character. ", end="")

    print(f"Hi {name}!")
    print("-----------------------------------------")
    print("HOW TO PLAY:")
    print("1. You and your opponent (the computer) will draw a random Pokemon.")
    print("2. You will pick a stat to compare.")
    print("3. The stats of your card and your opponent's card are compared.")
    print("4. The player who has the higher stat wins.")
    print("5. You and the opponent take turns to choose stats.\n")
    print("OTHER:")
    print("> Type 'exit' to leave the game at any time.")
    print("> The maximum number of rounds that can be played is 10.")
    print("-----------------------------------------")

    # Asking player if they are ready to play
    response = ready_to_play()

    if response:
        # insert player name here
        run_round(name, rounds + 1, player_score, opponent_score, pokemon_drawn)
    else:
        print("-----------------------------------------")
        print(f"See you another time, {name}!")



run_game()

# FEATURES:
# Multiple rounds
# Opponent choice on even rounds
# No duplicate pokemon
# Max number of rounds
# Type 'exit' at any point to end game
# Invalid input = request input again
# To select stat, player can type letter from a to e, the name of the stat or the value of the stat

# FURTHER:
# Make opponent's choice more intelligent
# Allow multiple cards to be drawn (although the game would not really be Top Trumps anymore)
# Classes!