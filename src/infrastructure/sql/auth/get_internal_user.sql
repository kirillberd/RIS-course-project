SELECT 
    id,
    password,
    username,
    firstname,
    lastname,
    role
FROM internal_users
WHERE username = '$username';
