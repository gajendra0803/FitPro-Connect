package com.GajendraDewangan.Equipment_Rental_Spring.services.admin;

import java.io.IOException;
import java.util.List;

import com.GajendraDewangan.Equipment_Rental_Spring.dto.BookAEquipmentDto;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.EquipmentDto;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.EquipmentDtoListDto;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.SearchEquipmentDto;

public interface AdminService {

    boolean postEquipment(EquipmentDto equipmentDto) throws IOException;

    List<EquipmentDto> getAllEquipments();

    void deleteEquipment(Long id);

    EquipmentDto getEquipmentById(Long id);

    boolean updateEquipment(Long equipmentId, EquipmentDto equipmentDto) throws IOException;

    List<BookAEquipmentDto> getBookings();

    boolean changeBookingStatus(Long bookingId,String status);

    EquipmentDtoListDto searchEquipment(SearchEquipmentDto searchEquipmentDto);

}
