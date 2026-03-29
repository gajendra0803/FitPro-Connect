package com.GajendraDewangan.Equipment_Rental_Spring.services.auth;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import com.GajendraDewangan.Equipment_Rental_Spring.Enums.UserRole;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.SignupRequest;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.UserDto;
import com.GajendraDewangan.Equipment_Rental_Spring.entity.User;
import com.GajendraDewangan.Equipment_Rental_Spring.repository.UserRepository;

import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService {
    private final UserRepository userRepository;
   

    @PostConstruct
    public void createAdminAccount(){
        User adminAccount = userRepository.findByUserRole(UserRole.ADMIN);
        if (adminAccount == null) {
            User newAdminAccount = new User();
            newAdminAccount.setName("Admin");
            newAdminAccount.setEmail("admin@test.com");
            newAdminAccount.setPassword(new BCryptPasswordEncoder().encode("admin"));
            newAdminAccount.setUserRole(UserRole.ADMIN);
            userRepository.save(newAdminAccount);
            System.err.println("Admin account created successfully");
        }
    }

    @Override
    public UserDto createCustomer(SignupRequest signupRequest){

        User user= new User();
        user.setName(signupRequest.getName());
        user.setEmail(signupRequest.getEmail());
        user.setPassword(new BCryptPasswordEncoder().encode(signupRequest.getPassword()));
        user.setUserRole(UserRole.CUSTOMER);
        User createdUser = userRepository.save(user);
        UserDto userDto = new UserDto();
        userDto.setId(createdUser.getId());
        
        return userDto;
    }

    @Override
    public boolean hasCustomerwithEmail(String email){
        return userRepository.findFirstByEmail(email).isPresent();
    }

}
