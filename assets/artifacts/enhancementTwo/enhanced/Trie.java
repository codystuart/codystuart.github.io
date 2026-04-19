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
