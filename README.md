# crud-py
Crud basico para disciplina de Banco de dados NoSQL



Como ultilizar?

 python3 -m venv venv           
 source venv/bin/activate       
 pip install -r requirements.txt
 python app.py


 controllers:
  create_contact>-> {{base_url}}/contacts 
 Payload:
 
    {
    "name": "Nome user",
    "phone": "number",
    "email": "email"
    }

 get_all_contacts-> {{base_url}}/contacts?page=1&page_size=5

 get_contact_by_id -> {{base_url}}/contacts/{contact_id}
 
 
 update_contact-> {{base_url}}/contacts/{contact_id}
 Payload:
 {
  "phone": "(11) 99999-8888"
}
delete_contact- >{{base_url}}/contacts/{contact_id}