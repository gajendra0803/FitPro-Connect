package com.GajendraDewangan.Equipment_Rental_Spring.services.auth;


import com.GajendraDewangan.Equipment_Rental_Spring.dto.SignupRequest;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.UserDto;

public interface AuthService {
    UserDto createCustomer(SignupRequest signupRequest);

    boolean hasCustomerwithEmail(String email);
   
}
