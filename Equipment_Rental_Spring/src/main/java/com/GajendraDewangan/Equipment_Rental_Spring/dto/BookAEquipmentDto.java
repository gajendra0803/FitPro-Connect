package com.GajendraDewangan.Equipment_Rental_Spring.dto;

import java.util.Date;

import com.GajendraDewangan.Equipment_Rental_Spring.Enums.BookEquipmentStatus;

import lombok.Data;

@Data
public class BookAEquipmentDto {

    private Long id;

    private Date fromDate;

    private Date toDate;

    private Long days;

    private Long price;

    private BookEquipmentStatus bookEquipmentStatus;

    private Long equipmentId;

    private Long userId;

    private String username;

    private String email;

}
