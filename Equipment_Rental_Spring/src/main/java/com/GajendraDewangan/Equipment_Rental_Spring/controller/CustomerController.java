package com.GajendraDewangan.Equipment_Rental_Spring.controller;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.GajendraDewangan.Equipment_Rental_Spring.dto.BookAEquipmentDto;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.EquipmentDto;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.SearchEquipmentDto;
import com.GajendraDewangan.Equipment_Rental_Spring.services.Customer.CustomerService;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/customer")
@RequiredArgsConstructor
public class CustomerController {

    private final CustomerService customerService;

    @GetMapping("/equipments")
    public ResponseEntity<List<EquipmentDto>> getAllEquipments(){
        List<EquipmentDto> equipmentDtoList = customerService.getAllEquipments();
        return ResponseEntity.ok(equipmentDtoList);
    }

    @PostMapping("/equipment/book")
    public ResponseEntity<Void> bookAEquipment(@RequestBody BookAEquipmentDto bookAEquipmentDto){
        boolean success = customerService.bookAEquipment(bookAEquipmentDto);

        if (success) {
            return ResponseEntity.status(HttpStatus.CREATED).build();
        }
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
    }

    @GetMapping("/equipment/{equipmentId}")
    public ResponseEntity<EquipmentDto> getEquipmentById(@PathVariable Long equipmentId){
       EquipmentDto equipmentDto = customerService.getEquipmentById(equipmentId);
       if(equipmentDto == null){
        return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(equipmentDto);
    }

    @GetMapping("/equipment/bookings/{userId}")
    public ResponseEntity <List <BookAEquipmentDto>> getBookingsByUserId(@PathVariable Long userId){
        return ResponseEntity.ok(customerService.getBookingsByUserId(userId));
    }

    @PostMapping("/equipment/search")
    public ResponseEntity<?> searchEquipment(@RequestBody SearchEquipmentDto searchEquipmentDto){
       
        return ResponseEntity.ok(customerService.searchEquipment(searchEquipmentDto));
    }


}
