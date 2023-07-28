.PHONY: create_db
create_db:
	python manage.py migrate

.PHONY: bootstrap_admin
bootstrap_admin: 
	python manage.py createsuperuser

.PHONY: map_and_index
map_and_index:
	docker run --network=gov-chat_gov_chat \
	--mount source=outputs,destination=/app/outputs \
	-e DATABASE_HOST=database \
	-e VECTOR_STORE_HOST=vectorstore \
	gov-chat-chat_server poetry run python gov_chat/webcraler_manager.py

.PHONY: test
test:
	docker run --network=gov-chat_gov_chat \
	-v ./models:/app/models/ \
	-e DATABASE_HOST=database \
	-e VECTOR_STORE_HOST=vectorstore \
	--name directory-test \
	--rm \
	gov-chat-chat_server ls models
	