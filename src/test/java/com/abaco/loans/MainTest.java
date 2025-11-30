package com.abaco.loans;

import com.abaco.loans.controller.AuthController;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
class MainTest {
    @Autowired
    private AuthController authController;

    @Test
    @DisplayName("Application context should load and contain the AuthController")
    void contextLoads() {
        assertThat(authController).isNotNull();
    }
}