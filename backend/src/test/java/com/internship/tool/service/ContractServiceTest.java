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

    @Test
    void getAllPaginated_ShouldReturnPage() {
        Pageable pageable = PageRequest.of(0, 10);
        Page<Contract> emptyPage = new PageImpl<>(Collections.emptyList());
        when(contractRepository.findAll(pageable)).thenReturn(emptyPage);
        Page<Contract> result = contractService.getAllPaginated(pageable);
        assertNotNull(result);
        verify(contractRepository).findAll(pageable);
    }

    @Test
    void getContractById_WhenExists_ShouldReturnContract() {
        Contract contract = new Contract();
        contract.setId(1L);
        when(contractRepository.findById(1L)).thenReturn(Optional.of(contract));
        Contract result = contractService.getContractById(1L);
        assertEquals(1L, result.getId());
    }

    @Test
    void getContractById_WhenNotFound_ShouldThrowException() {
        when(contractRepository.findById(99L)).thenReturn(Optional.empty());
        assertThrows(ResourceNotFoundException.class, () -> contractService.getContractById(99L));
    }

    @Test
    void createContract_WithValidData_ShouldSave() {
        Contract contract = new Contract();
        contract.setContractName("NDA");
        contract.setFileName("nda.pdf");
        when(contractRepository.save(any(Contract.class))).thenReturn(contract);
        Contract saved = contractService.createContract(contract);
        assertNotNull(saved);
        assertEquals("NDA", saved.getContractName());
    }

    @Test
    void createContract_WithNullName_ShouldThrowException() {
        Contract contract = new Contract();
        contract.setFileName("test.pdf");
        assertThrows(InvalidContractException.class, () -> contractService.createContract(contract));
    }

    @Test
    void createContract_WithEmptyName_ShouldThrowException() {
        Contract contract = new Contract();
        contract.setContractName(" ");
        contract.setFileName("test.pdf");
        assertThrows(InvalidContractException.class, () -> contractService.createContract(contract));
    }

    @Test
    void createContract_WithNullFile_ShouldThrowException() {
        Contract contract = new Contract();
        contract.setContractName("Name");
        assertThrows(InvalidContractException.class, () -> contractService.createContract(contract));
    }

    @Test
    void createContract_WithEmptyFile_ShouldThrowException() {
        Contract contract = new Contract();
        contract.setContractName("Name");
        contract.setFileName("");
        assertThrows(InvalidContractException.class, () -> contractService.createContract(contract));
    }

    @Test
    void createContract_ShouldCallRepositorySaveOnce() {
        Contract contract = new Contract();
        contract.setContractName("Test");
        contract.setFileName("test.pdf");
        when(contractRepository.save(any(Contract.class))).thenReturn(contract);
        contractService.createContract(contract);
        verify(contractRepository, times(1)).save(any(Contract.class));
    }

    @Test
    void getAllPaginated_WithContent_ShouldReturnPopulatedPage() {
        Pageable pageable = PageRequest.of(0, 10);
        Contract contract = new Contract();
        contract.setContractName("Populated");
        Page<Contract> page = new PageImpl<>(Collections.singletonList(contract));
        when(contractRepository.findAll(pageable)).thenReturn(page);
        Page<Contract> result = contractService.getAllPaginated(pageable);
        assertFalse(result.getContent().isEmpty());
    }
}