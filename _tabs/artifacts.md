---
# the default layout is 'page'
icon: fas fa-info-circle
order: 3
---

# Enhancement One: Software Design and Engineering

## Original

### Encryption.cpp
```cpp
// Encryption.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <cassert>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <ctime>

/// <summary>
/// encrypt or decrypt a source string using the provided key
/// </summary>
/// <param name="source">input string to process</param>
/// <param name="key">key to use in encryption / decryption</param>
/// <returns>transformed string</returns>
std::string encrypt_decrypt(const std::string& source, const std::string& key)
{
    // get lengths now instead of calling the function every time.
    // this would have most likely been inlined by the compiler, but design for perfomance.
    const auto key_length = key.length();
    const auto source_length = source.length();

    // assert that our input data is good
    assert(key_length > 0);
    assert(source_length > 0);

    std::string output = source;

    // loop through the source string char by char
    for (size_t i = 0; i < source_length; ++i)
    { // TODO: student need to change the next line from output[i] = source[i]
      // transform each character based on an xor of the key modded constrained to key length using a mod
        output[i] = source[i] ^ key[i % key_length];
    }

    // our output length must equal our source length
    assert(output.length() == source_length);

    // return the transformed string
    return output;
}

std::string read_file(const std::string& filename)
{
    //std::string file_text = "John Q. Smith\nThis is my test string";

    // TODO: implement loading the file into a string
    std::ifstream input_file(filename);
    if (!input_file) {
        std::cerr << "Could not open file: " << filename << std::endl;
        return "";
    }

    std::stringstream buffer;
    buffer << input_file.rdbuf();

    return buffer.str();
}

std::string get_student_name(const std::string& string_data)
{
    std::string student_name;

    // find the first newline
    size_t pos = string_data.find('\n');
    // did we find a newline
    if (pos != std::string::npos)
    { // we did, so copy that substring as the student name
        student_name = string_data.substr(0, pos);
    }

    return student_name;
}

void save_data_file(const std::string& filename, const std::string& student_name, const std::string& key, const std::string& data)
{
    //  TODO: implement file saving
    //  file format
    //  Line 1: student name
    //  Line 2: timestamp (yyyy-mm-dd)
    //  Line 3: key used
    //  Line 4+: data

    std::ofstream output_file(filename);
    if (!output_file) {
        std::cerr << "Could not open file for writing: " << filename << std::endl;
        return;
    }

    std::time_t t = std::time(nullptr);
    std::tm tm_buf;
    localtime_s(&tm_buf, &t);

    output_file << student_name << "\n";
    output_file << std::put_time(&tm_buf, "%Y-%m-%d") << "\n";
    output_file << key << "\n";
    output_file << data;

    output_file.close();
}

int main()
{
    std::cout << "Encyption Decryption Test!" << std::endl;

    // input file format
    // Line 1: <students name>
    // Line 2: <Lorem Ipsum Generator website used> https://pirateipsum.me/ (could be https://www.lipsum.com/ or one of https://www.shopify.com/partners/blog/79940998-15-funny-lorem-ipsum-generators-to-shake-up-your-design-mockups)
    // Lines 3+: <lorem ipsum generated with 3 paragraphs> 
    //  Fire in the hole bowsprit Jack Tar gally holystone sloop grog heave to grapple Sea Legs. Gally hearties case shot crimp spirits pillage galleon chase guns skysail yo-ho-ho. Jury mast coxswain measured fer yer chains man-of-war Privateer yardarm aft handsomely Jolly Roger mutiny.
    //  Hulk coffer doubloon Shiver me timbers long clothes skysail Nelsons folly reef sails Jack Tar Davy Jones' Locker. Splice the main brace ye fathom me bilge water walk the plank bowsprit gun Blimey wench. Parrel Gold Road clap of thunder Shiver me timbers hempen halter yardarm grapple wench bilged on her anchor American Main.
    //  Brigantine coxswain interloper jolly boat heave down cutlass crow's nest wherry dance the hempen jig spirits. Interloper Sea Legs plunder shrouds knave sloop run a shot across the bow Jack Ketch mutiny barkadeer. Heave to gun matey Arr draft jolly boat marooned Cat o'nine tails topsail Blimey.

    const std::string file_name = "inputdatafile.txt";
    const std::string encrypted_file_name = "encrypteddatafile.txt";
    const std::string decrypted_file_name = "decrytpteddatafile.txt";
    const std::string source_string = read_file(file_name);
    const std::string key = "password";

    // get the student name from the data file
    const std::string student_name = get_student_name(source_string);

    // encrypt sourceString with key
    const std::string encrypted_string = encrypt_decrypt(source_string, key);

    // save encrypted_string to file
    save_data_file(encrypted_file_name, student_name, key, encrypted_string);

    // decrypt encryptedString with key
    const std::string decrypted_string = encrypt_decrypt(encrypted_string, key);

    // save decrypted_string to file
    save_data_file(decrypted_file_name, student_name, key, decrypted_string);

    std::cout << "Read File: " << file_name << " - Encrypted To: " << encrypted_file_name << " - Decrypted To: " << decrypted_file_name << std::endl;

    // students submit input file, encrypted file, decrypted file, source code file, and key used
}
```

