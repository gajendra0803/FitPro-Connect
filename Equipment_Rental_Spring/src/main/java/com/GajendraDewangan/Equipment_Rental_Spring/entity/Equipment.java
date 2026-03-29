package com.GajendraDewangan.Equipment_Rental_Spring.entity;

import com.GajendraDewangan.Equipment_Rental_Spring.dto.EquipmentDto;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Lob;
import jakarta.persistence.Table;
import lombok.Data;

@Entity
@Data
@Table(name= "equipments")
public class Equipment {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;

    private String brand;

    private String name;

    private String type;

    private String description;

    private Long price;

    @Lob
    @Column(columnDefinition = "longblob")
    private byte[] image;

    public EquipmentDto getEquipmentDto(){
        EquipmentDto equipmentDto = new EquipmentDto();
        equipmentDto.setId(id);
        equipmentDto.setName(name);
        equipmentDto.setBrand(brand);
        equipmentDto.setPrice(price);
        equipmentDto.setDescription(description);
        equipmentDto.setType(type);
        equipmentDto.setReturnedImage(image);
        return equipmentDto;

    }



}
