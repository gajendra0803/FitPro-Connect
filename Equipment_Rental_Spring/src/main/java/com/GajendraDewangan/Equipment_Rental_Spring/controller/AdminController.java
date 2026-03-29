package com.GajendraDewangan.Equipment_Rental_Spring.controller;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.GajendraDewangan.Equipment_Rental_Spring.dto.BookAEquipmentDto;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.EquipmentDto;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.SearchEquipmentDto;
import com.GajendraDewangan.Equipment_Rental_Spring.services.admin.AdminService;

import lombok.RequiredArgsConstructor;
import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("/api/admin")
@RequiredArgsConstructor
public class AdminController {
    private final AdminService adminService;

    @PostMapping("/equipment")
    public ResponseEntity<?> postEquipment(@ModelAttribute EquipmentDto equipmentDto) throws IOException{

        boolean success = adminService.postEquipment(equipmentDto);
        if (success) {
            return ResponseEntity.status(HttpStatus.CREATED).build();
        }else{
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        }
    }
    
    @GetMapping("/equipments")
    public ResponseEntity<?> getAllEquipments(){
        return ResponseEntity.ok(adminService.getAllEquipments());
    }

    @DeleteMapping("/equipment/{id}")
    public ResponseEntity<Void> deleteEquipment(@PathVariable Long id){
        adminService.deleteEquipment(id);
        return ResponseEntity.ok(null);
    } 

    @GetMapping("/equipment/{id}")
    public ResponseEntity<EquipmentDto> getEquipmentById(@PathVariable Long id){
        EquipmentDto equipmentDto = adminService.getEquipmentById(id);
        return ResponseEntity.ok(equipmentDto);
    }

    @PutMapping("/equipment/{equipmentId}")
    public ResponseEntity<Void> updateEquipment(@PathVariable Long equipmentId, @ModelAttribute EquipmentDto equipmentDto) throws IOException{

        try {
            boolean success = adminService.updateEquipment(equipmentId, equipmentDto);
            if (success) {
                return ResponseEntity.status(HttpStatus.OK).build();
            }else{
                return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
            }
    
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        }
    }

    @GetMapping("/equipment/bookings")
    public ResponseEntity<List<BookAEquipmentDto>> getBookings(){
        return ResponseEntity.ok(adminService.getBookings());
        
    }

    @GetMapping("/equipment/booking/{bookingId}/{status}")
    public ResponseEntity<?> changeBookingStatus(@PathVariable  Long bookingId, @PathVariable String status){
        boolean success = adminService.changeBookingStatus(bookingId, status);
        if (success) {
            return ResponseEntity.ok().build();
        }else{
            return ResponseEntity.notFound().build();
        
        }
    }

    @PostMapping("/equipment/search")
    public ResponseEntity<?> searchEquipment(@RequestBody SearchEquipmentDto searchEquipmentDto){
       
        return ResponseEntity.ok(adminService.searchEquipment(searchEquipmentDto));
    }
}
