package com.globalhr.common.context;

import com.globalhr.common.CorrelationId;
import com.globalhr.common.RegionCode;
import com.globalhr.common.TenantId;

public final class TenantContext {

    private static final ThreadLocal<TenantId> TENANT = new ThreadLocal<>();
    private static final ThreadLocal<RegionCode> REGION = new ThreadLocal<>();
    private static final ThreadLocal<CorrelationId> CORRELATION = new ThreadLocal<>();

    private TenantContext() {}

    public static void set(TenantId tenant, RegionCode region, CorrelationId correlation) {
        TENANT.set(tenant);
        REGION.set(region);
        CORRELATION.set(correlation);
    }

    public static TenantId tenant() {
        return TENANT.get();
    }

    public static RegionCode region() {
        return REGION.get();
    }

    public static CorrelationId correlation() {
        return CORRELATION.get();
    }

    public static void clear() {
        TENANT.remove();
        REGION.remove();
        CORRELATION.remove();
    }
}
