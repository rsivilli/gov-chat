.PHONY: create_db
create_db:
	python manage.py migrate

.PHONY: bootstrap_admin
bootstrap_admin: 
	python manage.py createsuperuser

.PHONY: map_and_index
map_and_index:
	docker run --network=gov-chat_gov_chat -e DATABASE_HOST=database -e VECTOR_STORE_HOST=vectorstore gov-chat-chat_server poetry run python gov_chat/webcraler_manager.py