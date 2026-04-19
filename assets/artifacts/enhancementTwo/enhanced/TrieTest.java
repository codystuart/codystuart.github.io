package com.stuart.contacts.tests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import com.stuart.contacts.*;
import java.util.List;

class TrieTest {
	private Trie trie;
	private Contact con1;
	private Contact con2;
	
	@BeforeEach
	void setUp() {
		trie = new Trie();
		con1 = new Contact("1", "Cody", "Stuart", "1234567890", "123 Lane");
		con2 = new Contact("2", "Colton", "Smith", "1111222333", "456 Blvd");
	}
	
	@Test
	void testInsertAndPrefixSearch() {
		trie.insert("Cody", con1);
		
		List<Contact> result = trie.search("Co");
		assertEquals(1, result.size());
		assertEquals("Stuart", result.get(0).getLastName());
	}
	
	@Test
	void testMultipleContactsSamePrefix() {
		trie.insert(con1.getFirstName(), con1);
		trie.insert(con2.getFirstName(), con2);
		
		List<Contact> result = trie.search("Co");
		assertEquals(2, result.size());
	}
	
	@Test
    void testCaseInsensitivity() {
        trie.insert("Cody", con1);
        
        // Search with lowercase to verify normalization
        List<Contact> results = trie.search("cody");
        assertFalse(results.isEmpty());
    }

    @Test
    void testSearchNonExistentPrefix() {
        trie.insert("Cody", con1);
        List<Contact> results = trie.search("Z");
        assertTrue(results.isEmpty());
    }

    @Test
    void testInvalidCharactersInSearch() {
        trie.insert("Cody", con1);
        // Verify that symbols don't crash the search logic
        List<Contact> results = trie.search("Co!");
        assertEquals(1, results.size());
    }

}
