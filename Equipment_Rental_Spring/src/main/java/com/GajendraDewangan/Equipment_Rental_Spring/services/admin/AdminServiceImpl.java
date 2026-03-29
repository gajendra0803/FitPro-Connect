package com.GajendraDewangan.Equipment_Rental_Spring.services.admin;

import java.io.IOException;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;


import org.springframework.data.domain.Example;
import org.springframework.data.domain.ExampleMatcher;

import org.springframework.stereotype.Service;

import com.GajendraDewangan.Equipment_Rental_Spring.Enums.BookEquipmentStatus;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.BookAEquipmentDto;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.EquipmentDto;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.EquipmentDtoListDto;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.SearchEquipmentDto;
import com.GajendraDewangan.Equipment_Rental_Spring.entity.BookAEquipment;
import com.GajendraDewangan.Equipment_Rental_Spring.entity.Equipment;
import com.GajendraDewangan.Equipment_Rental_Spring.repository.BookAEquipmentRepository;
import com.GajendraDewangan.Equipment_Rental_Spring.repository.EquipmentRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class AdminServiceImpl implements AdminService{

    private final EquipmentRepository equipmentRepository;
    private final BookAEquipmentRepository bookAEquipmentRepository;

    @Override
    public boolean postEquipment(EquipmentDto equipmentDto) throws IOException{
        try {
            Equipment equipment = new Equipment();
            equipment.setName(equipmentDto.getName());
            equipment.setBrand(equipmentDto.getBrand());
            equipment.setPrice(equipmentDto.getPrice());
            equipment.setType(equipmentDto.getType());
            equipment.setDescription(equipmentDto.getDescription());
            equipment.setImage(equipmentDto.getImage().getBytes());
            equipmentRepository.save(equipment);
            return true;
        } 
        catch (Exception e) {
            e.printStackTrace();
            return false;
        }
        

}

    @Override
    public List<EquipmentDto> getAllEquipments(){
        return equipmentRepository.findAll().stream().map(Equipment::getEquipmentDto).collect(Collectors.toList());
    }

    @Override
    public void deleteEquipment(Long id){
        equipmentRepository.deleteById(id);
    }

    @Override
    public EquipmentDto getEquipmentById(Long id){
        Optional<Equipment> optionalEquipment = equipmentRepository.findById(id);
        return optionalEquipment.map(Equipment::getEquipmentDto).orElse(null);
        
    }

    @Override
    public boolean updateEquipment(Long equipmentId, EquipmentDto equipmentDto) throws IOException{
        Optional<Equipment> optionalEquipment = equipmentRepository.findById(equipmentId);
        if (optionalEquipment.isPresent()) {
            Equipment existingEquipment = optionalEquipment.get();
            if (equipmentDto.getImage() != null  && !equipmentDto.getImage().isEmpty()) {
                    existingEquipment.setImage(equipmentDto.getImage().getBytes());
            }
            existingEquipment.setPrice(equipmentDto.getPrice());
            existingEquipment.setType(equipmentDto.getType());
            existingEquipment.setBrand(equipmentDto.getBrand());
            existingEquipment.setDescription(equipmentDto.getDescription());
            existingEquipment.setName(equipmentDto.getName());
            equipmentRepository.save(existingEquipment);
            return true;
        }
        else{
            return false;
        }
    }

    @Override
    public List<BookAEquipmentDto> getBookings(){
        return bookAEquipmentRepository.findAll().stream().map(BookAEquipment::getBookAEquipmentDto).collect(Collectors.toList());
    }

    @Override
    public boolean changeBookingStatus(Long bookingId, String status){

        Optional<BookAEquipment> optionalBookAEquipment = bookAEquipmentRepository.findById(bookingId);

        if (optionalBookAEquipment.isPresent()) {
            BookAEquipment existingBookAEquipment = optionalBookAEquipment.get();
            if (Objects.equals(status, "Approve")) {
                existingBookAEquipment.setBookEquipmentStatus(BookEquipmentStatus.APPROVED);
            }
            else{
                existingBookAEquipment.setBookEquipmentStatus(BookEquipmentStatus.REJECTED);
            }
            bookAEquipmentRepository.save(existingBookAEquipment);
            return true;
        }

        return false;
    }

    @Override
    public EquipmentDtoListDto searchEquipment(SearchEquipmentDto searchEquipmentDto){
        Equipment equipment = new Equipment();
        equipment.setBrand(searchEquipmentDto.getBrand());
        equipment.setType(searchEquipmentDto.getType());
        
        ExampleMatcher exampleMatcher = ExampleMatcher.matchingAll()
            .withMatcher("brand", ExampleMatcher.GenericPropertyMatchers.contains().ignoreCase())
            .withMatcher("type", ExampleMatcher.GenericPropertyMatchers.contains().ignoreCase());
    

        Example<Equipment> equipmentExample = Example.of(equipment, exampleMatcher);
        List<Equipment> equipmentList = equipmentRepository.findAll(equipmentExample);
        System.out.println("Find All:"+equipmentRepository.findAll(equipmentExample));
        EquipmentDtoListDto equipmentDtoListDto = new EquipmentDtoListDto();
        equipmentDtoListDto.setEquipmentDtoList(
            equipmentList.stream().map(Equipment::getEquipmentDto).collect(Collectors.toList())
        );

    
        return equipmentDtoListDto;
    }
    
   
}

