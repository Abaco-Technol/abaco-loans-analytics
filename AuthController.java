package com.abaco.loans.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
public class AuthController {

    private static final Logger logger = LoggerFactory.getLogger(AuthController.class);

    /**
     * Handles the OAuth 2.0 callback from the identity provider.
     *
     * @param code  The authorization code provided by the identity provider.
     * @param state The state parameter for CSRF protection.
     * @return A response entity indicating the result of the authentication process.
     */
    @GetMapping("/auth-callback")
    public ResponseEntity<Map<String, String>> handleAuthCallback(@RequestParam("code") String code, @RequestParam("state") String state) {
        logger.info("Received OAuth 2.0 callback. State: {}, Code length: {}", state, code.length());

        // 1. **STATE VERIFICATION (CRITICAL):** Compare the received 'state' with the one stored in the user's session.
        //    This is a critical security step to prevent CSRF attacks.
        // 2. **CODE-FOR-TOKEN EXCHANGE:** Make a server-to-server POST request to the identity provider's token endpoint,
        //    exchanging the 'code' for an access_token and id_token. This requires client_id and client_secret.
        // 3. **SESSION CREATION:** Upon successful token exchange, create a user session and redirect to the application's dashboard.

        return ResponseEntity.ok(Map.of("status", "Callback received", "action", "Proceed with token exchange"));
    }
}