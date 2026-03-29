package com.GajendraDewangan.Equipment_Rental_Spring.dto;

import com.GajendraDewangan.Equipment_Rental_Spring.Enums.UserRole;

import lombok.Data;

@Data

public class UserDto {

    private long id;

    private String name;

    private String email;

    private UserRole userRole;

}
