package com.globalhr.common;

import java.util.Locale;
import java.util.Set;

public record RegionCode(String value) {
    public static final Set<String> SUPPORTED = Set.of("AMER", "EMEA", "APAC");

    public RegionCode {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("region required");
        }
        value = value.toUpperCase(Locale.ROOT);
        if (!SUPPORTED.contains(value)) {
            throw new IllegalArgumentException("unsupported region: " + value);
        }
    }

    @Override
    public String toString() {
        return value;
    }
}
