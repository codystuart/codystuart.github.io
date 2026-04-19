---
layout: page
title: Algorithms and Data Structures Enhancement
icon: fas fa-stream
order: 3
---

## Narrative

The artifact I’ve chosen to enhance for algorithms and data structures is the ContactService.java file from CS-320 Software Test, Automation, and Quality Assurance. The original artifact was centered around developing java code and using junit to perform unit testing on that code. 
I’ve included this artifact in ePortfolio as I wanted to showcase an ability to find code that can be improved through advanced algorithms and data structures. The original artifact uses a hashmap to store and lookup contacts, in modern applications however this would be missing something, the ability to search for contact names based on a part of a name. The idea of adding a prefix tree to enable partial searching made sense to me as in my cell phone I can search for contact names by only a portion of the name. I also kept the spirit of the original assignment by incorporating unit testing for the Trie system I added. This also helps me ensure that my added code is functioning. 
Through this enhancement I’ve achieved outcomes 3 and 6 by designing a solution that balances the trade-off between increased memory and significantly faster searching. As well including the Trie I’ve met the industry-specific goal of scalable data retrieval. 
What I learned from this enhancement was how to adapt a classic data structure to store complex objects, as well as gaining a deeper understanding of how to maintain data integrity across multiple structures like a hashmap and a trie simultaneously. 

---
## Artifacts

### Original

#### ContactService.java
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

### Enhanced

#### Trie.java
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

#### TrieNode.java
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
