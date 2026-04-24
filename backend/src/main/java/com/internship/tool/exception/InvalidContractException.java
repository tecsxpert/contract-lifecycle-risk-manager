package com.internship.tool.exception;

// Requirement: Custom exception classes for each error type
public class InvalidContractException extends RuntimeException {
    public InvalidContractException(String message) {
        super(message);
    }
}