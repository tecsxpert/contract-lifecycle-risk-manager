package com.internship.tool.controller;

import com.internship.tool.entity.Contract;
import com.internship.tool.service.ContractService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/contracts")
@RequiredArgsConstructor
@CrossOrigin(origins = "http://localhost:3000") // Restrict CORS for local development
public class ContractController {

    private final ContractService contractService;

    /**
     * Requirement: GET /all must be paginated (Day 4/7)
     * Supports UX Polish: Returns empty content [] instead of error for Empty States.
     */
    @GetMapping
    @PreAuthorize("hasAnyRole('USER', 'ADMIN')")
    public ResponseEntity<Page<Contract>> getAllContracts(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {

        Pageable pageable = PageRequest.of(page, size);
        Page<Contract> contracts = contractService.getAllPaginated(pageable);
        return ResponseEntity.ok(contracts);
    }

    /**
     * Requirement: Standardized JSON Error Boundary support
     * If ID doesn't exist, GlobalExceptionHandler catches the exception.
     */
    @GetMapping("/{id}")
    @PreAuthorize("hasAnyRole('USER', 'ADMIN')")
    public ResponseEntity<Contract> getContractById(@PathVariable Long id) {
        Contract contract = contractService.getContractById(id);
        return ResponseEntity.ok(contract);
    }

    /**
     * Requirement: RESTful Standard Polish
     * Returns 201 Created instead of 200 OK for new records.
     */
    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Contract> createContract(@RequestBody Contract contract) {
        Contract savedContract = contractService.createContract(contract);
        return new ResponseEntity<>(savedContract, HttpStatus.CREATED);
    }
}