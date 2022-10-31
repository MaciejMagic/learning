-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT description FROM crime_scene_reports WHERE street = "Humphrey Street";

-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
-- Interviews were conducted today with three witnesses who were present at the time
-- – each of their interview transcripts mentions the bakery

SELECT description FROM crime_scene_reports
WHERE year = 2021 AND month = 07 AND day = 28 AND street = "Humphrey Street";
SELECT name, transcript FROM interviews
WHERE year = 2021 AND month = 07 AND day = 28;

-- Ruth: Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
-- If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
-- > bakery_security_logs
-- Eugane: I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery,
-- I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
-- > atm_transactions
-- Raymond: As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
-- In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
-- The thief then asked the person on the other end of the phone to purchase the flight ticket.

SELECT hour, minute, license_plate FROM bakery_security_logs
WHERE year = 2021 AND month = 07 AND day = 28 AND hour = 10 AND minute > 15 AND minute < 26 AND activity = "exit";

-- | 10   | 16     | 5P2BI95       |
-- | 10   | 18     | 94KL13X       |
-- | 10   | 18     | 6P58WS2       |
-- | 10   | 19     | 4328GD8       |
-- | 10   | 20     | G412CB7       |
-- | 10   | 21     | L93JTIZ       |
-- | 10   | 23     | 322W7JE       |
-- | 10   | 23     | 0NTHK55       |

SELECT name, phone_number, license_plate, passport_number FROM people
WHERE license_plate = "5P2BI95" OR license_plate = "94KL13X" OR license_plate = "6P58WS2" AND license_plate = "4328GD8"
OR license_plate = "G412CB7" OR license_plate = "L93JTIZ" OR license_plate = "322W7JE" OR license_plate = "0NTHK55";

-- |  name   |  phone_number  | license_plate | passport_number |
-- +---------+----------------+---------------+-----------------+
-- | Vanessa | (725) 555-4692 | 5P2BI95       | 2963008352      |
-- | Iman    | (829) 555-5269 | L93JTIZ       | 7049073643      |
-- | Sofia   | (130) 555-0289 | G412CB7       | 1695452385      |
-- | Diana   | (770) 555-1861 | 322W7JE       | 3592750733      |
-- | Kelsey  | (499) 555-9472 | 0NTHK55       | 8294398571      |
-- | Bruce   | (367) 555-5533 | 94KL13X       | 5773159633      |

SELECT account_number, amount FROM atm_transactions
WHERE year = 2021 AND month = 07 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw";

-- | 28500762       | 48     |
-- | 28296815       | 20     |
-- | 76054385       | 60     |
-- | 49610011       | 50     |
-- | 16153065       | 80     |
-- | 25506511       | 20     |
-- | 81061156       | 30     |
-- | 26013199       | 35     |

SELECT name, account_number FROM bank_accounts
JOIN people ON bank_accounts.person_id = people.id
WHERE account_number = 28500762 OR  account_number = 28296815 OR account_number = 76054385 OR account_number = 49610011
OR account_number = 16153065 OR account_number = 25506511 OR account_number = 81061156 OR account_number = 26013199;

-- |  name   | account_number |
-- +---------+----------------+
-- | Bruce   | 49610011       |
-- | Diana   | 26013199       |
-- | Brooke  | 16153065       |
-- | Kenny   | 28296815       |
-- | Iman    | 25506511       |
-- | Luca    | 28500762       |
-- | Taylor  | 76054385       |
-- | Benista | 81061156       |

SELECT caller, receiver FROM phone_calls
WHERE year = 2021 AND month = 07 AND day = 28 AND duration < 60;

-- |     caller     |    receiver    | duration |
-- +----------------+----------------+----------+
-- | (130) 555-0289 | (996) 555-8899 | 51       |
-- | (499) 555-9472 | (892) 555-8872 | 36       |
-- | (367) 555-5533 | (375) 555-8161 | 45       |
-- | (499) 555-9472 | (717) 555-1342 | 50       |
-- | (286) 555-6063 | (676) 555-6554 | 43       |
-- | (770) 555-1861 | (725) 555-3243 | 49       |
-- | (031) 555-6622 | (910) 555-3251 | 38       |
-- | (826) 555-1652 | (066) 555-9701 | 55       |
-- | (338) 555-6650 | (704) 555-2131 | 54       |

