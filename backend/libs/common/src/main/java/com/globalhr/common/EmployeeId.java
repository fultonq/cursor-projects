package com.globalhr.common;

public record EmployeeId(String value) {
    public EmployeeId {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("employeeId required");
        }
    }

    @Override
    public String toString() {
        return value;
    }
}
