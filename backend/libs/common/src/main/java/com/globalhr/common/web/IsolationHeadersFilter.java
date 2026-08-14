package com.globalhr.common.web;

import com.globalhr.common.CorrelationId;
import com.globalhr.common.RegionCode;
import com.globalhr.common.TenantId;
import com.globalhr.common.context.TenantContext;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.core.Ordered;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.UUID;

public class IsolationHeadersFilter extends OncePerRequestFilter {

    public static final int ORDER = Ordered.HIGHEST_PRECEDENCE + 10;

    public static final String TENANT = "X-Tenant-Id";
    public static final String REGION = "X-Region";
    public static final String CORRELATION = "X-Correlation-Id";

    @Override
    protected boolean shouldNotFilter(HttpServletRequest request) {
        String path = request.getRequestURI();
        return path.startsWith("/actuator") || path.endsWith("/_ping");
    }

    @Override
    protected void doFilterInternal(
            HttpServletRequest request, HttpServletResponse response, FilterChain chain)
            throws ServletException, IOException {
        String tenant = request.getHeader(TENANT);
        String region = request.getHeader(REGION);
        String correlation = request.getHeader(CORRELATION);
        if (correlation == null || correlation.isBlank()) {
            correlation = UUID.randomUUID().toString();
        }
        response.setHeader(CORRELATION, correlation);
        if (tenant != null && region != null) {
            TenantContext.set(new TenantId(tenant), new RegionCode(region), new CorrelationId(correlation));
        }
        try {
            chain.doFilter(request, response);
        } finally {
            TenantContext.clear();
        }
    }
}