## Enhanced

### main.go
```go
/*
Project: CS 499 Capstone Software Engineering Enhancement
Author: Cody Stuart
Description: This is a Golang refactor of the same code functionality from a C++ utility demonstrating XOR encryption.
*/
package main

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"os"
	"strings"
	"time"
)

type DataTransformer struct {
	Key string
}

// EncryptDecrypt performs a symmetric bitwise XOR transformation.
// Because XOR is its own inverse, the same function is used for both
// encryption and decryption phases.
func (dt *DataTransformer) EncryptDecrypt(source []byte) []byte {
	keyLen := len(dt.Key)
	if keyLen == 0 {
		return source
	}

	// Pre-allocate output buffer to match the source length for memory efficiency
	output := make([]byte, len(source))
	for i := 0; i < len(source); i++ {
		/* * The modulo operator (%) allows the key to repeat cyclically if it
		 * is shorter than the source data, ensuring every byte is processed.
		 */
		output[i] = source[i] ^ dt.Key[i%keyLen]
	}
	return output
}

// SaveWithMetadata writes the payload to disk preceded by structured metadata.
func SaveWithMetadata(filename, studentName, key string, data []byte) error {
	file, err := os.Create(filename)
	if err != nil {
		return err
	}
	// Defer ensuring the file handle is released once the function returns
	defer file.Close()

	// Using Go's standard time formatting for consistent timestamping (YYYY-MM-DD)
	timestamp := time.Now().Format("2006-01-02")

	// Writing structured metadata: Line 1 = Name, Line 2 = Date, Line 3 = Key.
	fmt.Fprintln(file, studentName)
	fmt.Fprintln(file, timestamp)
	fmt.Fprintln(file, key)
	file.Write(data)

	return nil
}

// getStudentName extracts the identifier from the first line fo the input data
func getStudentName(stringData string) string {
	studentName := ""

	// Locates the first newline character to isolate header information
	pos := strings.Index(stringData, "\n")

	if pos != -1 {
		// slices the string from start to the first newline found.
		studentName = stringData[0:pos]
	}

	return studentName
}

// generateRandomKey provides a cryptographically secure alternative to hardcoded passwords.
func generateRandomKey(length int) (string, error) {
	bytes := make([]byte, length)
	// Using crypto/rand for high-entropy random byte generation.
	if _, err := rand.Read(bytes); err != nil {
		return "", err
	}
	// Convert bytes to a hex string so it's human-readable in metadata
	return hex.EncodeToString(bytes)[:length], nil
}

func main() {
	fileName := "inputdatafile.txt"

	// Enhancement: Dynamically generating a unique key for every session/
	key, err := generateRandomKey(16)
	if err != nil {
		fmt.Printf("Error generating random key %s\n", err)
		return
	}
	fmt.Printf("Generated random key %s\n", key)

	// Reading the input file into memory as a byte slice
	rawData, err := os.ReadFile(fileName)
	if err != nil {
		fmt.Printf("Error reading file: %v\n", err)
		return
	}

	// Parsing the student name from the raw file contents
	studentName := getStudentName(string(rawData))

	// Initialize the transformer with the generated key.
	transformer := DataTransformer{Key: key}

	// Encypting the file.
	encrypted := transformer.EncryptDecrypt(rawData)
	SaveWithMetadata("encrypted.txt", studentName, key, encrypted)

	// Decrypting the file to verify symmetric properties of XOR bitwise encryption.
	decrypted := transformer.EncryptDecrypt(encrypted)
	SaveWithMetadata("decrypted.txt", studentName, key, decrypted)

	fmt.Println("Transformation Complete.")
}
```

---
# Enhancement Two: Algorithms and Data Structures

## Original

