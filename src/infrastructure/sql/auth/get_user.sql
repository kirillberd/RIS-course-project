SELECT 
    id,
    password,
    username,
    firstname,
    lastname,
    phone,
    role
FROM external_users 
WHERE username = '$username';

