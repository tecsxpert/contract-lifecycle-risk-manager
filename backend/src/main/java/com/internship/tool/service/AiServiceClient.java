package com.internship.tool.service;

import java.util.HashMap;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpStatusCodeException;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestTemplate;

@Service
public class AiServiceClient {

    private static final Logger logger = LoggerFactory.getLogger(AiServiceClient.class);
    private static final int TIMEOUT_MILLIS = 10_000;
    private static final String DEFAULT_BASE_URL = "http://localhost:5000";

    private final RestTemplate restTemplate;
    private final String baseUrl;

    public AiServiceClient() {
        this(DEFAULT_BASE_URL);
    }

    public AiServiceClient(String baseUrl) {
        this.baseUrl = baseUrl;
        SimpleClientHttpRequestFactory requestFactory = new SimpleClientHttpRequestFactory();
        requestFactory.setConnectTimeout(TIMEOUT_MILLIS);
        requestFactory.setReadTimeout(TIMEOUT_MILLIS);
        this.restTemplate = new RestTemplate(requestFactory);
    }

    public Map<String, Object> sendPrompt(String prompt) {
        if (prompt == null) {
            logger.warn("sendPrompt called with null prompt");
            return null;
        }

        String endpoint = baseUrl + "/api/prompt";
        Map<String, String> payload = new HashMap<>();
        payload.put("prompt", prompt);

        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, String>> request = new HttpEntity<>(payload, headers);
            ResponseEntity<Map> response = restTemplate.postForEntity(endpoint, request, Map.class);
            if (response.getStatusCode().is2xxSuccessful()) {
                return response.getBody();
            }
            logger.error("AiService returned non-success status {} for {}", response.getStatusCode(), endpoint);
        } catch (HttpStatusCodeException ex) {
            logger.error("AiService HTTP error calling {}: {} - {}", endpoint, ex.getStatusCode(), ex.getResponseBodyAsString(), ex);
        } catch (ResourceAccessException ex) {
            logger.error("AiService request timed out or could not connect to {}: {}", endpoint, ex.getMessage(), ex);
        } catch (Exception ex) {
            logger.error("Unexpected error sending prompt to AiService at {}: {}", endpoint, ex.getMessage(), ex);
        }
        return null;
    }

    public Map<String, Object> callEndpoint(String endpointPath, Map<String, Object> payload) {
        if (endpointPath == null || endpointPath.isBlank()) {
            logger.warn("callEndpoint called with blank path");
            return null;
        }

        String endpoint = baseUrl + endpointPath;
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> request = new HttpEntity<>(payload, headers);
            ResponseEntity<Map> response = restTemplate.postForEntity(endpoint, request, Map.class);
            if (response.getStatusCode().is2xxSuccessful()) {
                return response.getBody();
            }
            logger.error("AiService returned non-success status {} for {}", response.getStatusCode(), endpoint);
        } catch (HttpStatusCodeException ex) {
            logger.error("AiService HTTP error calling {}: {} - {}", endpoint, ex.getStatusCode(), ex.getResponseBodyAsString(), ex);
        } catch (ResourceAccessException ex) {
            logger.error("AiService request timed out or could not connect to {}: {}", endpoint, ex.getMessage(), ex);
        } catch (Exception ex) {
            logger.error("Unexpected error calling AiService endpoint {}: {}", endpoint, ex.getMessage(), ex);
        }
        return null;
    }
}
