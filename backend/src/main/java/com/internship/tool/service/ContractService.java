package com.internship.tool.service;

import com.internship.tool.entity.Contract;
import com.internship.tool.exception.InvalidContractException;
import com.internship.tool.exception.ResourceNotFoundException;
import com.internship.tool.repository.ContractRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class ContractService {

    private final ContractRepository contractRepository;

    /**
     * Requirement: GET /all must be paginated
     * Redis Cache Key ensures page 0 and page 1 are stored separately
     */
    @Cacheable(value = "contracts", key = "#pageable.pageNumber + '-' + #pageable.pageSize")
    public Page<Contract> getAllPaginated(Pageable pageable) {
        return contractRepository.findAll(pageable);
    }

    @Cacheable(value = "contracts", key = "#id")
    public Contract getContractById(Long id) {
        return contractRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Contract not found with id: " + id));
    }

    /**
     * Requirement: Service layer business logic & input validation [cite: 67]
     */
    @CacheEvict(value = "contracts", allEntries = true)
    public Contract createContract(Contract contract) {
        validateContractName(contract.getContractName());
        validateFileName(contract.getFileName());
        return contractRepository.save(contract);
    }

    private void validateContractName(String contractName) {
        if (contractName == null || contractName.trim().isEmpty()) {
            throw new InvalidContractException("Contract name cannot be empty");
        }
        validateInjectionPatterns(contractName, "contract name");
    }

    private void validateFileName(String fileName) {
        if (fileName == null || fileName.trim().isEmpty()) {
            throw new InvalidContractException("File name is required");
        }
        validateInjectionPatterns(fileName, "file name");
    }

    private void validateInjectionPatterns(String value, String fieldName) {
        String normalized = value.trim().toLowerCase();
        if (containsSqlInjection(normalized)) {
            throw new InvalidContractException("Potential SQL injection detected in " + fieldName);
        }
        if (containsPromptInjection(normalized)) {
            throw new InvalidContractException("Potential prompt injection detected in " + fieldName);
        }
    }

    private boolean containsSqlInjection(String value) {
        return value.contains("select ")
                || value.contains("union ")
                || value.contains("drop ")
                || value.contains("insert ")
                || value.contains("delete ")
                || value.contains("update ")
                || value.contains("--")
                || value.contains(";")
                || value.contains("' or ")
                || value.contains("\" or ");
    }

    private boolean containsPromptInjection(String value) {
        return value.contains("ignore previous")
                || value.contains("ignore all")
                || value.contains("disregard previous")
                || value.contains("disregard all")
                || value.contains("do not follow instructions")
                || value.contains("dont follow instructions")
                || value.contains("forget previous")
                || value.contains("bypass security")
                || value.contains("prompt injection");
    }
}