### ContactService.java
```java
package com.stuart.contacts;

import java.util.HashMap;
import java.util.Map;

public class ContactService {
	private Map<String, Contact> contacts;
	
	public ContactService() {
		contacts = new HashMap<>();
	}
	
	
	public void addContact(String contactID, String firstName, String lastName, String phoneNumber, String address) {
		
		// Throw an error message if the contact already exist in the HashMap
		if (contacts.containsKey(contactID)) {
			throw new IllegalArgumentException("Contact ID " + contactID + " already exists. Contact IDs must be unique");
		}
		
		// Create a contact object using the passed in variables and then add it to the map
		Contact contact = new Contact(contactID, firstName, lastName, phoneNumber, address);
		contacts.put(contactID, contact);
	}
	
	public void deleteContact(String contactID) {
		
		// Throw an error if the contactID is not in the HashMap
		if (!contacts.containsKey(contactID)) {
			throw new IllegalArgumentException("Contact ID " + contactID + " not found.");
		}
		// This line removes the contact assuming it is found an error is not thrown. 
		contacts.remove(contactID);
	}
	
	public void updateContact(String contactID, String firstName, String lastName, String phoneNumber, String address) {
		// Use the provided contact ID to find the information we want to update
		Contact contact = contacts.get(contactID);
		if (contact == null) {
			throw new IllegalArgumentException("Contact ID " + contactID + " not found.");
		}
		
		// Assuming a contact was found, set the update values
		contact.setFirstName(firstName);
		contact.setLastName(lastName);
		contact.setPhoneNumber(phoneNumber);
		contact.setAddress(address);
	}

	
	// Useful method to assist in testing. We can use this to get contacts 
	public Contact getContact(String contactID) {
		return contacts.get(contactID);
	}
}
```

## Enhanced

### Trie.java
```java
package com.stuart.contacts;

import java.util.ArrayList;
import java.util.List;

// The Trie class manages the root and provides the logic for indexing and searching contacts.
public class Trie {
	
	private TrieNode root;
	
	public Trie() {
		root = new TrieNode();
	}
	
/*
 *Inserts a name into the Trie and associates it with a Contact Object. O(L) complexity where L is the length of the name. 
 * */
 
	public void insert(String key, Contact contact) {
		// Check for null or empty keys.
		if (key == null || key.isEmpty()) {
			return;
		}
		
		TrieNode curr = root;
		
		// Normalize to lowercase to ensure case-insensitive searching.
		for (char c : key.toLowerCase().toCharArray()) {
			int index = c - 'a';
			
			// Bounds checking to safely ignore non-alphabetic characters. 
			if (index < 0 || index >= 26) {
				continue;
			}
			
			// Build the tree path if the character node doesn't exist.
			if (curr.children[index] == null) {
				curr.children[index] = new TrieNode();
			}
			curr = curr.children[index];
			
			// Add the contact to this node's list if it isn't already present
			if (!curr.contactList.contains(contact)) {
				curr.contactList.add(contact);
			}
		}
		
		// Mark the final node as the completion of a full name.
		curr.isEndOfWord = true;
	}

	// Searches for all contacts matching a specific prefix.
	public List<Contact> search(String prefix) {
		// Check for null or empty prefixes.
		if (prefix == null || prefix.isEmpty()) {
			return new ArrayList<>();
		}
		
		TrieNode curr = root;
		
		 // Traverses the tree based on the provided prefix.
		for (char c : prefix.toLowerCase().toCharArray()) {
			int index = c - 'a';
			if (index < 0 || index >= 26) continue;
			
			// If a node path is missing, no contacts match this prefix.
			if (curr.children[index] == null) {
				return new ArrayList<>();
			}
			curr = curr.children[index];
		}
		
		// Return the list of contacts at this prefix level.
		return curr.contactList;
	}
	
	// Boolean helper to verify if any contacts exist for a given prefix
	public boolean isPrefix(String prefix) {
		List<Contact> results = search(prefix);
		return !results.isEmpty();
	}
	
	// Local verification of the Trie logic.
	public static void main(String[] args) {
		Trie trie = new Trie();
		
		// Example contact for manual validation
		Contact con1 = new Contact("1", "Cody", "Stuart", "1234567890", "123 Lane");
		trie.insert("Cody", con1);
		
		// Verify prefix retrieval.
		List<Contact> results = trie.search("Co");
		System.out.println("Found: " + results.get(0).getLastName());
	}

}
```

### TrieNode.java
```java
/*
Project: CS 499 Capstone Algorithims and Data Structures Enhancement
Author: Cody Stuart
Description: This is one of two classes designed to add search-by-prefix to the Contacts java package.
*/

 

package com.stuart.contacts;

import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;

public class TrieNode {
	
	// Array for child nodes each node represents a letter in the English alphabet (a-z).
	TrieNode[] children;
	
	// A collection of contact references, allowing retrieval of the full object.
	List<Contact> contactList;
	
	// Used to indicate the end of a string
	boolean isEndOfWord;
	
	// Constructor
	public TrieNode() {
		
		// Initialize the word end
		isEndOfWord = false;
		
		// Fixed size array for character to index mapping
		children = new TrieNode[26];
		
		// Initialized list to prevent NullPointerExceptions
		contactList = new ArrayList<>();
	}
}
```
---
# Enhancement Three: Databases

