package com.globalhr.common;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class RegionCodeTest {

    @Test
    void normalizesAndAcceptsSupportedRegions() {
        assertEquals("EMEA", new RegionCode("emea").value());
    }

    @Test
    void rejectsUnknownRegion() {
        assertThrows(IllegalArgumentException.class, () -> new RegionCode("LATAM"));
    }
}
