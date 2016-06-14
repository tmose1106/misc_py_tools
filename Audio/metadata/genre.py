# Standard
import os
# Dependencies
import xdg.BaseDirectory as xdg

def genre_format():

    genre_file = "%s/%s" % (xdg.load_first_config('trip'), 'genres')

    with open(genre_file) as config_file:
        
        genre_dictionary = {}
        index = 0
        
        for a_line in config_file:
            
            genre = a_line.rstrip('\n')
            
            genre_dictionary[str(index)] = genre

            index += 1

    return genre_dictionary

def genre_print(input_dictionary):
    
    """ This function is used to generate an ordered dictionary (for printing 
    purposes only) and then printing a nicely formatted list of genres from 
    the dictionary it is offered as an argument.
    
    The dictionary ordering function is thanks to Daniel Stutzbach on 
    stackoverflow in the thread 'How to sort alpha numeric set in python'
    """
    
    ord_dict = sorted(input_dictionary, key=lambda item: (int(item.partition(' ')[0])
                             if item[0].isdigit() else float('inf'), item))

    for index in ord_dict:
        output_string = "%s\t%s" % (index, input_dictionary[index])
        print(output_string) 

def genre_choice(input_dictionary):

    """ This function is responsible for executing a small CLI prompt for
    the user to choose a genre. If their choice is valid, then the proper
    dictionary value is returned as a string.
    """

    print("Choose a genre by entering an index listed below")
    genre_print(input_dictionary)
    choice = input("Your choice: ")

    if not choice in input_dictionary:
        print("Invalid choice")
    
    return input_dictionary[choice]

if __name__ == '__main__':
    genre_dict = genre_format()
    choice = genre_choice(genre_dict)
    print(choice)