## Original

### CRUD_Python_Module.py
```python
# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username, password): # Get username and password as parameters.
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        # USER = 'aacuser'
        # PASS = 'verySecurePassword' 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        try:
            self.client = MongoClient('mongodb://%s:%s@%s:%d' % (username,password,HOST,PORT)) 
            self.database = self.client['%s' % (DB)] 
            self.collection = self.database['%s' % (COL)]
            print("Connection to MongoDB successful!")
        except Exception as e:
            print(f" Could not connect to MongoDB: {e}")

    def aggregate(self, pipeline):
        if pipeline is not None:
            try:
                cursor = self.collection.aggregate(pipeline)
                return list(cursor)
            except Exception as e:
                print(f"An error occured during aggregation: {e}")
                return []
        else:
            raise Exception("Pipeline parameter is required for aggregation.")

    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        """
        Inserts a document into the 'animals' collection
        @param data: A dictionary representing the document to insert.
        @return: True if the insert was successful, otherwise False.
        """
        if data is not None: # validate paramters being passed in have actual values.
            try:
                result = self.database.animals.insert_one(data)  # data should be dictionary
                return result.acknowledged # returns True if data is inserted
            except Exception as e:
                print(f"An error occured during insert: {e}")
                return False
        else: 
            raise Exception("Nothing to save, because data parameter is empty") 

    # Create method to implement the R in CRUD.
    def read(self, query):
        """
        Queries for documents in the 'animals' collection.
        @param query: A dictionary defining the search criteria.
        @return: A list of matching documents. Returns an empty list if no matches.
        """
        if query is not None: # validate paramters being passed in have actual values.
            try:
                # The find() method returns a 'cursor' which is a pointer to the results.
                cursor = self.collection.find(query)
                # Convert the cursor to a list to return all matching documents
                results_list = list(cursor)
                return results_list
            except Exception as e:
                print(f"An error occured during read operation: {e}")
                return [] # returns an empty list
            
    def read_water_rescue(self):
        query = {
            "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
            "sex_upon_outcome": "Intact Female",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
        return self.read(query)

    def read_water_rescue_optimized(self):
        pipeline = [
            {"$match": {
                "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
                "sex_upon_outcome": "Intact Female",
                "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
            }},
            {"$project": {
                "_id": 0,
                "name": 1,
                "breed": 1,
                "age_upon_outcome_in_weeks": 1,
                "location_lat": 1,
                "location_long": 1
            }}
        ]
        return self.aggregate(pipeline)
    
    def read_mountain_rescue(self):
        query = {
           "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
        return self.read(query)

    def read_disaster_rescue(self):
        query = {
            "breed": {"$in": ["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
        return self.read(query)

            
    # Update method to implement the U in CRUD.
    def update(self, query, newValues):
        """
        Updates one or more documents matching a query.
        @param query: A dictionary defining the documents to update.
        @param newValues: A dictionary containing the fields and new values to set.
        @return: The number of documents that were modified
        """
        if query is not None and newValues is not None: # validate paramters being passed in have actual values.
            try:
                result = self.collection.update_many(query, {"$set": newValues})
                # Get the number of records modified as the return value
                return result.modified_count
            except Exception as e:
                print(f"An error occured during update: {e}")
                return 0
        else:
            raise Exception ("Query and newValues parameters are required to update.")
    
    # Delete method to implement the D in CRUD.
    def delete(self, query):
        """
        Deletes one or more documents matching a query.
        @param query: A dictionary defining the documents to delete.
        @return: The number of documents deleted. 
        """
        if query is not None: # validate paramters being passed in have actual values.
            try:
                result = self.collection.delete_many(query)
                # return the number of records deleted
                return result.deleted_count
            except Exception as e:
                print(f"An error occured during deletion: {e}")
                return 0 # When delete fails return 0
        else:
            raise Exception("Query paramter is required for deletion.")

```

