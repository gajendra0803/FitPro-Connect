package com.GajendraDewangan.Equipment_Rental_Spring.services.Customer;

import java.util.List;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.BookAEquipmentDto;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.EquipmentDto;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.EquipmentDtoListDto;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.SearchEquipmentDto;

public interface CustomerService {

    List<EquipmentDto> getAllEquipments();

    boolean bookAEquipment(BookAEquipmentDto bookAEquipmentDto);

    EquipmentDto getEquipmentById(Long equipmentId);

    List<BookAEquipmentDto> getBookingsByUserId(Long userId);

    EquipmentDtoListDto searchEquipment(SearchEquipmentDto searchEquipmentDto);

    

}
