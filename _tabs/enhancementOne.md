---
layout: page
title: Software Design and Engineering Enhancement
icon: fas fa-stream
order: 2
---

## Narrative
The artifact in question is a C++ file designed to showcase XOR bitwise encryption. It was originally completed for the Secure Coding course during the 2026 January to March term. The original artifact takes in an input file, extracts some information from said file, then encrypts the file, and decrypts the file to very symmetric properties of XOR. 
I selected this artifact for my ePortfolio because I wanted to showcase my ability to learn a new language and convert pre-existing code to that new language. I rather enjoy C++ and it’s certainly a useful language, but there are new languages like Golang which have different uses and efficiencies. I made a few improvements from the original artifact. For starters I felt that the encryption key being the hardcoded word “password” was not secure enough, so I created a function designed to generate a cryptographically secure key at runtime. Choosing Golang also adds memory safety to the code as an improvement. This enhancement showcases language refactoring, advanced programming with the use of Golangs byte slices and struct-based composition, and quality assurance with Go’s error handling for I/O.
With this code refactor I believe I met outcomes 4 and 5. I demonstrated an ability to use well-founded and innovative techniques by transitioning to a modern memory safe language, with a new architecture. I also successfully developed a security mindset by replacing the vulnerable hardcoded key. 
I learned the importance of working with immutability in Go. Unlike C++ where strings are easily manipulated in place, Go requires working with byte slices for bitwise operations, which is a safer and more efficient approach to data transformation. One primary challenge was replicating the specific C++ file-parsing logic in Go. I initially struggled with the getStudentName function returning a null value because I was parsing the actual filename rather than the contents of the actual file. I overcame this by debugging the pos and studentName variables which led me to realize my error.

---

## Original

<p style="text-indent: 50px; font-style: italic;">
Encryption.cpp takes an input data file which is in plain-text extrapolates information, then using XOR bitwise encryption encrypts the file with plain-text header information, and then decrypts the file with the same plain-text header information outputting each into a file to be compared.
</p>

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

---
## Enhanced

<p style="text-indent: 50px; font-style: italic;">
This file named main.go performs similar functionality to the above Encryption.cpp it was converted from. In addition to the original functionality, I've implemented a cryptographically secure key generated at runtime. In a professional environment the key would be offloaded to an external source such as Hashicorp vault, but in the scope of this project it is output with the created files.
</p>

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

