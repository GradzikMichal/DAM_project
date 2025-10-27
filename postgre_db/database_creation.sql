CREATE TABLE images (
    image_id SERIAL primary key,
    image_name text not null,
    image_path text,
    user_id int not null,
    creation_date timestamp
);

create or replace FUNCTION add_image(
    img_name text,
    folder_path text,
    u_id int
) RETURNS int
LANGUAGE plpgsql
AS $_$
    DECLARE new_img_id int;
    begin
    select nextval('images_image_id_seq') into new_img_id;
    insert into images (image_id, image_name, user_id, creation_date, image_path)
           values (new_img_id, img_name, u_id, now(), concat(folder_path, '/', new_img_id));
    return new_img_id;
    end;
$_$;


