package com.GajendraDewangan.Equipment_Rental_Spring.controller;

import java.util.Optional;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.DisabledException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.GajendraDewangan.Equipment_Rental_Spring.dto.UserDto;
import com.GajendraDewangan.Equipment_Rental_Spring.repository.UserRepository;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.AuthenticationRequest;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.AuthenticationResponse;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.SignupRequest;
import com.GajendraDewangan.Equipment_Rental_Spring.entity.User;
import com.GajendraDewangan.Equipment_Rental_Spring.services.auth.AuthService;
import com.GajendraDewangan.Equipment_Rental_Spring.services.jwt.UserService;
import com.GajendraDewangan.Equipment_Rental_Spring.utils.JWTUtil;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor

public class AuthController {
    private final AuthService authService;
    private final AuthenticationManager authenticationManager;
    private final UserService userService;
    private final UserRepository userRepository;
    private final JWTUtil jwtUtil;

    @PostMapping("/signup")
    public ResponseEntity<?> signupCustomer(@RequestBody SignupRequest signupRequest){
       if (authService.hasCustomerwithEmail(signupRequest.getEmail())) {
        return new ResponseEntity<>("Customer Already Exist with this email",HttpStatus.NOT_ACCEPTABLE);
        
       }

       UserDto createdCustomerDto = authService.createCustomer(signupRequest);
       if (createdCustomerDto == null)return new ResponseEntity<>("Customer not created, come again Later",HttpStatus.BAD_REQUEST);
       return new ResponseEntity<>(createdCustomerDto,HttpStatus.CREATED) ;

    }

    @PostMapping("/login")
    public AuthenticationResponse createAuthenticationToken(@RequestBody AuthenticationRequest  authenticationRequest) throws
            BadCredentialsException,
            DisabledException,
            UsernameNotFoundException {

        try {
            authenticationManager.authenticate(new UsernamePasswordAuthenticationToken(
                       authenticationRequest.getEmail(),
                       authenticationRequest.getPassword()
                )
            );
        } catch (BadCredentialsException e) {
            throw new BadCredentialsException("Incorrect username or password.");
        }

        final UserDetails userDetails = userService.userDetailsService()
            .loadUserByUsername(authenticationRequest.getEmail());

        Optional<User> optionalUser = userRepository.findFirstByEmail(userDetails.getUsername());

        final String jwt = jwtUtil.generateToken(userDetails);
        AuthenticationResponse authenticationResponse = new AuthenticationResponse();

        if (optionalUser.isPresent()) {
            authenticationResponse.setJwt(jwt);
            authenticationResponse.setUserId(optionalUser.get().getId());
            authenticationResponse.setUserRole(optionalUser.get().getUserRole());
        }

        return authenticationResponse;
    }


}
