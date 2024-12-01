SELECT 
    id,
    password,
    username,
    firstname,
    lastname,
    phone,
    role
FROM users 
WHERE username = '$username';

