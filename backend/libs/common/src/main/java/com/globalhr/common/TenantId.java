package com.globalhr.common;

public record TenantId(String value) {
    public TenantId {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("tenantId required");
        }
    }

    @Override
    public String toString() {
        return value;
    }
}