### ProjectTwoDashboard.ipynb
```python
# Setup the Jupyter version of Dash
from jupyter_dash import JupyterDash

# Configure the necessary Python module imports for dashboard components
import dash_leaflet as dl
from dash import dcc, html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output, State
import base64
JupyterDash.infer_jupyter_proxy_config()

# Configure OS routines
import os

# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from CRUD_Python_Module import AnimalShelter

###########################
# Data Manipulation / Model
###########################
username = "aacuser"
password = "verySecurePassword"

# Connect to database via CRUD Module
db = AnimalShelter(username, password)

# class read method must support return of list object and accept projection json input
# sending the read method an empty document requests all documents be returned
df = pd.DataFrame.from_records(db.read({}))

# MongoDB v5+ is going to return the '_id' column and that is going to have an 
# invlaid object type of 'ObjectID' - which will cause the data_table to crash - so we remove
# it in the dataframe here. The df.drop command allows us to drop the column. If we do not set
# inplace=True - it will reeturn a new dataframe that does not contain the dropped column(s)
df.drop(columns=['_id'],inplace=True)

## Debug
# print(len(df.to_dict(orient='records')))
# print(df.columns)


#########################
# Dashboard Layout / View
#########################
app = JupyterDash(__name__)

image_filename = 'Grazioso Salvare Logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([
#    html.Div(id='hidden-div', style={'display':'none'}),
    html.Center(html.B(html.H1('OnlyDogs.com'))),
    
    # Branding
    html.Center([
        html.A(
            html.Img(
                src='data:image/png;base64,{}'.format(encoded_image.decode()),
                style={'width': '200px'}    
                    ),
            href="http://www.snhu.edu"
        ),
        html.P("Dashboard by: Cody Stuart")
    ]),
    html.Hr(),
    html.Div(
        dcc.RadioItems(
            id='filter-type',
            options=[
                {'label': 'Water Rescue', 'value': 'water'},
                {'label': 'Mountain or Wilderness Rescue', 'value': 'mountain'},
                {'label': 'Disaster Rescue or Individual Tracking', 'value': 'disaster'},
                {'label': 'Reset', 'value': 'reset'}
            ],
            value='reset',
            labelStyle={'display': 'inline-block', 'margin-right': '10px'}
        )

    ),
    html.Hr(),
    dash_table.DataTable(id='datatable-id',
                         columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns],
                         data=df.to_dict('records'),
                        editable=False, # Prevents users from making edits to the table
                        filter_action="native", # Enables a filter box for each column
                        sort_action="native", # Allows users to sort columns by clicking headers
                        sort_mode="multi", # Allows multiple columns to be sorted
                        column_selectable=False, # Disabled the selection of entire columns
                        row_selectable="single", # Allows users to select a single row at a time
                        row_deletable=False, # prevents users from deleting rows
                        selected_columns=[], # Inititalizes wtih no columns selected
                        selected_rows=[0], # Selects the first row by default to ensure the map has initial data
                        page_action="native", # Enables pagination
                        page_current=0, # Starts on the first page
                        page_size=10 # Displays 10 rows per page
                        ),
    html.Br(),
    html.Hr(),
#This sets up the dashboard so that your chart and your geolocation chart are side-by-side
    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',

            ),
        html.Div(
            id='map-id',
            className='col s12 m6',
            ),
        html.Div(
            id='hist-id',
            className='col s12 m6'
        )
        ])
])

#############################################
# Interaction Between Components / Controller
#############################################



    
@app.callback(Output('datatable-id','data'),
              [Input('filter-type', 'value')])
def update_dashboard(filter_type):
    # Check which filter was selected and call the appropriate CRUD method
    if filter_type == 'water':
        data = db.read_water_rescue()
    elif filter_type == 'mountain':
        data = db.read_mountain_rescue()
    elif filter_type == 'disaster':
        data = db.read_disaster_rescue()
    else:
        data = db.read({}) # 'reset' or default case

    # If no data is returned, return an empty list
    if not data:
        return []
    
    # Convert the list of dicts from MongoDB into a DataFrame
    df = pd.DataFrame.from_records(data)
    
    # MongoDB v5+ is going to return the '_id' column and that is going to have an 
    # invlaid object type of 'ObjectID' - which will cause the data_table to crash - so we remove
    # it in the dataframe here. The df.drop command allows us to drop the column. If we do not set
    # inplace=True - it will reeturn a new dataframe that does not contain the dropped column(s)
    df.drop(columns=['_id'], inplace=True)
    
    # Return the filtered data as a list of dictionaries
    return df.to_dict('records')

# Display the breeds of animal based on quantity represented in
# the data table
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data")])
def update_graphs(viewData):
    # If the table data is empty, return nothing
    if not viewData:
        return []
    # Convert the visible table data into a DataFram
    dff = pd.DataFrame.from_dict(viewData)
    
    # Get the counts of each breed for the pie chart
    pie_data = dff['breed'].value_counts().reset_index()
    pie_data.columns = ['breed', 'count']
    
    # Create the pie cahrt figure
    fig_pie = px.pie(pie_data,
                     names='breed',
                     values='count',
                     title='Preferred Animals Breed Shares')

    return [
        dcc.Graph(
            figure=fig_pie,
            responsive=False
        )
    ]
    
#This callback will highlight a cell on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


# This callback will update the geo-location chart for the selected data entry
# derived_virtual_data will be the set of data available from the datatable in the form of 
# a dictionary.
# derived_virtual_selected_rows will be the selected row(s) in the table in the form of
# a list. For this application, we are only permitting single row selection so there is only
# one value in the list.
# The iloc method allows for a row, column notation to pull data from the datatable
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")])
def update_map(viewData, index):  
    if viewData is None:
        return
    elif index is None:
        return
    
    dff = pd.DataFrame.from_dict(viewData)
    
    if dff.empty:
        return [
                dl.Map(style={'width': '1000px', 'height': '500px'},
                   center=[30.75,-97.48], zoom=10, children=[
                   dl.TileLayer(id="base-layer-id")
                   ])
                ]   
    # Because we only allow single row selection, the list can be converted to a row index here
    if not index:
        row = 0
    else: 
        row = index[0]
        
    # Austin TX is at [30.75,-97.48]
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, 
            center=[30.75,-97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            # Marker with tool tip and popup
            # Column 13 and 14 define the grid-coordinates for the map
            # Column 4 defines the breed for the animal
            # Column 9 defines the name of the animal
            dl.Marker(position=[dff.iloc[row,13],dff.iloc[row,14]], 
                children=[
                dl.Tooltip(dff.iloc[row,4]),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(dff.iloc[row,9])
                ])
            ])
        ])
    ]

# Callback to create and display the Histogram
@app.callback(
    Output('hist-id', "children"),
    [Input('datatable-id', "derived_virtual_data")])
def update_histogram(viewData):
    # if the table is empty, return nothing
    if not viewData:
        return []
    
    # Convert the visibale table data into a DataFrame
    dff = pd.DataFrame.from_dict(viewData)

    # Create the histogram figure using the age in weeks column
    fig_hist = px.histogram(dff,
                            x='age_upon_outcome_in_weeks',
                            title='Age Distribution (in weeks)')

    return [
        dcc.Graph(
            figure=fig_hist,
            responsive=False
        )
    ]
# Run app and display result in jupyterlab mode, note, if you have previously run a prior app, the default port of 8050 may not be available, if so, try setting an alternate port.
app.run_server() 
```

