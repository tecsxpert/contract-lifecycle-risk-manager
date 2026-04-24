package com.internship.tool.controller;

import com.internship.tool.entity.Contract;
import com.internship.tool.service.ContractService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page; // Added
import org.springframework.data.domain.PageRequest; // Added
import org.springframework.data.domain.Pageable; // Added
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/contracts")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class ContractController {

    private final ContractService contractService;

    /**
     * Requirement: GET /all must be paginated (Day 4/7)
     * URL Example: http://localhost:8080/api/contracts?page=0&size=10
     */
    @GetMapping
    @PreAuthorize("hasAnyRole('USER', 'ADMIN')")
    public ResponseEntity<Page<Contract>> getAllContracts(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {

        Pageable pageable = PageRequest.of(page, size);
        return ResponseEntity.ok(contractService.getAllPaginated(pageable));
    }

    @GetMapping("/{id}")
    @PreAuthorize("hasAnyRole('USER', 'ADMIN')")
    public ResponseEntity<Contract> getContractById(@PathVariable Long id) {
        return ResponseEntity.ok(contractService.getContractById(id));
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public Contract createContract(@RequestBody Contract contract) {
        return contractService.createContract(contract);
    }
}