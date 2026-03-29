package com.GajendraDewangan.Equipment_Rental_Spring.services.Customer;

import java.util.List;
import java.util.Optional;
import java.util.concurrent.TimeUnit;
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
import com.GajendraDewangan.Equipment_Rental_Spring.entity.User;
import com.GajendraDewangan.Equipment_Rental_Spring.repository.BookAEquipmentRepository;
import com.GajendraDewangan.Equipment_Rental_Spring.repository.EquipmentRepository;
import com.GajendraDewangan.Equipment_Rental_Spring.repository.UserRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class CustomerServiceImpl implements CustomerService{

    private final EquipmentRepository equipmentRepository;
    private final UserRepository userRepository;
    private final BookAEquipmentRepository bookAEquipmentRepository;

    @Override
    public List<EquipmentDto> getAllEquipments(){
        return equipmentRepository.findAll().stream().map(Equipment::getEquipmentDto).collect(Collectors.toList());
    }

    @Override 
    public boolean bookAEquipment(BookAEquipmentDto bookAEquipmentDto){
        Optional<Equipment> optionalEquipment = equipmentRepository.findById(bookAEquipmentDto.getEquipmentId());
        Optional<User> optionalUser = userRepository.findById(bookAEquipmentDto.getUserId());
        if (optionalEquipment.isPresent() && optionalUser.isPresent()) {
            Equipment existingEquipment = optionalEquipment.get();
            BookAEquipment bookAEquipment = new BookAEquipment();

            bookAEquipment.setFromDate(bookAEquipmentDto.getFromDate());
            bookAEquipment.setToDate(bookAEquipmentDto.getToDate());

            bookAEquipment.setUser(optionalUser.get());
            bookAEquipment.setEquipment(existingEquipment);
            bookAEquipment.setBookEquipmentStatus(BookEquipmentStatus.PENDING);
            long diffInMilliSeconds = bookAEquipmentDto.getToDate().getTime() - bookAEquipmentDto.getFromDate().getTime();
            long days = TimeUnit.MILLISECONDS.toDays(diffInMilliSeconds);
            bookAEquipment.setDays(days);
            bookAEquipment.setPrice(existingEquipment.getPrice() *days);
            bookAEquipmentRepository.save(bookAEquipment);
            return true;
        }
        
        return false;
    }


    @Override
    public EquipmentDto getEquipmentById(Long equipmentId){
        Optional<Equipment> optionalEquipment = equipmentRepository.findById(equipmentId);
        return optionalEquipment.map(Equipment::getEquipmentDto).orElse(null);
    }

    @Override
    public List<BookAEquipmentDto> getBookingsByUserId(Long userId){
        return bookAEquipmentRepository.findAllByUserId(userId).stream().map(BookAEquipment::getBookAEquipmentDto).collect(Collectors.toList());
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