## Enhanced

### Setup_MongoDB.py
```python
"""
Author: Cody Stuart
Project: CS-499 Enhancement 3 - Databases
This python module is being used to create MongoDB environment necessary to enhance the original code to use aggregation pipelines.
"""
import pandas as pd
from pymongo import MongoClient

def setup_database(csv_file_path):
    # MongoDB info
    HOST = 'localhost'
    PORT = 27017
    DB_NAME = 'aac'
    COLLECTION_NAME = 'animals'

    # MongoDB Creds to be used for pulling information from the database. In a real environment this would not be hardcoded.
    USER = 'aacuser'
    PASSWORD = 'verySecurePassword'

    try:
        client = MongoClient(f'mongodb://{HOST}:{PORT}/')
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        try:
            db.command("createUser", USER, pwd=PASSWORD, roles=[{"role": "readWrite", "db": DB_NAME}])
            print(f"User '{USER}' created successfully with readWrite permissions on '{DB_NAME}'.")
        except Exception as e:
            if "already exists" in str(e):
                print(f"User '{USER}' already exists. Skipping creation.")
            else:
                raise e

        print(f"Reading data from {csv_file_path}...")
        df = pd.read_csv(csv_file_path)

        data_dict = df.to_dict(orient='records')

        collection.delete_many({})
        print("Existing collection cleared.")

        result = collection.insert_many(data_dict)

        print(f"Successfully created local database '{DB_NAME}' and collection '{COLLECTION_NAME}'.")
        print(f"Inserted {len(result.inserted_ids)} documents.")

    except Exception as e:
        print(f"An error occured during database setup: {e}")

if __name__ == "__main__":
    setup_database('aac_shelter_outcomes.csv')
```

