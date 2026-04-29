package com.internship.tool.repository;

import com.internship.tool.entity.Contract;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ContractRepository extends JpaRepository<Contract, Long> {
    // You can add custom query methods here later if needed
}