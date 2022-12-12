-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT description FROM crime_scene_reports
WHERE year = 2021
AND month = 7
AND day = 28
AND street = "Humphrey Street";

-- Theft took place at 10:15 am at the Humhrey Street bakery.
-- 3 witnesses, each of their interview transcripts mentions the bakery.
-- Searching for 3 witnesses...

SELECT name, transcript FROM interviews
WHERE transcript LIKE "%bakery%"
AND year = 2021
AND month = 7
AND day = 28;

-- 1 witness: Ruth | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
-- Searching for cars...

SELECT license_plate FROM bakery_security_logs
WHERE year = 2021
AND month = 7
AND day = 28
AND hour = 10
AND (minute > 15 AND minute <= 25)
AND activity = "exit";

-- 2 witness: Eugene  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

SELECT account_number FROM bank_accounts
WHERE person_id IN (
    SELECT id FROM people
    WHERE license_plate IN (
        SELECT license_plate FROM bakery_security_logs
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND hour = 10
        AND minute > 15 AND minute < 25
        AND activity = "exit"
    )
)
AND person_id in (
    SELECT id FROM people
    WHERE phone_number in (
        SELECT caller FROM phone_calls
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND duration < 60
    )
);

SELECT account_number FROM atm_transactions
WHERE atm_location = "Leggett Street"
AND year = 2021
AND month = 7
AND day = 28
AND transaction_type = "withdraw";

-- left 2 account_number: 49610011 and 26013199

SELECT name, phone_number, passport_number FROM people
WHERE id IN (
    SELECT person_id FROM bank_accounts
    WHERE account_number = 49610011 or account_number = 26013199
);

-- Now I suspect 2 people:
-- name: Diana | phone: (770) 555-1861 | passport: 3592750733
-- name: Bruce | phone: (367) 555-5533 | passport: 5773159633

-- if caller Diana, receiver - Philip | passport 3391710505:

SELECT name, passport_number FROM people
WHERE phone_number in (
    SELECT receiver FROM phone_calls
    WHERE year = 2021
    AND month = 7
    AND day = 28
    AND duration < 60
    AND caller = "(770) 555-1861"
);

-- if caller Bruce, receiver - Robin, no passport number

SELECT name, passport_number FROM people
WHERE phone_number in (
    SELECT receiver FROM phone_calls
    WHERE year = 2021
    AND month = 7
    AND day = 28
    AND duration < 60
    AND caller = "(367) 555-5533"
);


-- check Diana's and Bruce's flights. Bruce's - earliest, 8:20. So, Bruce is suspected and Robin is his accomplice
-- Destination_airport_id = 4

SELECT * FROM flights
WHERE year = 2021
AND month = 7
AND day = 29
AND origin_airport_id = (
    SELECT id FROM airports
    WHERE city = "Fiftyville"
)
AND id in (
    SELECT flight_id FROM passengers
    WHERE (passport_number = "5773159633")
);

SELECT * FROM airports
WHERE id = 4

-- LaGuardia Airport | New York City
