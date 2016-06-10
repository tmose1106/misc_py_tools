#! /usr/bin/python3

class Config_File_Parse:

    def __init__(self, in_file):
        
        """ This function creates a diction of configuration keys and values
        by reading a specified text file passed as an argument. It excludes
        lines starting with '#' (to act as comments) and blank lines. All
        lines of value shoud be formatted as 'key: value', where the value
        can only be one word, while the value can be a full string.
        """

        self.config_dict = {}

        with open(in_file) as a_file:
            for line in a_file:

                key = ()
                value = ()

                if line[0] != '#' and line != '\n':
                    key, value = line.split(maxsplit=1)
                else:
                    continue
                
                self.config_dict[key[:-1]] = str(value.rstrip('\n'))


    def just_print(self):
        
        """ Almost self-explanitory, it just prints the dictionary itself. Not
        quite sure if it is useful, but may be a good debugging tool.
        """
        
        print(self.config_dict)


    def pretty_print(self):
        
        """ Print a somewhat formatted and visually pleasing output of all 
        variables found within the config file on a new line.
        """
        print("Configuration Dictionary")
        print("------------------------\n")
        for key in self.config_dict:
            print("Key: %s\tValue: %s" % (key, self.config_dict[key]))
