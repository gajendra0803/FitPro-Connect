package com.GajendraDewangan.Equipment_Rental_Spring.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.GajendraDewangan.Equipment_Rental_Spring.entity.Equipment;

@Repository
public interface EquipmentRepository extends JpaRepository<Equipment, Long>{
    
    

}
