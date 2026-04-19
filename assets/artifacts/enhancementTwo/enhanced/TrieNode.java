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

