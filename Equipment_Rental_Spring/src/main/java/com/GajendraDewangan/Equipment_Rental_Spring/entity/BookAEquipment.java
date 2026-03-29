package com.GajendraDewangan.Equipment_Rental_Spring.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import lombok.Data;
import java.util.Date;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

import com.GajendraDewangan.Equipment_Rental_Spring.Enums.BookEquipmentStatus;
import com.GajendraDewangan.Equipment_Rental_Spring.dto.BookAEquipmentDto;
import com.fasterxml.jackson.annotation.JsonIgnore;
@Entity
@Data

public class BookAEquipment {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Date fromDate;

    private Date toDate;

    private Long days;

    private Long price;

    private BookEquipmentStatus bookEquipmentStatus;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "user_id", nullable = false)
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JsonIgnore

    private User user;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "equipment_id", nullable = false)
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JsonIgnore

    private Equipment equipment;

    public BookAEquipmentDto getBookAEquipmentDto(){
        BookAEquipmentDto bookAEquipmentDto = new BookAEquipmentDto();
        bookAEquipmentDto.setId(id);
        bookAEquipmentDto.setDays(days);
        bookAEquipmentDto.setBookEquipmentStatus(bookEquipmentStatus);
        bookAEquipmentDto.setPrice(price);
        bookAEquipmentDto.setToDate(toDate);
        bookAEquipmentDto.setFromDate(fromDate);
        bookAEquipmentDto.setEmail(user.getEmail());
        bookAEquipmentDto.setUsername(user.getName());
        bookAEquipmentDto.setUserId(user.getId());
        bookAEquipmentDto.setEquipmentId(equipment.getId());
        return bookAEquipmentDto;

    }

}
