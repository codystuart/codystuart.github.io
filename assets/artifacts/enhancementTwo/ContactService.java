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
