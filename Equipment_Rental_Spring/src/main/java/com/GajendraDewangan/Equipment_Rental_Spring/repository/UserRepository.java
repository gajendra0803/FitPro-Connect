package com.GajendraDewangan.Equipment_Rental_Spring.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.GajendraDewangan.Equipment_Rental_Spring.entity.User;
// import java.util.List;
import java.util.Optional;
//import java.util.List;
import com.GajendraDewangan.Equipment_Rental_Spring.Enums.UserRole;



@Repository

public interface UserRepository extends JpaRepository<User,Long> {
    Optional<User> findFirstByEmail(String email);

    User findByUserRole(UserRole userRole);

}
