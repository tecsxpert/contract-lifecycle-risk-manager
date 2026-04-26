package com.internship.tool.service;

import com.internship.tool.entity.Contract;
import com.internship.tool.exception.InvalidContractException;
import com.internship.tool.exception.ResourceNotFoundException;
import com.internship.tool.repository.ContractRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;

import java.util.Collections;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class ContractServiceTest {

    @Mock
    private ContractRepository contractRepository;

    @InjectMocks
    private ContractService contractService;

    // 1. Success Path: Get All Paginated (Supports Empty States)
    @Test
    void getAllPaginated_ShouldReturnPage() {
        Pageable pageable = PageRequest.of(0, 10);
        Page<Contract> emptyPage = new PageImpl<>(Collections.emptyList());
        when(contractRepository.findAll(pageable)).thenReturn(emptyPage);

        Page<Contract> result = contractService.getAllPaginated(pageable);

        assertNotNull(result);
        assertTrue(result.getContent().isEmpty());
        verify(contractRepository, times(1)).findAll(pageable);
    }

    // 2. Success Path: Get by ID
    @Test
    void getContractById_WhenExists_ShouldReturnContract() {
        Contract contract = new Contract();
        contract.setId(1L);
        when(contractRepository.findById(1L)).thenReturn(Optional.of(contract));

        Contract result = contractService.getContractById(1L);

        assertNotNull(result);
        assertEquals(1L, result.getId());
    }

    // 3. Exception Path: Resource Not Found (Day 11 Requirement)
    @Test
    void getContractById_WhenNotFound_ShouldThrowException() {
        when(contractRepository.findById(99L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> contractService.getContractById(99L));
    }

    // 4. Success Path: Create Contract
    @Test
    void createContract_WithValidData_ShouldSave() {
        Contract contract = new Contract();
        contract.setContractName("Service Agreement");
        contract.setFileName("contract.pdf");
        when(contractRepository.save(any(Contract.class))).thenReturn(contract);

        Contract saved = contractService.createContract(contract);

        assertNotNull(saved);
        assertEquals("Service Agreement", saved.getContractName());
    }

    // 5-6. Exception Path: Validation Failures (Day 11 UX Polish)
    @Test
    void createContract_WithNullName_ShouldThrowException() {
        Contract contract = new Contract();
        contract.setFileName("test.pdf");
        assertThrows(InvalidContractException.class, () -> contractService.createContract(contract));
    }

    @Test
    void createContract_WithEmptyName_ShouldThrowException() {
        Contract contract = new Contract();
        contract.setContractName("   ");
        contract.setFileName("test.pdf");
        assertThrows(InvalidContractException.class, () -> contractService.createContract(contract));
    }

    // 7-8. Exception Path: File Name Validations
    @Test
    void createContract_WithNullFile_ShouldThrowException() {
        Contract contract = new Contract();
        contract.setContractName("Valid Name");
        assertThrows(InvalidContractException.class, () -> contractService.createContract(contract));
    }

    @Test
    void createContract_WithEmptyFile_ShouldThrowException() {
        Contract contract = new Contract();
        contract.setContractName("Valid Name");
        contract.setFileName("");
        assertThrows(InvalidContractException.class, () -> contractService.createContract(contract));
    }

    // 9. Edge Case: Verify Repository Call Count
    @Test
    void createContract_ShouldCallRepositorySaveOnce() {
        Contract contract = new Contract();
        contract.setContractName("Audit Test");
        contract.setFileName("audit.pdf");
        when(contractRepository.save(any(Contract.class))).thenReturn(contract);

        contractService.createContract(contract);

        verify(contractRepository, times(1)).save(any(Contract.class));
    }

    // 10. Success Path: Verify Page with Content
    @Test
    void getAllPaginated_WithContent_ShouldReturnPopulatedPage() {
        Pageable pageable = PageRequest.of(0, 10);
        Contract contract = new Contract();
        contract.setContractName("Populated");
        Page<Contract> page = new PageImpl<>(Collections.singletonList(contract));

        when(contractRepository.findAll(pageable)).thenReturn(page);

        Page<Contract> result = contractService.getAllPaginated(pageable);

        assertFalse(result.getContent().isEmpty());
        assertEquals("Populated", result.getContent().get(0).getContractName());
    }
}