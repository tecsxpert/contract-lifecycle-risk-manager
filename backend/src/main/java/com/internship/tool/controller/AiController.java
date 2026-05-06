package com.internship.tool.controller;

import com.internship.tool.service.AiServiceClient;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/ai")
@RequiredArgsConstructor
@CrossOrigin(origins = "http://localhost:3000")
public class AiController {

    private final AiServiceClient aiServiceClient;

    @PostMapping("/prompt")
    public ResponseEntity<Map<String, Object>> sendPrompt(@RequestBody Map<String, String> request) {
        String prompt = request.get("prompt");
        if (prompt == null || prompt.isBlank()) {
            return ResponseEntity.badRequest().body(Map.of("error", "Missing prompt field"));
        }

        Map<String, Object> result = aiServiceClient.sendPrompt(prompt);
        if (result == null) {
            return ResponseEntity.status(502).body(Map.of("error", "AI service unavailable"));
        }
        return ResponseEntity.ok(result);
    }
}