SELECT name, phone_number FROM people
WHERE phone_number = "(130) 555-0289" OR phone_number = "(499) 555-9472" OR phone_number = "(367) 555-5533" OR phone_number = "(499) 555-9472"
OR phone_number = "(286) 555-6063" OR phone_number = "(770) 555-1861" OR phone_number = "(031) 555-6622" OR phone_number = "(826) 555-1652" OR phone_number = "(338) 555-6650";

-- |  name   |  phone_number  |
-- +---------+----------------+
-- | Kenny   | (826) 555-1652 |
-- | Sofia   | (130) 555-0289 |
-- | Benista | (338) 555-6650 |
-- | Taylor  | (286) 555-6063 |
-- | Diana   | (770) 555-1861 |
-- | Kelsey  | (499) 555-9472 |
-- | Bruce   | (367) 555-5533 |
-- | Carina  | (031) 555-6622 |

SELECT name, phone_number FROM people
WHERE phone_number = "(996) 555-8899" OR phone_number = "(892) 555-8872" OR phone_number = "(375) 555-8161" OR phone_number = "(717) 555-1342"
OR phone_number = "(676) 555-6554" OR phone_number = "(725) 555-3243" OR phone_number = "(910) 555-3251" OR phone_number = "(066) 555-9701" OR phone_number = "(704) 555-2131";

-- |    name    |  phone_number  |
-- +------------+----------------+
-- | James      | (676) 555-6554 |
-- | Larry      | (892) 555-8872 |
-- | Anna       | (704) 555-2131 |
-- | Jack       | (996) 555-8899 |
-- | Melissa    | (717) 555-1342 |
-- | Jacqueline | (910) 555-3251 |
-- | Philip     | (725) 555-3243 |
-- | Robin      | (375) 555-8161 |
-- | Doris      | (066) 555-9701 |

-- | 8  | CSF          | Fiftyville Regional Airport             | Fiftyville

SELECT flights.hour, flights.minute, flights.origin_airport_id, flights.destination_airport_id, airports.full_name FROM flights
JOIN airports ON (flights.origin_airport_id = airports.id AND flights.destination_airport_id = airports.id)
WHERE year = 2021 AND month = 07 AND day = 29
ORDER BY hour;

SELECT flights.id, hour, minute, origin_airport_id, destination_airport_id FROM flights
JOIN airports ON flights.destination_airport_id = airports.id
WHERE year = 2021 AND month = 07 AND day = 29 AND origin_airport_id = 8
ORDER BY hour;

-- escaped to New York City

SELECT passport_number FROM passengers
JOIN flights ON passengers.flight_id = flights.id
WHERE flight_id = 36;

-- | passport_number |
-- +-----------------+
-- | 7214083635      |
-- | 1695452385      |
-- | 5773159633      |
-- | 1540955065      |
-- | 8294398571      |
-- | 1988161715      |
-- | 9878712108      |
-- | 8496433585      |

SELECT passport_number FROM people
WHERE name = "Diana" OR name = "Bruce";

-- | passport_number |
-- +-----------------+
-- | 3592750733      |
-- | 5773159633      |

SELECT name FROM people
WHERE passport_number = 5773159633;

-- Bruce is the thief

SELECT name, phone_number, passport_number, license_plate FROM people
WHERE name = "Bruce";

-- | name  |  phone_number  | passport_number | license_plate |
-- +-------+----------------+-----------------+---------------+
-- | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |

SELECT caller, receiver FROM phone_calls
WHERE year = 2021 AND month = 07 AND day = 28 AND duration < 60 AND caller = "(367) 555-5533";

-- |     caller     |    receiver    |
-- +----------------+----------------+
-- | (367) 555-5533 | (375) 555-8161 |

SELECT name, phone_number, passport_number, license_plate FROM people
WHERE phone_number = "(375) 555-8161";

-- | name  |  phone_number  | passport_number | license_plate |
-- +-------+----------------+-----------------+---------------+
-- | Robin | (375) 555-8161 |                 | 4V16VO0       |

-- Robin is the accomplice
