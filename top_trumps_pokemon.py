# Top trumps: Pokemon

# Multiple rounds
# Opponent chooses on even rounds
# Attack, defence and speed stats added
# No duplicates

# Import modules
import random
import requests

# Constants: minimum and maximum values for Pokemon IDs, max number of invalid responses, max number of rounds
INVALID_RESPONSE = 3
MIN_ID = 1
MAX_ID = 151
MAX_ROUNDS = 10

# Definition asking if player ready to play
def ready_to_play(counter = 0):
    response = input("Proceed with game? (Y/N): ").lower()

    if response == "y":
        return True
    elif response == "n":
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

# Function for accessing Pokemon data
def get_pokemon_data(pokemon_drawn, counter = 0):
    # Generating random id between MIN and MAX
    id = random.randint(MIN_ID, MAX_ID)

    # If ID has previously been drawn, get another id
    if id in pokemon_drawn:
        return get_pokemon_data(pokemon_drawn)

    # Using the Pokemon API get a Pokemon based on its ID number
    url = f"https://pokeapi.co/api/v2/pokemon/{id}/"
    response = requests.get(url)

    # Return data if id valid
    if response.status_code == 200:
        return response.json()
    # End game if too many errors while retrieving ID
    elif counter >= INVALID_RESPONSE:
        print("Too many errors while retreiving ID.")
        exit()
    # Get another random id if id invalid
    else:
        print("Error retrieving ID. ", end="")
        counter += 1
        return get_pokemon_data(pokemon_drawn, counter)


# Function for creating trump cards from Pokemon API data
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
        stat = data_stats[i]
        if data_stats[i]["stat"]["name"] == "attack":
            attack = data_stats[i]["base_stat"]
            break

    for i in range(length_stats):
        stat = data_stats[i]
        if data_stats[i]["stat"]["name"] == "defense":
            defence = data_stats[i]["base_stat"]
            break

    for i in range(length_stats):
        stat = data_stats[i]
        if data_stats[i]["stat"]["name"] == "speed":
            speed = data_stats[i]["base_stat"]
            break

    # Return a dictionary that contains selected stats of the Pokemon
    return {
        "name": data["name"],
        "id": data["id"],
        "height": data["height"],
        "weight": data["weight"],
        "attack": attack,
        "defence": defence,
        "speed": speed,
    }


# Function asking the user which stat they want to use #TO-DO: limit incorrect input
def choose_stat(name, pokemon_stats, player_score, opponent_score, counter=0):
    print(">> a: height    b: weight    c: attack    d: defence    e: speed")
    stat_to_play = input("Choice: ").lower()

    # Return stat if input matches letter or name of stat
    if stat_to_play == "a" or stat_to_play == "height":
        return "height"
    elif stat_to_play == "b" or stat_to_play == "weight":
        return "weight"
    elif stat_to_play == "c" or stat_to_play == "attack":
        return "attack"
    elif stat_to_play == "d" or stat_to_play == "defence":
        return "defence"
    elif stat_to_play == "e" or stat_to_play == "speed":
        return "speed"
    # If incorrect input entered too many times, game ends
    elif counter >= INVALID_RESPONSE:
        print("-----------------------------------------")
        print("Invalid input entered too many times.")
        print_final_scores(name, player_score, opponent_score)
        exit()
    else:
        print("Input invalid. Please type a letter from a to e.")
        counter += 1
        return choose_stat(name, pokemon_stats, player_score, opponent_score, counter)


# Function for opponent to choose stat
def opponent_choice():
    stats = ["height", "weight", "attack", "defence", "speed"]
    print("-----------------------------------------")

    stat_chosen = random.choice(stats)
    print(f"Your opponent chose to play the {stat_chosen} stat.")

    return stat_chosen

# Function asking player if they want to continue playing
def continue_play():
    confirmation = input("Continue playing? (Y/N) ").lower()

    if confirmation == "y":
        return True
    elif confirmation == "n":
        return False
    else:
        print("Input invalid. ", end="")
        return continue_play()


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
def run_round(name, round, player_score, opponent_score, pokemon_drawn):
    print("-----------------------------------------")
    print("-----------------------------------------")
    print(f"ROUND {round}")
    print("-----------------------------------------")

    # Get a random Pokemon for the player and another for their opponent
    player_pokemon = create_pokemon_dictionary(pokemon_drawn)
    opponent_pokemon = create_pokemon_dictionary(pokemon_drawn)

    # Show player what their stats are for the Pokemon they drew
    print(f"You drew {player_pokemon["name"].title()} (Pokemon ID: {player_pokemon["id"]}). "
          f"Here are your Pokemon's stats: ")
    print(f">> Height: {player_pokemon["height"]}")
    print(f">> Weight: {player_pokemon["weight"]}")
    print(f">> Attack: {player_pokemon["attack"]}")
    print(f">> Defence: {player_pokemon["defence"]}")
    print(f">> Speed: {player_pokemon["speed"]}")

    # Opponent's choice on even rounds
    if round % 2 == 0:
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
    if round >= MAX_ROUNDS:
        # Print final tally
        print_final_scores(name, player_score, opponent_score)
        exit()

    # Confirm whether player want to keep playing. If False, end game.
    keep_playing = continue_play()

    if keep_playing == True:
        return run_round(name, round + 1, player_score, opponent_score, pokemon_drawn)
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

    # Asking user name
    name = input("Insert player name: ")
    print(f"Hi {name}! ", end="")

    # Asking player if they are ready to play
    response = ready_to_play()

    if response == True:
        # insert player name here
        run_round(name, rounds + 1, player_score, opponent_score, pokemon_drawn)
    else:
        print("-----------------------------------------")
        print(f"See you another time, {name}!")



run_game()

# TO-DO
# 1. Input name of player [done]
# 2. Max number of rounds (maybe 10) [done]
# 3. a, b, c, d, e
# 4. Thanks to name of player

# Maybe allow user to insert numerical value of stat as well
# Make opponent more intelligent when choosing which stat to play
# Maybe allow multiple cards to be drawn (though does top trumps allow that?)
# >> For above, maybe just set max number of rounds at like 20
# Maximum number of rounds
