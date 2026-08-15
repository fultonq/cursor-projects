package com.globalhr.common;

public record CorrelationId(String value) {
    public CorrelationId {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("correlationId required");
        }
    }

    @Override
    public String toString() {
        return value;
    }
}
