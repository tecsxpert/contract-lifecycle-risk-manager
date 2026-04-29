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
        if (contract.getContractName() == null || contract.getContractName().trim().isEmpty()) {
            throw new InvalidContractException("Contract name cannot be empty");
        }

        if (contract.getFileName() == null || contract.getFileName().trim().isEmpty()) {
            throw new InvalidContractException("File name is required");
        }

        return contractRepository.save(contract);
    }
}