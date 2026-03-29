package com.GajendraDewangan.Equipment_Rental_Spring.dto;

import org.springframework.web.multipart.MultipartFile;

import lombok.Data;

@Data
public class EquipmentDto {
    private long id;
    private String brand;
    private String name;
    private String type;
    private String description;
    private Long price;
    private MultipartFile image;
    private byte[] returnedImage;




}
