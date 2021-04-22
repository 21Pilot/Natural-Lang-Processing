
# 2021 NATL
# Parsing Project_Grammar
# Seo

# sys.py file included in the zip file
# Python 3 program that converts a CFG to CNF from Professor Sable
import sys

# Initiate Parse
class Node:
    def __init__(self, data, left = None, right = None):
        self.left = left;
        self.right = right;
        self.data = data;

# Initiate bracket notation to be printed 
def bracket_parse(node):
  if node.right == None:
        result = "["+ node.data +" "+ node.left +"]"
  else:
        result = "["+ node.data +" "+ bracket_parse(node.left) +" "+ bracket_parse(node.right) +"]"
  return result

# Initiate textual parse tree
def text_parse(node, level =1):
  level = level;
  if node.right == None:
    result = "["+ node.data +" "+ node.left +"]\n";
  else:
    result = "["+ node.data +"\n" + "  "*level+ text_parse(node.left, level+1)+ level*"  " + text_parse(node.right, level+1) +(level-1)*"   "+ "]\n";
  return result

# Terminal categories 
# CNF Noun Terminal 
CNF_NounTerm = {};

# CNF Reverse Terminal
CNF_RevTerm = {};

# CNF Reverse Noun Terminal 
CNF_RevNounTerm = {}

# Valid Node Head
valid_Node = [];

# Load grammar rules from CNF
def load_grammar_rule(lines):
    for line in lines:
        # Skip any comment lines (#) in the grammar file
        # This is also in part of sys.py file 
        if not line.startswith("#"):
            words = line.split();

            # Load noun terminals
            if words[0] in CNF_NounTerm.keys():
                 CNF_NounTerm[words[0]].append([words[2], words[3]]);
            else:
                 CNF_NounTerm[words[0]] = [[words[2], words[3]]]; 

            # Create the possible end of rule for better searching 
            for w in [words[2], words[3]]:
                if w in CNF_RevNounTerm.keys():
                        CNF_RevNounTerm[w].add(words[0]);
                else:
                    CNF_RevNounTerm[w] = {words[0]};

# Parse sentence adopting the CKY algorithm 
def sentence_parse(sentence):
  # Split sentences to word lists 
  sentence = sentence.split();
  # Count the numbers of seperated words 
  n = len(sentence);

  # Initialize each sentence for prasing 
  nValid = 0;
  valid_Node.clear();

  # Initiate parse table
  table = [[ []for i in range(n+1)] for j in range (n+1)];
  for j in range(1,n+1):
        if sentence[j-1] in CNF_RevTerm.keys():

            # Diagonals
            for t in CNF_RevTerm[sentence[j-1]]:
                mnode = Node(t);
                mnode.left = sentence[j-1]
                table[j-1][j].append(mnode);
        # j-2 to 0
        for i in range(j-2, -1,-1):
            for k in range(i+1, j):
                # Iterate each entry
                for i_entry in table[i][k]:
                    for j_entry in table[k][j]:
                       
                        # Check if both i,j Noun Terminals 
                        # are both in whole Noun Terminal 
                        if i_entry.data in CNF_RevNounTerm.keys() and j_entry.data in CNF_RevNounTerm.keys():
                            
                            # Find the best fitting rule by checking intersection 
                            # on i and j entries 
                            fit_node =list(set(CNF_RevNounTerm[i_entry.data]) 
                            & set(CNF_RevNounTerm[j_entry.data]));
                            if len(fit_node)!= 0:
                                
                                for node in fit_node:
                                    if [i_entry.data,j_entry.data] in CNF_NounTerm[node]:
                                        temp_node = Node(node);
                                        temp_node.left = i_entry;
                                        temp_node.right = j_entry;
                                        table[i][j].append(temp_node);
                                        # A valid parse if found
                                        if node == 'S' and i == 0 and j == n:
                                            nValid = nValid + 1;
                                            valid_Node.append(temp_node);
  return nValid;

def get_arg():
    print_text = True if input("Do you want textual parse trees to be displayed(y/n)?:") == 'y' else False;
    while True:
        # User must provide input 
        user_sentence = input("Enter a sentence: ");
        # If quit is detected 
        if user_sentence == 'quit':
            print("Goodbye!");
            sys.exit(0);
        else:
            # If continue, parse the sentence 
            nValid = sentence_parse(user_sentence);
            # If no parse is found
            if not nValid:
                print("NO VALID PARSES");
            # If parse is found, print in bracket notation
            else:
                print("VALID SENTENCE\n");
                for i in range(0, nValid):
                    print("Valid parse #" + str(i+1) + ":");
                    print(bracket_parse(valid_Node[i]));
                    if print_text:
                        print("\n"+ text_parse(valid_Node[i]));
                print("\nNumber of valid parses: " + str(nValid));

def main():
    # Retrieve the appropriate file name 
    CNF_FileName = sys.argv[1];
    CNF_File = open(CNF_FileName,"r");
    lines = CNF_File.readlines();

    print("Grammar loaded");
    load_grammar_rule(lines);

    get_arg();

if __name__ == '__main__':
    main();

print('Thank you for allowing me the extension Professor Sable___Seo')
