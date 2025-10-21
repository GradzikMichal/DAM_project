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
    DECLARE new_img_id integer;
    begin
    insert into images (image_name, user_id, creation_date)
           values (img_name, u_id, now());
    COMMIT;

    select (select image_id from images
            where creation_date=now() and user_id=u_id and image_name=img_name) into new_img_id;
    UPDATE images set image_path=concat(folder_path, new_img_id) where image_id=new_img_id;
    return new_img_id;

    end;
$_$;
