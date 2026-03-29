package com.GajendraDewangan.Equipment_Rental_Spring.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;


import com.GajendraDewangan.Equipment_Rental_Spring.entity.BookAEquipment;

@Repository
public interface BookAEquipmentRepository extends JpaRepository<BookAEquipment , Long>{
    
     List<BookAEquipment> findAllByUserId(Long userId);
    

}
