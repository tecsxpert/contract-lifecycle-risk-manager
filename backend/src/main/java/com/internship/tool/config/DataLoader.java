package com.internship.tool.config;

import com.internship.tool.entity.Contract;
import com.internship.tool.repository.ContractRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Component
public class DataLoader implements CommandLineRunner {

    private final ContractRepository contractRepository;

    public DataLoader(ContractRepository contractRepository) {
        this.contractRepository = contractRepository;
    }

    @Override
    public void run(String... args) throws Exception {
        if (contractRepository.count() == 0) {
            List<Contract> contracts = new ArrayList<>();

            // 1. Manually defined records for the Demo Day walkthrough
            contracts.add(Contract.builder()
                    .contractName("High-Risk Vendor Agreement")
                    .vendorName("TechCorp Solutions")
                    .status("Pending Review")
                    .riskScore(8.5)
                    .fileName("techcorp_v1.pdf")
                    .build());

            contracts.add(Contract.builder()
                    .contractName("Standard Service SLA")
                    .vendorName("BlueSky Logistics")
                    .status("Active")
                    .riskScore(2.0)
                    .fileName("sla_bluesky.pdf")
                    .build());

            // 2. Loop to generate a total of 30 records for pagination/charts
            String[] vendors = {"CloudStream", "DataNexus", "SafeGuard", "AlphaRetail", "OmniLogic"};
            String[] statuses = {"Draft", "Pending Review", "Active", "Expired"};

            for (int i = 1; i <= 28; i++) {
                contracts.add(Contract.builder()
                        .contractName("Contract #" + (100 + i))
                        .vendorName(vendors[i % vendors.length])
                        .status(statuses[i % statuses.length])
                        .riskScore((double) (i % 10))
                        .fileName("document_" + i + ".pdf")
                        .build());
            }

            contractRepository.saveAll(contracts);
            System.out.println(">> Day 12: Successfully seeded 30 records into the 'contracts' table.");
        }
    }
}