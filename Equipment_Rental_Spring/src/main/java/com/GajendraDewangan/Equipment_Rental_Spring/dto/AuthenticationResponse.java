package com.GajendraDewangan.Equipment_Rental_Spring.dto;

import com.GajendraDewangan.Equipment_Rental_Spring.Enums.UserRole;

import lombok.Data;

@Data
public class AuthenticationResponse {
    private String jwt;
    private UserRole userRole;
    private Long userId;
}
