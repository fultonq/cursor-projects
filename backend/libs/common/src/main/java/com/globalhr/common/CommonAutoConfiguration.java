package com.globalhr.common;

import com.globalhr.common.web.IsolationHeadersFilter;
import org.springframework.boot.autoconfigure.AutoConfiguration;
import org.springframework.boot.autoconfigure.condition.ConditionalOnWebApplication;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;

@AutoConfiguration
@ConditionalOnWebApplication(type = ConditionalOnWebApplication.Type.SERVLET)
public class CommonAutoConfiguration {

    @Bean
    FilterRegistrationBean<IsolationHeadersFilter> isolationHeadersFilter() {
        FilterRegistrationBean<IsolationHeadersFilter> bean = new FilterRegistrationBean<>(new IsolationHeadersFilter());
        bean.setOrder(IsolationHeadersFilter.ORDER);
        return bean;
    }
}
