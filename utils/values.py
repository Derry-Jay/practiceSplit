from extensions.custom_data_types import String

gmc = String('AIzaSyD9B1DCKjvUeerSsuPmlKSV4AMhnKLNDXI').get_google_maps_client()

email_pattern = String(r'^[a-z0-9]+[._]?[a-z0-9]+@\w+[.]\w{2,3}$').to_pattern()

password_pattern = String(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$').to_pattern()
