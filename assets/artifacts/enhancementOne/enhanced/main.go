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