### CRUD_Python_Module_Enhanced.py
```python
# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username, password): # Get username and password as parameters.
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        # USER = 'aacuser'
        # PASS = 'verySecurePassword' 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        try:
            self.client = MongoClient('mongodb://%s:%s@%s:%d/?authSource=%s' % (username,password,HOST,PORT, DB)) # Updated this string to find the aacuser in the aac DB instead of the admin DB. A user solely for aac should not be a total admin.
            self.database = self.client['%s' % (DB)] 
            self.collection = self.database['%s' % (COL)]
            print("Connection to MongoDB successful!")
        except Exception as e:
            print(f" Could not connect to MongoDB: {e}")



    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        """
        Inserts a document into the 'animals' collection
        @param data: A dictionary representing the document to insert.
        @return: True if the insert was successful, otherwise False.
        """
        if data is not None: # validate paramters being passed in have actual values.
            try:
                result = self.database.animals.insert_one(data)  # data should be dictionary
                return result.acknowledged # returns True if data is inserted
            except Exception as e:
                print(f"An error occured during insert: {e}")
                return False
        else: 
            raise Exception("Nothing to save, because data parameter is empty")

    # Added for MongoDB aggregation.
    def aggregate(self, pipeline):
        if pipeline is not None:
            try:
                cursor = self.collection.aggregate(pipeline)
                return list(cursor)
            except Exception as e:
                print(f"An error occured during aggregation: {e}")
                return []
        else:
            raise Exception("Pipeline parameter is required for aggregation.")

    # Create method to implement the R in CRUD.
    def read(self, query):
        """
        Queries for documents in the 'animals' collection.
        @param query: A dictionary defining the search criteria.
        @return: A list of matching documents. Returns an empty list if no matches.
        """
        if query is not None: # validate paramters being passed in have actual values.
            try:
                # The find() method returns a 'cursor' which is a pointer to the results.
                cursor = self.collection.find(query)
                # Convert the cursor to a list to return all matching documents
                results_list = list(cursor)
                return results_list
            except Exception as e:
                print(f"An error occured during read operation: {e}")
                return [] # returns an empty list

    def read_rescue(self, rescue_type):
        """
        Enhanced: A single method that dynamically builds an Aggregation Pipeline based on the requested rescue category.
        """
        rescue_configs = {
            'water': ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"],
            'mountain': ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"],
            'disaster': ["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]
        }
        breeds = rescue_configs.get(rescue_type, [])

        sex = "Intact Female" if rescue_type == 'water' else "Intact Male"

        pipeline = [
            {
                "$match": {
                    "breed": {"$in": breeds},
                    "sex_upon_outcome": sex,
                    "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
                }
            },
            # Optimization: Only return the fields the dashboard actually renders
            {
                "$project": {
                    "_id": 0,
                    "age_upon_outcome": 1,
                    "name": 1,
                    "breed": 1,
                    "age_upon_outcome_in_weeks": 1,
                    "location_lat": 1,
                    "location_long": 1,
                    "animal_id": 1,
                    "color": 1,
                    "date_of_birth": 1,
                    "datetime": 1,
                    "monthyear": 1,
                    "outcome_subtype": 1,
                    "outcome_type": 1,
                    "sex_upon_outcome": 1,
                    "location_lat": 1,
                    "location_long": 1,
                    "animal_type": 1
                }
            },
            {
                "$addFields": {
                    "age_upon_outcome_in_weeks": {"$round": ["$age_upon_outcome_in_weeks", 0]}
                }
            }
        ]
        return self.aggregate(pipeline)
            
    def read_water_rescue(self):
        query = {
            "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
            "sex_upon_outcome": "Intact Female",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
        return self.read(query)
    
    def read_mountain_rescue(self):
        query = {
           "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
        return self.read(query)

    def read_disaster_rescue(self):
        query = {
            "breed": {"$in": ["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
        return self.read(query)

            
    # Update method to implement the U in CRUD.
    def update(self, query, newValues):
        """
        Updates one or more documents matching a query.
        @param query: A dictionary defining the documents to update.
        @param newValues: A dictionary containing the fields and new values to set.
        @return: The number of documents that were modified
        """
        if query is not None and newValues is not None: # validate paramters being passed in have actual values.
            try:
                result = self.collection.update_many(query, {"$set": newValues})
                # Get the number of records modified as the return value
                return result.modified_count
            except Exception as e:
                print(f"An error occured during update: {e}")
                return 0
        else:
            raise Exception ("Query and newValues parameters are required to update.")
    
    # Delete method to implement the D in CRUD.
    def delete(self, query):
        """
        Deletes one or more documents matching a query.
        @param query: A dictionary defining the documents to delete.
        @return: The number of documents deleted. 
        """
        if query is not None: # validate paramters being passed in have actual values.
            try:
                result = self.collection.delete_many(query)
                # return the number of records deleted
                return result.deleted_count
            except Exception as e:
                print(f"An error occured during deletion: {e}")
                return 0 # When delete fails return 0
        else:
            raise Exception("Query paramter is required for deletion.")
```

