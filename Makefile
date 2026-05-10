.PHONY: install test deploy clean ui

install:
	pip install -r requirements.txt

test:
	python test_invoke.py

ui:
	streamlit run app.py

package:
	rm -rf package deployment.zip
	mkdir package
	pip install -r requirements.txt -t package/
	cp *.py package/
	cd package && zip -r ../deployment.zip .

deploy: package
	@if [ -z "$$LAMBDA_ROLE_ARN" ]; then \
		echo "ERROR: LAMBDA_ROLE_ARN is not set. Please export it or define it before running make deploy."; \
		exit 1; \
	fi
	@echo "Deploying to AWS Lambda..."
	@if aws lambda get-function --function-name TopicResearchAssistant > /dev/null 2>&1; then \
		echo "Function exists. Updating code..."; \
		aws lambda update-function-code --function-name TopicResearchAssistant --zip-file fileb://deployment.zip; \
	else \
		echo "Function does not exist. Creating new function..."; \
		aws lambda create-function \
			--function-name TopicResearchAssistant \
			--runtime python3.12 \
			--role $$LAMBDA_ROLE_ARN \
			--handler handler.lambda_handler \
			--timeout 90 \
			--zip-file fileb://deployment.zip; \
		echo "Waiting for function to become active..."; \
		sleep 5; \
		echo "Adding Function URL for public access (so Streamlit can reach it)..."; \
		aws lambda create-function-url-config \
			--function-name TopicResearchAssistant \
			--auth-type NONE; \
		aws lambda add-permission \
			--function-name TopicResearchAssistant \
			--statement-id FunctionURLAllowPublicAccess \
			--action lambda:InvokeFunctionUrl \
			--principal "*" \
			--function-url-auth-type NONE; \
	fi
	@echo "Deployment complete! If this was a new function, check the AWS Console for your Function URL to put into app.py."

clean:
	rm -rf package deployment.zip __pycache__