### Dashboard.py
```python
import base64
import os
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_leaflet as dl
import plotly.express as px
import pandas as pd

from CRUD_Python_Module_Enhanced import AnimalShelter

###########################
# Data Manipulation / Model
###########################
username = "aacuser"
password = "verySecurePassword"

# Initialize local MongoDB connection
db = AnimalShelter(username, password)

# Load initial data and clean the ObjectID for Dash compatibility
df = pd.DataFrame.from_records(db.read({}))
if not df.empty and '_id' in df.columns:
    df.drop(columns=['_id'], inplace=True)

#########################
# Dashboard Layout / View
#########################
app = dash.Dash(__name__)

# Load branding image locally
image_filename = 'Grazioso Salvare Logo.png'
try:
    with open(image_filename, 'rb') as f:
        encoded_image = base64.b64encode(f.read()).decode()
    img_src = f'data:image/png;base64,{encoded_image}'
except FileNotFoundError:
    img_src = "" 

app.layout = html.Div(style={'fontSize': '18px', 'fontFamily': 'sans-serif'}, children=[
    html.Center(html.B(html.H1('OnlyDogs.com', style={'fontSize': '40px'}))),
    html.Center([
        html.Img(src=img_src, style={'width': '250px'}),
        html.P("Dashboard by: Cody Stuart", style={'fontSize': '20px', 'fontWeight': 'bold'})
    ]),
    html.Hr(),
    
    # Filter selection for specific rescue types
    dcc.RadioItems(
        id='filter-type',
        options=[
            {'label': 'Water Rescue', 'value': 'water'},
            {'label': 'Mountain or Wilderness Rescue', 'value': 'mountain'},
            {'label': 'Disaster Rescue or Individual Tracking', 'value': 'disaster'},
            {'label': 'Reset', 'value': 'reset'}
        ],
        value='reset',
        labelStyle={'display': 'inline-block', 'margin-right': '20px', 'fontSize': '20px'}
    ),
    html.Hr(),
    
    dash_table.DataTable(
        id='datatable-id',
        columns=[
            {"name": "Animal ID", "id": "animal_id"},
            {"name": "Name", "id": "name"},
            {"name": "Breed", "id": "breed"},
            {"name": "Age (Weeks)", "id": "age_upon_outcome_in_weeks"},
            {"name": "Sex", "id": "sex_upon_outcome"},
            {"name": "Outcome", "id": "outcome_type"}
        ],
        style_cell={'fontSize': '16px', 'fontFamily': 'sans-serif', 'padding': '10px'},
        style_header={'backgroundcolor': 'rgb(230,230,230)', 'fontWeight': 'bold', 'fontSize': '18px'},
        data=df.to_dict('records'),
        page_size=10,
        row_selectable="single",
        selected_rows=[0],
        filter_action="native",
        sort_action="native"
    ),
    
    html.Div(style={'display': 'flex'}, children=[
        html.Div(id='graph-id', style={'flex': '1'}),
        html.Div(id='map-id', style={'flex': '1'}),
        html.Div(id='hist-id', style={'flex': '1'})
    ])
])

#############################################
# Controller / Callbacks
#############################################
@app.callback(Output('datatable-id', 'data'), [Input('filter-type', 'value')])
def update_dashboard(filter_type):
    if filter_type == 'reset':
        data = db.read({})
    else:
        data = db.read_rescue(filter_type)

    dff = pd.DataFrame.from_records(data)
    if not dff.empty and '_id' in dff.columns:
        dff.drop(columns=['_id'], inplace=True)
    return dff.to_dict('records')

@app.callback(Output('graph-id', 'children'), [Input('datatable-id', 'derived_virtual_data')])
def update_graphs(viewData):
    if not viewData: return []
    dff = pd.DataFrame(viewData)
    fig = px.pie(dff, names='breed', title='Breed Distribution')
    return [dcc.Graph(figure=fig)]

@app.callback(Output('map-id', 'children'), 
              [Input('datatable-id', 'derived_virtual_data'), 
               Input('datatable-id', 'derived_virtual_selected_rows')])
def update_map(viewData, index):
    if not viewData or index is None: return []
    dff = pd.DataFrame(viewData)

    if dff.empty:
        return [dl.Map(style={'height': '400px'}, center=[30.75, -97.48], zoom=10, children=[dl.TileLayer()])]
    row = index[0] if index else 0

    lat = dff.iloc[row]['location_lat']
    long = dff.iloc[row]['location_long']
    animal_name = dff.iloc[row]['name']
    breed_name = dff.iloc[row]['breed']

    return [
        dl.Map(style={'height': '400px'},
               center=[lat,long], zoom=12, children=[
                dl.TileLayer(),
                dl.Marker(position=[lat,long],
                          children=[
                              dl.Tooltip(breed_name),
                              dl.Popup([
                                  html.H3("Animal Name"),
                                  html.P(animal_name)
                              ])
                          ])
            ])
    ]
    """
    # Center map on the animal's coordinates
    return [dl.Map(style={'height': '400px'}, center=[30.75, -97.48], zoom=10, children=[
        dl.TileLayer(),
        dl.Marker(position=[dff.iloc[row, 13], dff.iloc[row, 14]], children=[
            dl.Tooltip(dff.iloc[row, 4]),
            dl.Popup([html.H3(dff.iloc[row, 9])])
        ])
    ])]
    """

if __name__ == "__main__":
    app.run()
```